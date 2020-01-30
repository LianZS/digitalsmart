import re

from django.core.exceptions import ObjectDoesNotExist
from attractions.models import TableManager, ScenceManager
from .models import WeatherDB
from datainterface.tasks import NetWorker
from attractions.tool.select_historyflown import get_historyscenceflow_class
from attractions.tool.processing_request import check_request_method, conversion_args_type, get_request_args, \
    RequestMethod

from attractions.tool.processing_response import access_control_allow_origin


class ScenicDataDetail(object):

    @staticmethod
    def interface_get_historytime_scence_queryset(request):
        """
        获取历史某个具体时刻的人流量--链接格式：
         http://127.0.0.1:8000/interface/api/getScenceDataByTime?pid=6&ddate=20170916&ttime=22:00:00&flag=0&token=bGlhbnpvbmdzaGVuZw==
        :param request:
        :return:

        """
        err_msg = {"status": 0, "message": "错误"}

        if check_request_method(request) == RequestMethod.GET:
            pid, ddate, ttime, token, flag = get_request_args(request, 'pid', 'ddate', 'ttime', 'token', 'flag')
            pid, ddate, ttime, token, flag = conversion_args_type(
                {pid: int, ddate: int, ttime: str, token: str, flag: int})
            if token != "bGlhbnpvbmdzaGVuZw==" or not (
                    pid and ddate and re.match("\d{2}:\d{2}:00", ttime) and token and isinstance(flag, int)):
                response = err_msg
            else:
                try:
                    obj = TableManager.objects.get(pid=pid, flag=0)  # 查询目标所在的表位置
                except ObjectDoesNotExist:
                    return access_control_allow_origin({"status": 0, "message": "无目标数据"})

                area = obj.area
                # 查询历史数据
                table_id: int = obj.table_id  # 表地址
                # 下面之所以不格式化字符串，是预防注入
                historyscenceflow = get_historyscenceflow_class(table_id)
                result = historyscenceflow.objects.filter(ddate=ddate, ttime=ttime).values('num')
                num = None
                for item in result:
                    num = item['num']
                response = {"num": num, "pid": pid, "area": area, "date": ddate, "ttime": ttime}
        else:
            response = err_msg
        json_response = access_control_allow_origin(response)
        return json_response

    @staticmethod
    def interface_get_historydate_scence_queryset(request):
        """
        查询某天人流情况---链接格式：
        http://127.0.0.1:8001/interface/api/getScenceDataByDate?pid=6&ddate=20190921&
        flag=0&token=bGlhbnpvbmdzaGVuZw==
        :param request:
        :return:
        """
        err_msg = {"status": 0, "message": "错误"}

        if check_request_method(request) == RequestMethod.GET:
            pid, ddate, token, flag = get_request_args(request, 'pid', 'ddate', 'token', 'flag')
            pid, ddate, token, flag = conversion_args_type(
                {pid: int, ddate: int, token: str, flag: int})
            if token != "bGlhbnpvbmdzaGVuZw==" or not (pid and ddate and isinstance(flag, int)):
                response = err_msg

            else:

                try:
                    obj = TableManager.objects.get(pid=pid, flag=flag)  # 查询目标所在的表位置

                except ObjectDoesNotExist:
                    return access_control_allow_origin({"status": 0, "message": "无目标数据"})

                area = obj.area

                # 查询历史数据
                table_id: int = obj.table_id  # 表 地址
                # 下面之所以不格式化字符串，是预防注入
                historyscenceflow = get_historyscenceflow_class(table_id)
                result = historyscenceflow.objects.filter(ddate=ddate).values('ttime', 'num')
                history_scenic_queryset = list()
                for item in result:
                    ttime = item['ttime']
                    num = item['num']
                    history_scenic_queryset.append([ttime, num])
                response = {"area": area, "pid": pid, "datalist": history_scenic_queryset, "date": ddate}
        else:
            response = err_msg
        json_response = access_control_allow_origin(response)
        return json_response

    @staticmethod
    def interface_get_hisroty_distribution_queryset(request):
        """
        获取历史景区人流分布数据
     http://127.0.0.1:8000/interface/api/getScenceHeatmapDataByTime?pid=6&ddate=20170121&ttime=12:00:00&flag =0&token=bGlhbnpvbmdzaGVuZw==

        :param request:
        :return:
        """
        err_msg = {"status": 0, "message": "错误"}

        if check_request_method(request) == RequestMethod.GET:
            pid, ddate, ttime, token, flag = get_request_args(request, 'pid', 'ddate', 'ttime', 'token', 'flag')
            pid, ddate, ttime, token, flag = conversion_args_type(
                {pid: int, ddate: int, ttime: str, token: str, flag: int})
            if token != "bGlhbnpvbmdzaGVuZw==" or not (
                    pid and ddate and re.match("\d{2}:\d{2}:00", ttime) and isinstance(flag, int)):
                response = err_msg
            else:
                year, month, day = str(ddate)[0:4], str(ddate)[4:6], str(ddate)[6:]
                ddate = '-'.join([year, month, day])
                try:
                    obj = ScenceManager.objects.get(pid=pid, flag=0)  # 检查是否存在
                except ObjectDoesNotExist:
                    return access_control_allow_origin(err_msg)
                area = obj.area
                longitude = obj.longitude  # 中心经度
                latitude = obj.latitude  # 中心维度
                data = NetWorker().get_scence_distribution_data(pid, ddate, ttime)
                if data == {}:
                    return access_control_allow_origin({"status": 0, "message": "本次请求失败，请重试"})
                response = {"pid": pid, "area": area, "data": data, "longitude": longitude, "latitude": latitude,
                            "multiple": 10000}
        else:
            response = err_msg
        json_response = access_control_allow_origin(response)
        return json_response

    @staticmethod
    def interface_get_hisroty_weather(request):
        """
        获取历史天气数据
        :param request:
        :return:
        """
        err_msg = {"status": 0, "message": "错误"}

        if check_request_method(request) == RequestMethod.GET:
            pid, ddate, token = get_request_args(request, 'pid', 'ddate', 'token')
            pid, ddate = conversion_args_type({pid: int, ddate: int})
            if token != "bGlhbnpvbmdzaGVuZw==" or not (pid and ddate):
                response = err_msg
            else:
                result = WeatherDB.objects.filter(pid=pid, ddate=ddate).values("ddate", "weatherstate", "template",
                                                                               "wind").iterator()
                response = {"data": list(result)}
        else:
            response = err_msg
        json_response = access_control_allow_origin(response)
        return json_response
