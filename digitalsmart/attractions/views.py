from django.shortcuts import render, HttpResponse, Http404
from django.http import JsonResponse
from attractions.models import ScenceManager, ScenceFlow
from django.db import connection


# Create your views here.


def cityList(request):  # http://127.0.0.1:8000/attractions/test/?province=广东省
    # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:# 反爬虫
    #
    #     return JsonResponse({"status": 0})
    province = request.GET.get('province')
    if not province:
        return JsonResponse({"status": 0})
    result = ScenceManager.objects.filter(province=province).values("loaction", "citypid").distinct()
    response = {"province": province, "city": list(result)}
    return JsonResponse(response)


def scenceList(request):  # http://127.0.0.1:8000/attractions/api/getRegionsByCity?province=广东省&location=深圳市&citypid=340
    # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:  # 反爬虫
    #     return JsonResponse({"status": 0})
    province = request.GET.get("province")
    city = request.GET.get("location")
    citypid = request.GET.get("citypid")

    if not len(city) or not len(province) or not citypid:
        return JsonResponse({"status": 0})
    result = ScenceManager.objects.filter(province=province, loaction=city, citypid=citypid).values("area", "pid")
    response = {"city": city, "area": list(result)}

    return JsonResponse(response)


def scenceflowData(request):
    pid: int = int(request.GET.get("pid"))
    date_begin: int = int(request.GET.get("date_begin"))
    date_end: int = request.GET.get("date_end")
    predict = request.GET.get("predict")  # 是否预测
    # result = ScenceFlow.objects.raw('select id,ttime,num from digitalsmart.scenceflow where pid=%s and ddate=%s',
    #
    #                                 params=[2, 20190722])
    with connection.cursor() as cursor:
        cursor.execute("select ttime,num from digitalsmart.scenceflow "
                       "where pid= %s and ddate=%s ", [pid, date_begin])
        row = cursor.fetchall()

    response = {"data": row}
    return JsonResponse(response)
