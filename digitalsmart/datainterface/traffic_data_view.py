import datetime
import json
import uuid
from django.http import JsonResponse
from django.core.cache import cache
from traffic.models import CityInfoManager, CityTraffic, RoadTraffic, YearTraffic, RoadInfoManager, AirState
from attractions.tool.access_control_allow_origin import Access_Control_Allow_Origin


class CityTrafficView():

    # http://127.0.0.1:8000/interface/api/getCitydailyIndex?cityCode=340&ddate=20190722&token=bGlhbnpvbmdzaGVuZw==
    def daily_index(self, request):
        pid = request.GET.get("cityCode")
        ddate = request.GET.get("ddate")
        token = request.GET.get("token")
        if token != "bGlhbnpvbmdzaGVuZw==":
            return JsonResponse({"status": 0, "message": "appkey错误"})
        if not (pid and ddate and token):
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        try:
            pid = int(pid)
            ddate = int(ddate)

        except ValueError:

            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        try:

            cityname = CityInfoManager.objects.get(pid=pid).cityname
        except Exception:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        result = CityTraffic.objects.filter(pid=pid, ddate=ddate).values("ttime", "rate").iterator()
        response = {"data":
            {
                "city": cityname,
                "cityCode": pid,
                "indexlist": list(result),
                "date": ddate
            }
        }

        return JsonResponse(response)

    # http://127.0.0.1:8000/interface/api/getCityRoadlist?cityCode=100&token=bGlhbnpvbmdzaGVuZw==
    def road_list(self, request):
        pid = request.GET.get("cityCode")
        token = request.GET.get("token")
        if token != "bGlhbnpvbmdzaGVuZw==":
            return JsonResponse({"status": 0, "message": "appkey错误"})
        if not pid:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        try:
            pid = int(pid)

        except ValueError:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})

        updateSet = RoadInfoManager.objects.filter(citypid=pid).values("up_date")
        ##找出最早的时间，避免因为挖掘数据时出现了一个差错而导致部分未能正常录入，保证数据能完全展示给用户
        up_date = sorted(updateSet, key=lambda x: x['up_date'])[0]['up_date']
        result = RoadTraffic.objects.filter(citypid=pid, up_date=up_date).values("roadname", "speed", "direction",
                                                                                 "roadpid", "rate")
        response = {

            "roadlist": list(result),
            "cityCode": pid

        }
        return JsonResponse(response)

    # http://127.0.0.1:8000/interface/api/getCityMonthsTraffic?cityCode=235&token=bGlhbnpvbmdzaGVuZw==
    def yeartraffic(self, request):
        pid = request.GET.get("cityCode")
        token = request.GET.get("token")
        if token != "bGlhbnpvbmdzaGVuZw==":
            return JsonResponse({"status": 0, "message": "appkey错误"})
        if not pid:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        try:
            pid = int(pid)
        except ValueError:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        try:
            obj = CityInfoManager.objects.get(pid=pid)
            yearpid = obj.yearpid
            cityname = obj.cityname
        except Exception:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})

        result = YearTraffic.objects.filter(yearpid=yearpid, tmp_date__gt=20190101).values("tmp_date",
                                                                                           "rate").distinct()
        response = {
            "cityCode": pid,
            "city": cityname,

            "indexSet": list(result),

        }
        return JsonResponse(response)

    # http://127.0.0.1:8000/interface/api/getCityAirState?&cityCode=810000&token=bGlhbnpvbmdzaGVuZw==
    def get_city_air(self, request):
        # 获取城市空气状况
        pid = request.GET.get("cityCode")
        token = request.GET.get("token")
        if token != "bGlhbnpvbmdzaGVuZw==":
            return JsonResponse({"status": 0, "message": "appkey错误"})
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
                "cityCode": pid,
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
        return JsonResponse(response)

