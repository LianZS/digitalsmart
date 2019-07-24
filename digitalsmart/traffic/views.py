import datetime
import json
from django.http import JsonResponse
from .models import CityManager, CityTraffic, RoadTraffic


#
def citylist(request):
    callback = request.GET.get("callback")  # jsonp_1563933175006
    request_datetime = request.GET.get("datetime")

    now = datetime.datetime.now().timestamp()
    # request_datetime = int(request_datetime)
    # if now - request_datetime > 10:
    #     return JsonResponse({"status": 0})
    result = CityManager.objects.all().values("pid", "name").iterator()
    return JsonResponse(
        {"data":
             {"datetime": int(now),
              "citylist": list(result),
              "message": None}
         }
    )


def daily_index(request):  # ?cityCode=340&type=minute&
    pid = request.GET.get("cityCode")
    ddate = request.GET.get("ddate")
    ttype = request.GET.get("type")
    callback = request.GET.get("callback")  # jsonp_1563933175006
    pid = int(pid)
    ddate = int(ddate)
    now = datetime.datetime.now().timestamp()
    request_datetime = int(ddate)
    # if now - request_datetime > 10:
    #     return JsonResponse({"status": 0})
    name = CityManager.objects.get(pid=pid).name
    result = CityTraffic.objects.filter(pid=pid, ddate=ddate).values("ttime", "rate").iterator()

    return JsonResponse(
        {"data": {
            "city": name,
            "now": int(now),
            "indexlist": list(result),
            "message": None,
        }
        }
    )


def road_list(request):  # 317&1563475647

    pid = request.GET.get("cityCode")
    ttype = request.GET.get("type")
    callback = request.GET.get("callback")  # jsonp_1563933175006
    pid = int(pid)
    now = datetime.datetime.now().timestamp()
    # if now - request_datetime > 10:
    #     return JsonResponse({"status": 0})
    result = RoadTraffic.objects.filter(pid=pid, up_date=1563475647).values("pid", "roadname", "speed", "direction",
                                                                            )
    return JsonResponse(
        {
            "data":
                {
                    "roadlist": list(result),
                    "message": None,

                }
        }
    )


def detail_road(request):  # trafficindex/city/roadcurve?cityCode=200&id=x&callback=jsonp_1563936493102_4624051
    pid = request.GET.get("cityCode")
    roadid = request.GET.get("num")
    result = RoadTraffic.objects.filter(pid=pid, up_date=1563475647).values("bound", "data")[0]
    bounds = result.get("bound")
    data = result.get("data")
    print()

    return JsonResponse(
        {
            "data":
                {
                    "detail":
                        {
                            "bounds": json.loads(bounds),
                            "data": json.loads(data),
                        }
                }
        }
    )
