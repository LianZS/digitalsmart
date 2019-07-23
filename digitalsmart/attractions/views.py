import datetime
import re
from django.http import JsonResponse
from attractions.models import ScenceManager, SearchRate, TableManager, Geographic
from django.db import connection


# Create your views here.


def citylist(request):  # http://127.0.0.1:8000/attractions/test/?province=广东省
    # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:# 反爬虫
    #
    #     return JsonResponse({"status": 0})
    province = request.GET.get('province')
    if not province:
        return JsonResponse({"status": 0})
    result = ScenceManager.objects.filter(province=province).values("loaction", "citypid").distinct()
    response = {"province": province, "city": list(result)}
    return JsonResponse(response)


def scencelist(request):  # http://127.0.0.1:8000/attractions/api/getRegionsByCity?province=广东省&location=深圳市&citypid=340
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


def scenceflow_data(
        request):  # http://127.0.0.1:8000/attractions/api/getLocation_pn_percent_new?pid=2&date_begin=20190722&&date_end=20190723&predict=true
    # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:  # 反爬虫
    #     return JsonResponse({"status": 0})

    pid = request.GET.get("pid")
    date_begin = request.GET.get("date_begin")
    date_end = request.GET.get("date_end")
    predict = request.GET.get("predict")  # 是否预测
    sub_domain = request.GET.get('sub_domain')  # 是否为开发者标识

    if not pid or not date_begin or not date_end or not predict:
        return JsonResponse({"status": 0})
    try:
        pid = int(pid)
        date_begin = int(date_begin)
        date_end = int(date_end)
    except Exception:
        return JsonResponse({"status": 0})
    # result = ScenceFlow.objects.raw('select id,ttime,num from digitalsmart.scenceflow where pid=%s and ddate=%s',
    #
    #                                 params=[pid, date_begin])
    with connection.cursor() as cursor:
        cursor.execute("select ttime,num from digitalsmart.scenceflow "
                       "where pid= %s and ddate=%s ", [pid, date_begin])
        rows = cursor.fetchall()
        result = sorted(rows, key=lambda x: str(x[0]))  # 排序

    response = {"data": result}
    return JsonResponse(response)


def scenceflow_trend(
        request):  # http://127.0.0.1:8000/attractions/api/getLocation_trend_percent_new?&pid=18346&date_begin=20190722&&date_end=20190723&predict=true
    pid = request.GET.get("pid")
    date_begin = request.GET.get("date_begin")
    date_end = request.GET.get("date_end")
    predict = request.GET.get("predict")  # 是否预测
    sub_domain = request.GET.get('sub_domain')  # 是否为开发者标识

    if not pid or not date_begin or not date_end or not predict:
        return JsonResponse({"status": 0})
    try:
        pid = int(pid)
        date_begin = int(date_begin)
        date_end = int(date_end)
    except Exception:
        return JsonResponse({"status": 0})
    with connection.cursor() as cursor:
        cursor.execute("select ttime,rate from digitalsmart.scencetrend where pid=%s and ddate=%s", [pid, date_begin])
        rows = cursor.fetchall()
        result = sorted(rows, key=lambda x: str(x[0]))  # 排序

    response = {"data": result}
    return JsonResponse(response)


def search_heat(
        request):  # 搜索热度#http://127.0.0.1:8000/attractions/api/getLocation_search_rate?&pid=158&date_begin=20190722&date_end=20190723&sub_domain=
    pid = request.GET.get("pid")
    sub_domain = request.GET.get('sub_domain')  # 是否为开发者标识

    if not pid:
        return JsonResponse({"status": 0})
    try:
        pid = int(pid)
    except Exception:
        return JsonResponse({"status": 0})
    old = datetime.datetime.today() - datetime.timedelta(days=30)
    olddate = int(str(old.date()).replace("-", ""))
    rows = SearchRate.objects.filter(pid=pid, tmp_date__gt=olddate).values("tmp_date", "name", "rate").iterator()
    wechat = list()
    baidu = list()
    sougou = list()

    for item in rows:
        if item['name'] == 'wechat':
            wechat.append(item)

        elif item['name'] == 'sougou':
            sougou.append(item)
        else:
            baidu.append(item)
    response = {"微信": wechat, "搜狗": sougou, "百度": baidu}
    return JsonResponse(response)


def scence_people_distribution(
        request):  # http://127.0.0.1:8000/attractions/api/getLocation_distribution_rate?pid=4910&sub_domain=
    pid = request.GET.get("pid")
    if not pid:
        return JsonResponse({"status": 0})
    try:
        pid = int(pid)
    except Exception:
        return JsonResponse({"status": 0})
    sub_domain = request.GET.get('sub_domain')  # 是否为开发者标识
    obj = TableManager.objects.get(pid=pid)
    last_up: int = obj.last_date  # 最近更新时间
    table_id: int = obj.table_id  # 表位置
    # 下面之所以不格式化字符串，是预防注入
    sql = None
    if table_id == 0:
        sql = "select lat,lon,num from digitalsmart.peopleposition0 where pid=%s and tmp_date=%s"
    elif table_id == 1:
        sql = "select lat,lon,num from digitalsmart.peopleposition1 where pid=%s and tmp_date=%s"
    elif table_id == 2:
        sql = "select lat,lon,num from digitalsmart.peopleposition2 where pid=%s and tmp_date=%s"
    elif table_id == 3:
        sql = "select lat,lon,num from digitalsmart.peopleposition3 where pid=%s and tmp_date=%s"
    elif table_id == 4:
        sql = "select lat,lon,num from digitalsmart.peopleposition4 where pid=%s and tmp_date=%s"
    elif table_id == 5:
        sql = "select lat,lon,num from digitalsmart.peopleposition5 where pid=%s and tmp_date=%s"
    elif table_id == 6:
        sql = "select lat,lon,num from digitalsmart.peopleposition6 where pid=%s and tmp_date=%s"
    elif table_id == 7:
        sql = "select lat,lon,num from digitalsmart.peopleposition7 where pid=%s and tmp_date=%s"
    elif table_id == 8:
        sql = "select lat,lon,num from digitalsmart.peopleposition8 where pid=%s and tmp_date=%s"
    elif table_id == 9:
        sql = "select lat,lon,num from digitalsmart.peopleposition9 where pid=%s and tmp_date=%s"

    with connection.cursor() as cursor:
        cursor.execute(sql,
                       [pid, last_up])
        rows = cursor.fetchall()
        data = list()
        for item in rows:
            lat = item[0]
            lon = item[1]
            num = item[2]
            data.append({"lat": lat, "lon": lon, "num": num})
    return JsonResponse({"data": data})


def scence_geographic(request):
    pid = request.GET.get("pid")
    if not pid:
        return JsonResponse({"status": 0})
    try:
        pid = int(pid)
    except Exception:
        return JsonResponse({"status": 0})
    with connection.cursor() as cursor:
        cursor.execute("select longitude,latitude from digitalsmart.geographic where pid=%s", [pid])
        rows = cursor.fetchall()

    return JsonResponse({"bounds": rows})
