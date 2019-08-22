import datetime
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .models import CityInfoManager, CityTraffic, RoadTraffic, YearTraffic, RoadInfoManager, AirState
from attractions.tool.access_control_allow_origin import Access_Control_Allow_Origin


## http://127.0.0.1:8000/traffic/api/trafficindex/city/list?request_datetime=15432721&callback=jsonp_1563933175006`

@cache_page(timeout=60 * 23)
def citylist(
        request):
    now = datetime.datetime.now().timestamp()

    result = CityInfoManager.objects.all().values("pid", "cityname").iterator()
    response = {"data":
                    {"datetime": int(now),
                     "citylist": list(result),
                     "message": None}
                }
    response = JsonResponse(response)
    response = Access_Control_Allow_Origin(response)
    return response


# http://127.0.0.1:8000/traffic/api/trafficindex/city/curve?cityCode=340&type=hour&ddate=20190722&callback=jsonp_1563933175006
@cache_page(timeout=60 * 5)
def daily_index(request):
    pid = request.GET.get("cityCode")
    ddate = request.GET.get("ddate")
    ttype = request.GET.get("type")
    callback = request.GET.get("callback")  # jsonp_1563933175006
    if not (pid and ddate and ttype and callback):
        return JsonResponse({"status": 0})
    try:
        pid = int(pid)
        ddate = int(ddate)
        request_datetime = int(ddate)

    except Exception:

        return JsonResponse({"status": 0})
    response = cache.get(pid, default=None)

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

    return JsonResponse(response)


# http://127.0.0.1:8000/traffic/api/trafficindex/city/road?cityCode=100&request_datetime=1563475647&callback=jsonp_1563933175
def road_list(request):
    pid = request.GET.get("cityCode")
    callback = request.GET.get("callback")  # jsonp_1563933175006
    request_datetime = request.GET.get("request_datetime")
    if not (pid and callback):
        return JsonResponse({"status": 0})
    try:
        pid = int(pid)
        request_datetime = int(request_datetime)

    except Exception:
        return JsonResponse({"status": 0})
    now = datetime.datetime.now().timestamp()

    # if now - request_datetime > 10:  ## 反爬虫
    #     return JsonResponse({"status": 0})
    response = cache.get(pid, default=None)
    if not response:
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
    return JsonResponse(response)


# http://127.0.0.1:8000/traffic/api/trafficindex/city/detailroad?cityCode=100&id=4&up_date=1563968622
@cache_page(timeout=60 * 5)
def detail_road(request):
    pid = request.GET.get("cityCode")
    roadid = request.GET.get("id")
    up_date = request.GET.get("up_date")  # 重要参数，最近道路更新时间

    if not (pid and roadid and up_date):  # 反爬虫
        return JsonResponse({"status": 0})

    try:
        pid = int(pid)
        roadid = int(roadid)
        up_date = int(up_date)
    except Exception:
        return JsonResponse({"status": 0})

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

        return JsonResponse(response)
    return HttpResponse("none")


# http://127.0.0.1:8000/traffic/api/trafficindex/city/year?cityCode=130300
# @cache_page(60 * 60*15)
def yeartraffic(request):
    pid = request.GET.get("cityCode")
    if not pid:
        return JsonResponse({"status": 0})
    try:
        pid = int(pid)
    except Exception:
        return JsonResponse({"status": 0})
    yearpid = CityInfoManager.objects.get(pid=pid).yearpid
    result = YearTraffic.objects.filter(yearpid=yearpid, tmp_date__gt=20190101).values("tmp_date", "rate").distinct()
    response = {
        "data":
            {
                "detail":
                    {
                        "indexSet": list(result),
                    }
            }
    }
    return JsonResponse(response)


# http://scenicmonitor.top/traffic/api/airstate?&cityCode=810000
@cache_page(60*60)
def get_city_air(request):
    # 获取城市空气状况
    pid = request.GET.get("cityCode")
    try:
        obj = AirState.objects.filter(citypid=pid, flag=True).order_by("-lasttime"). \
            values("lasttime", 'aqi', 'pm2', 'pm10', 'co', 'no2', 'o3', 'so2')[0]
    except Exception as e:
        print(e)
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
    response = JsonResponse(response)
    response = Access_Control_Allow_Origin(response)
    return response

@cache_page(60*60*15)
def get_city_map(request):
    info = CityInfoManager.objects.all().values("pid", "cityname", "longitude", "latitude").iterator()
    result = {
        "data":
            list(info)
    }
    response = JsonResponse(result)
    response = Access_Control_Allow_Origin(response)
    return response
