import datetime
import json
import uuid
from django.http import JsonResponse
from django.core.cache import cache
from digitalsmart.settings import redis_cache
from .models import CityInfoManager, CityTraffic, RoadTraffic, YearTraffic, RoadInfoManager, AirState
from attractions.tool.access_control_allow_origin import Access_Control_Allow_Origin


class CityDemo:

    def citylist(self,
                 request):

        """
        获取城市列表- 链接格式：
        http://127.0.0.1:8000/traffic/api/trafficindex/city/list?request_datetime=15432721&callback=jsonp_1563933175006`

        :param request:
        :return:response = {"data":
                            {"datetime": int(now),
                             "citylist": list(result),
                             "message": None}
                        }
        """
        key = "city"

        response = cache.get(key)  # 查看是否有缓存
        if response is None:  # 没有的话查询
            now = datetime.datetime.now().timestamp()

            result = CityInfoManager.objects.all().values("pid", "cityname").iterator()
            response = {"data":
                            {"datetime": int(now),
                             "citylist": list(result),
                             "message": None}
                        }
            cache.set(key, response, 60 * 60 * 10)

        return Access_Control_Allow_Origin(response)

    def daily_index(self, request):
        """
        获取实时交通拥堵延迟指数--链接格式：
        http://127.0.0.1:8000/traffic/api/trafficindex/city/curve?cityCode=340&type=hour&ddate=20190722&
        callback=jsonp_1563933175006
        :param request:
        :return:response = {"data":
                {
                    "city": name,
                    "now": int(now),
                    "indexlist": result,
                    "message": None,
                }
            }
        """
        pid = request.GET.get("cityCode")
        ddate = request.GET.get("ddate")
        ttype = request.GET.get("type")
        callback = request.GET.get("callback")  # jsonp_1563933175006
        if not (pid and ddate and ttype and callback):
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        try:
            pid = int(pid)
            ddate = int(ddate)
            request_datetime = int(ddate)

        except ValueError:

            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        key = "traffic:{0}".format(pid)
        response = cache.get(key)
        if response is None or len(response.keys()) == 0:
            now = datetime.datetime.now().timestamp()  # 当前时间戳
            # if now - request_datetime > 10:  # 反爬虫
            #     return JsonResponse({"status": 0})
            # 先从内存读取数据
            name = CityInfoManager.objects.get(pid=pid).cityname  # 获取城市名字
            result = redis_cache.hashget(key, data_key_name="ttime", data_value_name="rate")  # 直接从内存里获取数据，减轻数据库压力
            result = list(result)
            if len(result) == 0:  # 当内存没有数据时从数据库读取
                result = CityTraffic.objects.filter(pid=pid, ddate=ddate).values("ttime", "rate").iterator()
                result = list(result)
            response = {"data":
                {
                    "city": name,
                    "now": int(now),
                    "indexlist": result,
                    "message": None,
                }
            }

            cache.set(key, response, 60 * 30)  # 缓存

        return Access_Control_Allow_Origin(response)

    def road_list(self, request):
        """
        获取城市拥堵道路基本信息--链接格式：
        http://127.0.0.1:8000/traffic/api/trafficindex/city/road?cityCode=148&request_datetime=1568867086&
        callback=jsonp_1563933175
        :param request:
        :return: response = {
                "data":
                    {
                        "roadlist": result,
                        "message": None,
                        'up_date': up_date  # 道路更新时间

                    }
            }
        """
        pid = request.GET.get("cityCode")
        callback = request.GET.get("callback")  # jsonp_1563933175006
        request_datetime = request.GET.get("request_datetime")
        if not (pid and callback):
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        try:
            pid = int(pid)
            request_datetime = int(request_datetime)

        except ValueError:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        now = datetime.datetime.now().timestamp()

        # if now - request_datetime > 10:  ## 反爬虫
        #     return JsonResponse({"status": 0})
        key = "road:{0}".format(pid)

        response = cache.get(key)
        if response is None or len(response.keys()) == 0:
            # 先从内存读取数据
            keys: list = redis_cache.keys(pattern=key + ":*")  # 找出该key下所有的key
            result = redis_cache.get(keys, "roadname", "speed", "direction",
                                     "roadpid", "rate", "up_date")
            result = list(result)
            if len(result) == 0:  # 当内存没有数据时从数据库读取
                updateSet = RoadInfoManager.objects.filter(citypid=pid).values("up_date")
                ##找出最早的时间，避免因为挖掘数据时出现了一个差错而导致部分未能正常录入，保证数据能完全展示给用户
                up_date = sorted(updateSet, key=lambda x: x['up_date'])[0]['up_date']
                result = RoadTraffic.objects.filter(citypid=pid, up_date=up_date).values("roadname", "speed",
                                                                                         "direction",
                                                                                         "roadpid", "rate")
                result = list(result)
            up_date = result[0]['up_date']  # 道路最近更新时间
            response = {
                "data":
                    {
                        "roadlist": result,
                        "message": None,
                        'up_date': up_date  # 道路更新时间，非常重要

                    }
            }
            cache.set(key, response, 60 * 10)
        return Access_Control_Allow_Origin(response)

    def detail_road(self, request):
        """
        获取城市某条道路的拥堵延迟数据--链接格式：
        http://127.0.0.1:8000/traffic/api/trafficindex/city/detailroad?cityCode=100&id=4&up_date=1563968622
        :param request:
        :return: response = {
                    "data":
                        {
                            "detail":
                                {
                                    "bounds": json.loads(bounds),
                                    "data": json.loads(data),
                                }
                        }
                }
        """
        pid = request.GET.get("cityCode")
        roadid = request.GET.get("id")
        up_date = request.GET.get("up_date")  # 重要参数，最近道路更新时间

        if not (pid and roadid and up_date):  # 反爬虫
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})

        try:
            pid = int(pid)
            roadid = int(roadid)
            up_date = int(up_date)
        except ValueError:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        key = "road:{pid}:{roadpid}".format(pid=pid, roadpid=roadid)
        response = cache.get(key)
        if response is None or len(response.keys()) == 0:
            # 先从内存读取数据

            result = redis_cache.get(key, "bounds", "data")
            result = list(result)
            if len(result) == 0:  # 当内存没有数据时从数据库读取
                result = RoadTraffic.objects.filter(citypid=pid, up_date=up_date, roadpid=roadid).values("bounds",
                                                                                                         "data")
                result = list(result)
            if len(result) > 0:
                bounds = result[0]['bounds']
                data = result[0]['data']
                response = {
                    "data":
                        {
                            "detail":
                                {
                                    "bounds": json.loads(bounds),
                                    "data": json.loads(data),
                                }
                        }
                }
                cache.set(key, response, 60 * 11)  # 缓存数据

            else:
                response = {
                    "data":
                        {
                            "detail":
                                {
                                    "bounds": None,
                                    "data": None,
                                }
                        }
                }
        return Access_Control_Allow_Origin(response)

    def yeartraffic(self, request):
        """
        获取城市季度交通拥堵延迟数据--链接格式 ：
        http://127.0.0.1:8000/traffic/api/trafficindex/city/year?cityCode=235
        :param request:
        :return:response = {
                "data":
                    {
                        "detail":
                            {
                                "indexSet": list(result),
                            }
                    }
            }
        """
        pid = request.GET.get("cityCode")
        if not pid:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        try:
            pid = int(pid)
        except ValueError:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        key = "yeartraffic:{0}".format(pid)
        response = cache.get(key)
        if response is None:
            yearpid = CityInfoManager.objects.get(pid=pid).yearpid
            result = YearTraffic.objects.filter(yearpid=yearpid, tmp_date__gt=20190101).values("tmp_date",
                                                                                               "rate").distinct()
            response = {
                "data":
                    {
                        "detail":
                            {
                                "indexSet": list(result),
                            }
                    }
            }
            cache.set(key, response, 60 * 60 * 20)  # 缓存数据
        return Access_Control_Allow_Origin(response)

    def get_city_air(self, request):
        """
        获取城市空气状况--链接格式：
        http://scenicmonitor.top/traffic/api/airstate?&cityCode=810000
        :param request:
        :return: response = {
                "pid": pid,
                "lasttime": lasttime,
                "data": {
                    "aqi": aqi,
                    "pm2": pm2,
                    "pm10": pm10,
                    "co": co,
                    "no2": no2,
                    "o3": o3,
                    "so2": so2

                }
            }
        """

        pid = request.GET.get("cityCode")
        key = "air:{0}".format(pid)
        response = cache.get(key)
        if response is None or len(response.keys()) == 0:
            result = redis_cache.hashget(key=key)  # 先从内存获取数据
            result = list(result)[0]
            if len(result.keys()) == 0:  # 当内存没有数据时从数据库获取

                try:
                    result = AirState.objects.filter(citypid=pid, flag=True).order_by("-lasttime"). \
                        values("lasttime", 'aqi', 'pm2', 'pm10', 'co', 'no2', 'o3', 'so2')[0]
                    print("e")
                except IndexError:
                    return JsonResponse({"status": 0, "message": "不好意思，最新数据还未采集成功"})
            lasttime = result['lasttime']
            aqi = result['aqi']
            pm2 = result['pm2']
            pm10 = result['pm10']
            co = result['co']
            no2 = result['no2']
            o3 = result['o3']
            so2 = result['so2']
            response = {
                "pid": pid,
                "lasttime": lasttime,
                "data": {
                    "aqi": aqi,
                    "pm2": pm2,
                    "pm10": pm10,
                    "co": co,
                    "no2": no2,
                    "o3": o3,
                    "so2": so2

                }
            }
            cache.set(key, response, 60 * 60)  # 缓存数据
        return Access_Control_Allow_Origin(response)

    def get_city_map(self, request):
        """
        获取城市地图信息--链接格式：
        http://127.0.0.1:8000/traffic/api/getCityInfo
        :param request:
        :return:
        """
        key = "city_map"
        response = cache.get(key)
        if response is None:
            info = CityInfoManager.objects.all().values("pid", "cityname", "longitude", "latitude").iterator()
            response = {
                "data":
                    list(info)
            }
            cache.set(key, response, 60 * 60 * 10)
        return Access_Control_Allow_Origin(response)
