from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from django.db import connection

from .models import TableManager
from attractions.tool.access_control_allow_origin import Access_Control_Allow_Origin

"""
人流数据
"""


class PeopleFlow():

    # http://127.0.0.1:8000/attractions/api/getLocation_pn_percent_new?pid=2&date_begin=20190722&&date_end=20190723&
    # predict=true&sub_domain=
    @staticmethod
    def scenceflow_data(
            request):
        # 景区实时人流
        # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:  # 反爬虫
        #     return JsonResponse({"status": 0})

        pid = request.GET.get("pid")
        date_begin = int(request.GET.get("date_begin"))  # 20190722
        date_end = int(request.GET.get("date_end"))  # 20190723
        predict = request.GET.get("predict")  # 是否预测,true,false
        sub_domain = request.GET.get('sub_domain')  # 是否为开发者标识
        inv = date_end - date_begin
        if inv > 1:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})

        if not (pid and date_begin and date_end and predict):
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        try:
            pid = int(pid)
            date_begin = int(date_begin)
            date_end = int(date_end)
        except Exception:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        #  缓存key构造规则
        key = "flow" + str(pid * 1111 + inv)
        response = cache.get(key)
        if response is None:
            with connection.cursor() as cursor:
                cursor.execute("select ttime,num from digitalsmart.scenceflow "
                               "where pid= %s and ddate=%s ", [pid, date_begin])
                rows = cursor.fetchall()
                result = sorted(rows, key=lambda x: str(x[0]))  # 排序
                response = {"data": result}

            cache.set(key,response,60*5)

        return PeopleFlow.deal_response(response)

    # http://127.0.0.1:8000/attractions/api/getLocation_trend_percent_new?&pid=18346&date_begin=20190722&&date_end=20190723
    # &predict=true&sub_domain=
    @staticmethod
    @cache_page(timeout=60 * 5)
    def scenceflow_trend(
            request):
        # 景区人流趋势
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
        with connection.cursor() as cursor:
            cursor.execute("select ttime,rate from digitalsmart.scencetrend where pid=%s and ddate=%s",
                           [pid, date_begin])
            rows = cursor.fetchall()
            result = sorted(rows, key=lambda x: str(x[0]))  # 排序

        response = {"data": result}
        return PeopleFlow.deal_response(response)

    # http://127.0.0.1:8000/attractions/api/getLocation_distribution_rate?pid=4910&flag=0&sub_domain=
    @staticmethod
    @cache_page(timeout=60 * 5)
    def scence_people_distribution(request):
        # 人流分布数据
        # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:  # 反爬虫
        #     return JsonResponse({"status": 0})
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
                data.append({"lat": lat, "lng": lon, "count": num})
        response = {"data": data}
        return PeopleFlow.deal_response(response)

    @staticmethod
    def deal_response(response):
        response = JsonResponse(response)

        response = Access_Control_Allow_Origin(response)

        return response
