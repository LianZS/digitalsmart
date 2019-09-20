import uuid
from django.core.cache import cache
from django.http import JsonResponse
from django.db import connection
from digitalsmart.settings import redis_cache
from .models import TableManager
from attractions.tool.access_control_allow_origin import Access_Control_Allow_Origin
from .predict import Predict

"""
人流数据
"""


class PeopleFlow():

    @staticmethod
    def scenceflow_data(
            request):
        """
        获取景区客流量(暂时不公开type_flag =1 的数据源的景区数据)--链接格式：
        http://127.0.0.1:8000/attractions/api/getLocation_pn_percent_new?pid=2&date_begin=20190722&&date_end=20190723&
        predict=true&sub_domain=
        :param request:
        :return:response = {"data": result, "future_time": predict_data['future_time'],
                        "future_data": predict_data['future_data']}
        """
        # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:  # 反爬虫
        #     return JsonResponse({"status": 0})
        type_flag = 0
        pid = request.GET.get("pid")
        date_begin = request.GET.get("date_begin")
        date_end = request.GET.get("date_end")
        predict = request.GET.get("predict")  # 是否预测,true,false
        sub_domain = request.GET.get('sub_domain')  # 是否为开发者标识

        if not (pid and date_begin and date_end and predict):
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        try:
            pid = int(pid)
            date_begin = int(date_begin)  # 格式为20190722
            date_end = int(date_end)
            inv = date_end - date_begin
            if inv > 1:
                return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})

        except Exception:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        #  缓存key
        key = "scence:{0}:{1}".format(pid, type_flag)
        # 获取缓存数据
        response = cache.get(key)
        if response is None or len(response.keys()) == 0:  # 没有缓存数据
            result = redis_cache.hashget(key=key)  # 先从内存获取数据
            result = list(result)
            if len(result) == 0:  # 内存没有数据，查询数据库
                # 获取该景区数据位于哪张表
                table_id = TableManager.objects.filter(pid=pid, flag=0).values("table_id")[0]["table_id"]
                with connection.cursor() as cursor:
                    # 确定要查询哪张表
                    sql = "select ttime,num from digitalsmart.historyscenceflow{0} where pid= %s and ddate=%s".format(
                        table_id)
                    cursor.execute(sql, [pid, date_begin])
                    result = cursor.fetchall()
            else:  # 数据统一格式
                temp_result = list()
                data = result[0]
                for k in data.keys():
                    v = data[k]
                    temp_result.append([k, v])
                result = temp_result
            # 按时间排序
            result = sorted(result, key=lambda x: str(x[0]))
            # 预测客流量数据
            predict_data = Predict().predict(pid)
            response = {"data": result, "future_time": predict_data['future_time'],
                        "future_data": predict_data['future_data']}
            cache.set(key, response, 60 * 5)

        return PeopleFlow.deal_response(response)

    @staticmethod
    def scenceflow_trend(
            request):
        """
        获取景区人流趋势--链接格式：
        http://127.0.0.1:8000/attractions/api/getLocation_trend_percent_new?&pid=18346&date_begin=20190722&&date_end=20190723
        &predict=true&sub_domain=
        :param request:
        :return: response = {"data": result}

        """
        #
        # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:  # 反爬虫
        #     return JsonResponse({"status": 0})

        pid = request.GET.get("pid")
        date_begin = request.GET.get("date_begin")
        date_end = request.GET.get("date_end")
        predict = request.GET.get("predict")  # 是否预测
        sub_domain = request.GET.get('sub_domain')  # 是否为开发者标识

        if not pid or not date_begin or not date_end or not predict:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        try:
            pid = int(pid)
            date_begin = int(date_begin)
            date_end = int(date_end)
        except Exception:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        #  缓存key构造规则

        key = "trend:{0}".format(pid)

        response = cache.get(key)
        if response is None or len(response.keys()) == 0:
            result = redis_cache.hashget(key=key)
            result = list(result)
            if len(result) == 0:
                with connection.cursor() as cursor:
                    cursor.execute("select ttime,rate from digitalsmart.scencetrend where pid=%s and ddate=%s",
                                   [pid, date_begin])
                    result = cursor.fetchall()
            else:  # 数据统一格式
                temp_result = list()
                data = result[0]
                for k in data.keys():
                    v = data[k]
                    temp_result.append([k, v])
                result = temp_result
            result = sorted(result, key=lambda x: str(x[0]))  # 排序

            response = {"data": result}
            cache.set(key, response, 60 * 6)
        return PeopleFlow.deal_response(response)

    @staticmethod
    def scence_people_distribution(request):
        """
        获取景区实时客流分布情况--链接格式：
        # http://127.0.0.1:8000/attractions/api/getLocation_distribution_rate?pid=4910&type_flag=0&sub_domain=
        :param request:
        :return:{"data": result}

        """
        # 人流分布数据
        # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:  # 反爬虫
        #     return JsonResponse({"status": 0})
        pid = request.GET.get("pid")
        type_flag = request.GET.get("type_flag")
        if not (pid and type_flag):
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        try:
            pid = int(pid)
            type_flag = int(type_flag)
        except Exception:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        sub_domain = request.GET.get('sub_domain')  # 是否为开发者标识
        #  缓存key构造规则

        key = "distribution:{0}".format(pid)

        response = cache.get(key)
        if response is None or len(response.keys()) == 0:
            result = redis_cache.get(key)
            result = list(result)
            if len(result) == 0 or result[0] == None:
                try:
                    obj = TableManager.objects.get(pid=pid, flag=type_flag)  # 避免重复冲突
                except Exception:
                    return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
                last_up: int = obj.last_date  # 最近更新时间
                table_id: int = obj.table_id  # 表位置
                # 下面之所以不格式化字符串，是预防注入
                sql = "select lat,lon,num from digitalsmart.peopleposition{0} where pid=%s and tmp_date=%s".format(
                    table_id)

                with connection.cursor() as cursor:
                    cursor.execute(sql,
                                   [pid, last_up])
                    rows = cursor.fetchall()
                    result = list()
                    for item in rows:
                        lat = item[0]
                        lon = item[1]
                        num = item[2]
                        result.append({"lat": lat, "lng": lon, "count": num})
            else:
                result = result[0]
            response = {"data": result}
            cache.set(key, response, 60 * 5)
        return PeopleFlow.deal_response(response)

    @staticmethod
    def deal_response(response):

        response = Access_Control_Allow_Origin(response)

        return response
