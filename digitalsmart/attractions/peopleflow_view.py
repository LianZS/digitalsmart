from django.core.cache import cache
from django.http import JsonResponse
from django.db import connection

from django.core.exceptions import ObjectDoesNotExist
from .models import TableManager
from attractions.tool.predict import Predict, predict_func
from attractions.tool.select_historyflown import get_historyscenceflow_class
from .tool.processing_response import access_control_allow_origin, cache_response
from .tool.processing_request import get_request_args, check_request_method, RequestMethod, conversion_args_type

"""
人流数据
"""


class ScenicPeopleFlowDetail(object):

    @staticmethod
    def get_scenicflow_data_queryset(request):
        """
        获取景区客流量(暂时不公开type_flag =1 的数据源的景区数据)--链接格式：
        http://127.0.0.1:8000/attractions/api/getLocation_pn_percent_new?pid=6&date_begin=20190921&date_end=20190723&
        predict=true&sub_domain=
        :param request:
        :return:response = {"data": result, "future_time": predict_data['future_time'],
                        "future_data": predict_data['future_data']}
        """

        err_msg = {"status": 0, "code": 0, "message": "参数有误"}
        if check_request_method(request) == RequestMethod.GET:

            type_flag = 0
            pid, date_begin, date_end, predict, sub_domain = get_request_args(request, 'pid', 'date_begin', 'date_end',
                                                                              'predict', 'sub_domain')
            pid, date_begin, date_end = conversion_args_type({pid: int, date_begin: int, date_end: int})

            if not (pid and date_begin and date_end and predict):
                response = err_msg
            else:
                date_interval = date_end - date_begin
                if date_interval > 1:
                    return JsonResponse(err_msg)

                #  缓存key
                key = "scence:{0}:{1}".format(pid, type_flag)
                # 获取缓存数据
                response = cache.get(key)
                if response is None:  # 没有缓存数据

                    # # 获取该景区数据位于哪张表
                    table_id = TableManager.objects.filter(pid=pid, flag=0).values("table_id")[0]["table_id"]
                    scenic_people_detail_queryset = get_historyscenceflow_class(table_id).objects.filter(
                        ddate=date_begin).values(
                        'ttime',
                        'num')
                    temp_result = list()
                    for item in scenic_people_detail_queryset:
                        temp_result.append([item['ttime'], item['num']])
                    scenic_people_detail_queryset = temp_result
                    # 按时间排序
                    scenic_people_detail_queryset = sorted(scenic_people_detail_queryset, key=lambda x: str(x[0]))
                    # 预测客流量数据
                    if predict_func(predict) == Predict.PREDICT:
                        predict_data = Predict().predict(pid, table_id)
                    else:
                        predict_data = {'future_time': None, 'future_data': None}
                    response = {"data": scenic_people_detail_queryset, "future_time": predict_data['future_time'],
                                "future_data": predict_data['future_data']}
                    cache_response(key, response, 60 * 50,len(scenic_people_detail_queryset))
        else:
            response = err_msg
        jsonreponse = access_control_allow_origin(response)

        return jsonreponse

    @staticmethod
    def get_scenicflow_trend_queryset(
            request):
        """
        获取景区人流趋势--链接格式：
        http://127.0.0.1:8000/attractions/api/getLocation_trend_percent_new?&pid=18346&date_begin=20190722&&date_end=20190723
        &predict=true&sub_domain=
        :param request:
        :return: response = {"data": result}

        """
        err_msg = {"status": 0, "code": 0, "message": "参数有误"}
        if check_request_method(request) == RequestMethod.GET:

            pid, date_begin, date_end, predict, sub_domain = get_request_args(request, 'pid', 'date_begin', 'date_end',
                                                                              'predict', 'sub_domain')
            pid, date_begin, date_end = conversion_args_type({pid: int, date_begin: int, date_end: int})
            if not (pid and date_begin and date_end):
                response = err_msg
            else:
                #  缓存key构造规则

                key = "trend:{0}".format(pid)

                response = cache.get(key)
                if response is None:
                    with connection.cursor() as cursor:
                        cursor.execute("select ttime,rate from digitalsmart.scencetrend where pid=%s and ddate=%s",
                                       [pid, date_begin])
                        trend_detail_queryset = cursor.fetchall()

                    trend_detail_queryset = sorted(trend_detail_queryset, key=lambda x: str(x[0]))  # 排序

                    response = {"data": trend_detail_queryset}
                    cache_response(key, response, 60 * 5,len(trend_detail_queryset))
        else:
            response = err_msg
        jsonresponse = access_control_allow_origin(response)
        return jsonresponse

    @staticmethod
    def scence_people_distribution(request):
        """
        获取景区实时客流分布情况--链接格式：
         http://127.0.0.1:8000/attractions/api/getLocation_distribution_rate?pid=4910&type_flag=0&sub_domain=
        :param request:
        :return:{"data": result}

        """
        err_msg = {"status": 0, "code": 0, "message": "参数有误"}
        if check_request_method(request) == RequestMethod.GET:
            pid, type_flag, sub_domain = get_request_args(request, 'pid', 'type_flag', 'sub_domain')
            pid, type_flag = conversion_args_type({pid: int, type_flag: int})

            if not (pid and isinstance(type_flag, int)):
                response = err_msg
            else:
                #  缓存key构造规则
                key = "distribution:{0}".format(pid)
                response = cache.get(key)
                if response is None:

                    try:
                        obj = TableManager.objects.get(pid=pid, flag=type_flag)  # 避免重复冲突
                    except ObjectDoesNotExist:
                        return JsonResponse(err_msg)
                    last_up: int = obj.last_date  # 最近更新时间
                    table_id: int = obj.table_id  # 表位置
                    # 下面之所以不格式化字符串，是预防注入
                    sql = "select lat,lon,num from digitalsmart.peopleposition{0} where  tmp_date=%s".format(
                        table_id)

                    with connection.cursor() as cursor:
                        cursor.execute(sql,
                                       [last_up])
                        rows = cursor.fetchall()
                        distribution_queryset = list()
                        for item in rows:
                            lat = item[0]
                            lon = item[1]
                            num = item[2]
                            distribution_queryset.append({"lat": lat, "lng": lon, "count": num})

                    response = {"data": distribution_queryset}
                    cache_response(key, response, 60 * 5,len(distribution_queryset))

        else:
            response = err_msg
        jsonresponse = access_control_allow_origin(response)
        return jsonresponse
