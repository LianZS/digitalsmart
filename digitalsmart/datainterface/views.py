import re
import datetime

from django.db import connection
from django.http import JsonResponse
from attractions.models import TableManager, ScenceManager
from .tasks import NetWorker


class ScenceData(object):

    # Create your views here.

    # http://127.0.0.1:8000/interface/api/getScenceDataByTime?pid=6&ddate=20170916&ttime=22:00:00&token=5j1znBVAsnSf5xQyNQyq

    def interface_historytime_scence_data(self, request):
        """
        获取历史某个具体时刻的人流量
        :param request:
        :return:
        """
        pid, ddate, ttime, token = self.check_paramer(request)
        if not (pid and ddate and ttime and token):
            return JsonResponse({"status": 0, "message": "参数格式有误"})
        today: int = int(str(datetime.datetime.today().date()).replace("-", ""))

        try:
            obj = TableManager.objects.get(pid=pid, flag=0)  # 查询目标所在的表位置

        except Exception:
            return JsonResponse({"status": 0, "message": "error"})

        area = obj.area
        if ddate == today:  # 查询今天的数据的话
            return self.interface_todaytime_scence_data(pid, ddate, ttime, area)
        # 查询历史数据
        table_id: int = obj.table_id  # 表为止
        # 下面之所以不格式化字符串，是预防注入
        sql = None
        if table_id == 0:
            sql = "select num from digitalsmart.historyscenceflow0 where pid=%s and ddate=%s and ttime=%s"
        elif table_id == 1:
            sql = "select num from digitalsmart.historyscenceflow1 where pid=%s and ddate=%s and ttime=%s"
        elif table_id == 2:
            sql = "select num from digitalsmart.historyscenceflow2 where pid=%s and ddate=%s and ttime=%s"
        elif table_id == 3:
            sql = "select num from digitalsmart.historyscenceflow3 where pid=%s and ddate=%s and ttime=%s"
        elif table_id == 4:
            sql = "select num from digitalsmart.historyscenceflow4 where pid=%s and ddate=%s and ttime=%s"
        elif table_id == 5:
            sql = "select num from digitalsmart.historyscenceflow5 where pid=%s and ddate=%s and ttime=%s"
        elif table_id == 6:
            sql = "select num from digitalsmart.historyscenceflow6 where pid=%s and ddate=%s and ttime=%s"
        elif table_id == 7:
            sql = "select num from digitalsmart.historyscenceflow7 where pid=%s and ddate=%s and ttime=%s"
        elif table_id == 8:
            sql = "select num from digitalsmart.historyscenceflow8 where pid=%s and ddate=%s and ttime=%s"
        elif table_id == 9:
            sql = "select num from digitalsmart.historyscenceflow9 where pid=%s and ddate=%s and ttime=%s "

        with connection.cursor() as cursor:
            cursor.execute(sql,
                           [pid, ddate, ttime])
            try:
                num = cursor.fetchone()[0]
            except Exception:
                num = None

        return JsonResponse({"num": num, "pid": pid, "area": area})

    @staticmethod
    def interface_todaytime_scence_data(pid, ddate, ttime, area):
        """
        查询今天人流数据
        :param pid:
        :param ddate:
        :param ttime:
        :param area:
        :return:
        """
        with connection.cursor() as cursor:
            sql = "select num from digitalsmart.scenceflow where pid=%s and ddate=%s and ttime=%s  "
            cursor.execute(sql,
                           [pid, ddate, ttime])
            try:
                num = cursor.fetchone()[0]
            except Exception:
                num = None

        return JsonResponse({"num": num, "pid": pid, "area": area})

    # http://127.0.0.1:8000/interface/api/getScenceDataByDate?pid=6&ddate=20170121&token=5j1znBVAsnSf5xQyNQyq
    def interface_historydate_scence_data(self, request):
        """
        查询某天人流情况
        :param request:
        :return:
        """
        pid, ddate, ttime, token = self.check_paramer(request, 0)  # ttime默认为None
        if not (pid and ddate and token):
            return JsonResponse({"status": 0, "message": "参数格式有误"})

        today: int = int(str(datetime.datetime.today().date()).replace("-", ""))

        try:
            obj = TableManager.objects.get(pid=pid, flag=0)  # 查询目标所在的表位置

        except Exception:
            return JsonResponse({"status": 0, "message": "error"})

        area = obj.area
        if ddate == today:  # 查询今天的数据的话
            return self.interface_todaydate_scence_data(pid, ddate, area)
        # 查询历史数据
        table_id: int = obj.table_id  # 表为止
        # 下面之所以不格式化字符串，是预防注入
        sql = None
        if table_id == 0:
            sql = "select ttime,num from digitalsmart.historyscenceflow0 where pid=%s and ddate=%s "
        elif table_id == 1:
            sql = "select ttime,num from digitalsmart.historyscenceflow1 where pid=%s and ddate=%s"
        elif table_id == 2:
            sql = "select ttime,num from digitalsmart.historyscenceflow2 where pid=%s and ddate=%s "
        elif table_id == 3:
            sql = "select ttime,num from digitalsmart.historyscenceflow3 where pid=%s and ddate=%s "
        elif table_id == 4:
            sql = "select ttime,num from digitalsmart.historyscenceflow4 where pid=%s and ddate=%s "
        elif table_id == 5:
            sql = "select ttime,num from digitalsmart.historyscenceflow5 where pid=%s and ddate=%s "
        elif table_id == 6:
            sql = "select ttime,num from digitalsmart.historyscenceflow6 where pid=%s and ddate=%s "
        elif table_id == 7:
            sql = "select ttime,num from digitalsmart.historyscenceflow7 where pid=%s and ddate=%s "
        elif table_id == 8:
            sql = "select ttime,num from digitalsmart.historyscenceflow8 where pid=%s and ddate=%s "
        elif table_id == 9:
            sql = "select ttime,num from digitalsmart.historyscenceflow9 where pid=%s and ddate=%s "
        with connection.cursor() as cursor:
            cursor.execute(sql,
                           [pid, ddate])
            rows = cursor.fetchall()
            return JsonResponse({"area": area, "pid": pid, "datalist": rows})

    @staticmethod
    def interface_todaydate_scence_data(pid, ddate, area):
        with connection.cursor() as cursor:
            sql = "select ttime,num from digitalsmart.scenceflow where pid=%s and ddate=%s  "
            cursor.execute(sql, [pid, ddate])
            rows = cursor.fetchall()
            return JsonResponse({"num": rows, "pid": pid, "area": area})

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

    # http://127.0.0.1:8000/interface/api/getScenceHeatmapDataByTime?pid=6&ddate=20170121&ttime=12:00:00&token=5j1znBVAsnSf5xQyNQyq
    def interface_hisroty_scence_distribution_data(self, request):
        """
        获取历史景区人流分布数据
        :param request:
        :return:
        """
        pid, ddate, ttime, token = self.check_paramer(request)
        year, month, day = str(ddate)[0:4], str(ddate)[4:6], str(ddate)[6:]
        ddate = '-'.join([year, month, day])

        try:
            obj = ScenceManager.objects.get(pid=pid, flag=0)  # 检查是否存在
        except Exception:
            return JsonResponse({"status": 0, "message": "error"})
        area = obj.area

        longitude = obj.longitude  # 中心经度
        latitude = obj.latitude  # 中心维度
        data = NetWorker().get_scence_distribution_data(pid, ddate, ttime)

        response = {"pid": pid, "area": area, "data": data, "longitude": longitude, "latitude": latitude,
                    "multiple": 10000}
        return JsonResponse(response)
    