import datetime
import json
import uuid
from django.http import JsonResponse
from django.core.cache import cache
from .models import CityInfoManager, CityTraffic, RoadTraffic, YearTraffic, RoadInfoManager, AirState
from attractions.tool.access_control_allow_origin import Access_Control_Allow_Origin


class CityDemo():
    ## http://127.0.0.1:8000/traffic/api/trafficindex/city/list?request_datetime=15432721&callback=jsonp_1563933175006`

    def citylist(self,
                 request):
        key = "city"

        response = cache.get(key)
        if response is None:
            now = datetime.datetime.now().timestamp()

            result = CityInfoManager.objects.all().values("pid", "cityname").iterator()
            response = {"data":
                            {"datetime": int(now),
                             "citylist": list(result),
                             "message": None}
                        }
            cache.set(key, response, 60 * 60 * 10)

        return Access_Control_Allow_Origin(response)

    # http://127.0.0.1:8000/traffic/api/trafficindex/city/curve?cityCode=340&type=hour&ddate=20190722&callback=jsonp_1563933175006
    def daily_index(self, request):
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
        key = "daily" + str(pid * 1111 + ddate)
        key = uuid.uuid5(uuid.NAMESPACE_OID, key)

        response = cache.get(key)
        if response is None:

            now = datetime.datetime.now().timestamp()
            # if now - request_datetime > 10:  # 反爬虫
            #     return JsonResponse({"status": 0})
            if not response:
                name = CityInfoManager.objects.get(pid=pid).cityname
                result = CityTraffic.objects.filter(pid=pid, ddate=ddate).values("ttime", "rate").iterator()
                response = {"data":
                    {
                        "city": name,
                        "now": int(now),
                        "indexlist": list(result),
                        "message": None,
                    }
                }

                cache.set(key, response, 60 * 30)

        return Access_Control_Allow_Origin(response)

    # http://127.0.0.1:8000/traffic/api/trafficindex/city/road?cityCode=100&request_datetime=1563475647&callback=jsonp_1563933175
    def road_list(self, request):
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
        key = "roadlist" + str(pid)
        key = uuid.uuid5(uuid.NAMESPACE_OID, key)

        response = cache.get(key)
        if response is None:
            updateSet = RoadInfoManager.objects.filter(citypid=pid).values("up_date")
            ##找出最早的时间，避免因为挖掘数据时出现了一个差错而导致部分未能正常录入，保证数据能完全展示给用户
            up_date = sorted(updateSet, key=lambda x: x['up_date'])[0]['up_date']
            result = RoadTraffic.objects.filter(citypid=pid, up_date=up_date).values("roadname", "speed", "direction",
                                                                                     "roadpid", "rate")
            response = {
                "data":
                    {
                        "roadlist": list(result),
                        "message": None,
                        'up_date': up_date  # 道路更新时间，非常重要

                    }
            }
            cache.set(key, response, 60 * 10)
        return Access_Control_Allow_Origin(response)

    # http://127.0.0.1:8000/traffic/api/trafficindex/city/detailroad?cityCode=100&id=4&up_date=1563968622
    def detail_road(self, request):
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
        key = "road" + str(pid * 1111 + roadid * 1000 + up_date)
        key = uuid.uuid5(uuid.NAMESPACE_OID, key)
        response = cache.get(key)
        if response is None:
            result = RoadTraffic.objects.filter(citypid=pid, up_date=up_date, roadpid=roadid).values("bounds", "data")

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
                cache.set(key, response, 60 * 10)

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

    # http://127.0.0.1:8000/traffic/api/trafficindex/city/year?cityCode=235
    def yeartraffic(self, request):
        pid = request.GET.get("cityCode")
        if not pid:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        try:
            pid = int(pid)
        except ValueError:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        key = "year" + str(pid)
        key = uuid.uuid5(uuid.NAMESPACE_OID, key)
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
            cache.set(key, response, 60 * 60 * 10)
        return Access_Control_Allow_Origin(response)

    # http://scenicmonitor.top/traffic/api/airstate?&cityCode=810000
    def get_city_air(self, request):
        # 获取城市空气状况
        pid = request.GET.get("cityCode")
        key = "air" + str(pid)
        key = uuid.uuid5(uuid.NAMESPACE_OID, key)
        response = cache.get(key)
        if response is None:
            try:
                obj = AirState.objects.filter(citypid=pid, flag=True).order_by("-lasttime"). \
                    values("lasttime", 'aqi', 'pm2', 'pm10', 'co', 'no2', 'o3', 'so2')[0]
            except IndexError:
                return JsonResponse({"status": 0, "message": "不好意思，最新数据还未采集成功"})
            lasttime = obj['lasttime']
            aqi = obj['aqi']
            pm2 = obj['pm2']
            pm10 = obj['pm10']
            co = obj['co']
            no2 = obj['no2']
            o3 = obj['o3']
            so2 = obj['so2']
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
            cache.set(key, response, 60 * 60)
        return Access_Control_Allow_Origin(response)

    # http://127.0.0.1:8000/traffic/api/getCityInfo

    def get_city_map(self, request):
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
