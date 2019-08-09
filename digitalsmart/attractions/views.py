import datetime
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tool.access_control_allow_origin import Access_Control_Allow_Origin
from attractions.models import ScenceManager, SearchRate, TableManager
from django.db import connection


# Create your views here.
# http://127.0.0.1:8000/attractions/api/getCitysByProvince?province=广东省
@cache_page(timeout=None)  # 永久缓存
def citylist(request):
    # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:# 反爬虫
    #
    #     return JsonResponse({"status": 0})
    province = request.GET.get('province')  # 广东省
    if not province:
        return JsonResponse({"status": 0})
    result = ScenceManager.objects.filter(province=province).values("loaction", "citypid").distinct()
    response = {"province": province, "city": list(result)}
    #站点跨域请求的问题
    response=JsonResponse(response)

    response = Access_Control_Allow_Origin(response)

    return response


## http://127.0.0.1:8000/attractions/api/getRegionsByCity?province=广东省&location=深圳市&citypid=340
@cache_page(timeout=None)
def scencelist(request):
    # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:  # 反爬虫
    #     return JsonResponse({"status": 0})
    province = request.GET.get("province")
    city = request.GET.get("location")  # 深圳市
    citypid = request.GET.get("citypid")  # 123

    if not len(city) or not len(province) or not citypid:
        return JsonResponse({"status": 0})
    result = ScenceManager.objects.filter(province=province, loaction=city, citypid=citypid).values("area", "pid")
    response = {"city": city, "area": list(result)}
    #站点跨域请求的问题
    response=JsonResponse(response)

    response = Access_Control_Allow_Origin(response)
    return response


# http://127.0.0.1:8000/attractions/api/getLocation_pn_percent_new?pid=2&date_begin=20190722&&date_end=20190723&
# predict=true&sub_domain=
@cache_page(timeout=60 * 5)
def scenceflow_data(
        request):
    # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:  # 反爬虫
    #     return JsonResponse({"status": 0})

    pid = request.GET.get("pid")
    date_begin = request.GET.get("date_begin")  # 20190722
    date_end = request.GET.get("date_end")  # 20190723
    predict = request.GET.get("predict")  # 是否预测,true,false
    sub_domain = request.GET.get('sub_domain')  # 是否为开发者标识

    if not (pid and date_begin and date_end and predict):
        return JsonResponse({"status": 0})
    try:
        pid = int(pid)
        date_begin = int(date_begin)
        date_end = int(date_end)
    except Exception:
        return JsonResponse({"status": 0})

    with connection.cursor() as cursor:
        cursor.execute("select ttime,num from digitalsmart.scenceflow "
                       "where pid= %s and ddate=%s ", [pid, date_begin])
        rows = cursor.fetchall()
        result = sorted(rows, key=lambda x: str(x[0]))  # 排序

    response = {"data": result}
    return JsonResponse(response)


# http://127.0.0.1:8000/attractions/api/getLocation_trend_percent_new?&pid=18346&date_begin=20190722&&date_end=20190723
# &predict=true&sub_domain=
@cache_page(timeout=60 * 5)
def scenceflow_trend(
        request):
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


# http://127.0.0.1:8000/attractions/api/getLocation_search_rate?&pid=158&date_begin=20190722&date_end=20190723&sub_domain=
@cache_page(timeout=60 * 60 * 12)
def search_heat(
        request):  # 搜索热度
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


# http://127.0.0.1:8000/attractions/api/getLocation_distribution_rate?pid=4910&flag=0&sub_domain=
@cache_page(timeout=60 * 5)
def scence_people_distribution(
        request):
    pid = request.GET.get("pid")
    flag = request.GET.get("flag")
    if not (pid and flag):
        return JsonResponse({"status": 0})
    try:
        pid = int(pid)
        flag = int(flag)
    except Exception:
        return JsonResponse({"status": 0})
    sub_domain = request.GET.get('sub_domain')  # 是否为开发者标识
    obj = TableManager.objects.get(pid=pid, flag=flag)  # 避免重复冲突
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


# http://127.0.0.1:8000/attractions/api/getLocation_geographic_bounds?pid=1398&flag=1
@cache_page(timeout=60 * 60 * 12)
def scence_geographic(request):
    pid = request.GET.get("pid")
    flag = request.GET.get("flag")  # 避免同pid冲突
    if not pid:
        return JsonResponse({"status": 0})
    try:
        pid = int(pid)
        flag = int(flag)
    except Exception:
        return JsonResponse({"status": 0})
    with connection.cursor() as cursor:
        cursor.execute("select longitude,latitude from digitalsmart.geographic where pid=%s and flag=%s", [pid, flag])
        rows = cursor.fetchall()

    return JsonResponse({"bounds": rows})


