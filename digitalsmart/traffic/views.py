import datetime
import json
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .models import CityManager, CityTraffic, RoadTraffic, YearTraffic


#
@cache_page(timeout=None)
def citylist(
        request):  # http://xx/traffic/trafficindex/city/list?request_datetime=15432721&callback=jsonp_1563933175006`

    now = datetime.datetime.now().timestamp()

    result = CityManager.objects.all().values("pid", "name").iterator()
    response = {"data":
                    {"datetime": int(now),
                     "citylist": list(result),
                     "message": None}
                }

    return JsonResponse(response)


def daily_index(request):  # ?cityCode=340&type=hour&ddate=20190722&callback=jsonp_1563933175006
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
        name = CityManager.objects.get(pid=pid).name
        result = CityTraffic.objects.filter(pid=pid, ddate=ddate).values("ttime", "rate").iterator()
        response = {"data":
            {
                "city": name,
                "now": int(now),
                "indexlist": list(result),
                "message": None,
            }
        }
        cache.set(pid, response, 60 * 30)

    return JsonResponse(response)


def road_list(request):  # trafficindex/city/road?cityCode =317&request_datetime=1563475647&callback=jsonp_1563933175006
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
    up_date = 1563714751
    if not response:
        result = RoadTraffic.objects.filter(pid=pid, up_date=up_date).values("pid", "roadname", "speed", "direction",
                                                                             "roadid")
        response = {
            "data":
                {
                    "roadlist": list(result),
                    "message": None,

                }
        }
        cache.set(pid, response, timeout=60 * 10)
    return JsonResponse(response)


def detail_road(request):  # trafficindex/city/detailroad?cityCode=200&id=x&callback=jsonp_1563936493102_4624051
    pid = request.GET.get("cityCode")
    roadid = request.GET.get("id")
    if not (pid and roadid):  # 反爬虫
        return JsonResponse({"status": 0})
    try:
        pid = int(pid)
        roadid = int(roadid)
    except Exception:
        return JsonResponse({"status": 0})
    key = pid * 1000 + roadid
    response = cache.get(key, default=None)
    if not response:
        up_date = 1563938551
        result = RoadTraffic.objects.filter(pid=pid, up_date=up_date, roadid=roadid).values("bound", "data")
        if len(result) > 0:
            bounds = result[0]['bound']
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

    return JsonResponse(response)


@cache_page(60 * 60 * 24)
def yeartraffic(request):  # http://127.0.0.1:8000/traffic/trafficindex/city/year?cityCode=130300

    pid = request.GET.get("cityCode")
    if not pid:
        return JsonResponse({"status": 0})
    try:
        pid = int(pid)
    except Exception:
        return JsonResponse({"status": 0})

    result = YearTraffic.objects.filter(pid=pid, tmp_date__gt=20190101).values("tmp_date", "rate").distinct()
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
