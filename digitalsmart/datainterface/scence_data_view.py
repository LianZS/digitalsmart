import re
import datetime

from django.db import connection
from django.http import JsonResponse

from attractions.models import TableManager, ScenceManager
from .models import WeatherDB
from datainterface.tasks import NetWorker
from attractions.model_choice import ModelChoice


class ScenceData(object):

    # Create your views here.

    def interface_historytime_scence_data(self, request):
        """
        获取历史某个具体时刻的人流量--链接格式：
         http://127.0.0.1:8000/interface/api/getScenceDataByTime?pid=6&ddate=20170916&
         ttime=22:00:00&flag=0&token=bGlhbnpvbmdzaGVuZw==
        :param request:
        :return:

        """
        flag = request.GET.get("flag")

        pid, ddate, ttime, token = self.check_paramer(request)
        if token != "bGlhbnpvbmdzaGVuZw==":
            return JsonResponse({"status": 0, "message": "appkey错误"})
        if not (pid and ddate and ttime and token and flag):
            return JsonResponse({"status": 0, "message": "参数格式有误"})

        try:
            obj = TableManager.objects.get(pid=pid, flag=0)  # 查询目标所在的表位置

        except Exception:
            return JsonResponse({"status": 0, "message": "无目标数据"})

        area = obj.area
        # 查询历史数据
        table_id: int = obj.table_id  # 表为止
        # 下面之所以不格式化字符串，是预防注入
        historyscenceflow = ModelChoice.historyscenceflow(table_id)
        result = historyscenceflow.objects.filter(ddate=ddate, ttime=ttime).values('num')
        num = None
        for item in result:
            num = item['num']

        return JsonResponse({"num": num, "pid": pid, "area": area, "date": ddate, "ttime": ttime})

    def interface_historydate_scence_data(self, request):
        """
        查询某天人流情况---链接格式：
        http://127.0.0.1:8001/interface/api/getScenceDataByDate?pid=6&ddate=20190921&
        flag=0&token=bGlhbnpvbmdzaGVuZw==
        :param request:
        :return:
        """
        flag = request.GET.get("flag")

        pid, ddate, ttime, token = self.check_paramer(request, 0)  # ttime默认为None
        if token != "bGlhbnpvbmdzaGVuZw==":
            return JsonResponse({"status": 0, "message": "appkey错误"})
        if not (pid and ddate and token and flag):
            return JsonResponse({"status": 0, "message": "参数格式有误"})

        today: int = int(str(datetime.datetime.today().date()).replace("-", ""))

        try:
            obj = TableManager.objects.get(pid=pid, flag=0)  # 查询目标所在的表位置

        except Exception:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})

        area = obj.area

        # 查询历史数据
        table_id: int = obj.table_id  # 表 地址
        # 下面之所以不格式化字符串，是预防注入
        historyscenceflow = ModelChoice.historyscenceflow(table_id)
        result = historyscenceflow.objects.filter(ddate=ddate).values('ttime', 'num')
        rows = list()
        for item in result:
            ttime = item['ttime']
            num = item['num']
            rows.append([ttime, num])

        return JsonResponse({"area": area, "pid": pid, "datalist": rows, "date": ddate})

    @staticmethod
    def check_paramer(request, flag=1):
        """参数检查
        flag为1时表示要检查ttime格式，0表示不需要
        """
        pid = request.GET.get("pid")
        token: str = request.GET.get("token")  # 密钥
        ddate = request.GET.get("ddate")  # 日期
        ttime: str = request.GET.get("ttime")  # 时间

        if not (pid and token and ddate):
            return None, None, None, None
        try:
            ddate: int = int(ddate)
            pid: int = int(pid)
            if flag:

                match_result = re.match("\d{2}:\d{2}:00", ttime)
                if not match_result:
                    return None, None, None, None

        except Exception:
            return None, None, None, None
        return pid, ddate, ttime, token

    # http://127.0.0.1:8000/interface/api/getScenceHeatmapDataByTime?pid=6&ddate=20170121&ttime=12:00:00&flag =0&token=bGlhbnpvbmdzaGVuZw==
    def interface_hisroty_scence_distribution_data(self, request):
        """
        获取历史景区人流分布数据
        :param request:
        :return:
        """
        flag = request.GET.get("flag")

        pid, ddate, ttime, token = self.check_paramer(request)
        if token != "bGlhbnpvbmdzaGVuZw==":
            return JsonResponse({"status": 0, "message": "appkey错误"})
        year, month, day = str(ddate)[0:4], str(ddate)[4:6], str(ddate)[6:]
        ddate = '-'.join([year, month, day])

        try:
            obj = ScenceManager.objects.get(pid=pid, flag=0)  # 检查是否存在
        except Exception:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        area = obj.area

        longitude = obj.longitude  # 中心经度
        latitude = obj.latitude  # 中心维度
        data = NetWorker().get_scence_distribution_data(pid, ddate, ttime)
        if data == {}:
            return JsonResponse({"status": 0, "message": "本次请求失败，请重试"})
        response = {"pid": pid, "area": area, "data": data, "longitude": longitude, "latitude": latitude,
                    "multiple": 10000}
        return JsonResponse(response)

    def interface_hisroty_weather(self, request):
        pid = request.GET.get("pid")
        ddate = request.GET.get("ddate")
        if not (pid and ddate):
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        try:
            pid = int(pid)
            ddate = int(ddate)
        except Exception:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        result = WeatherDB.objects.filter(pid=pid, ddate=ddate).values("ddate", "weatherstate", "template",
                                                                       "wind").iterator()
        response = {"data": list(result)}
        return JsonResponse(response)
