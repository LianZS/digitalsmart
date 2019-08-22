import re
from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse

from attractions.models import TableManager


# Create your views here.
# http://127.0.0.1:8000/interface/api/getScenceDataByTime?pid=6&ddate=20170916&ttime=22:00:00&token=5j1znBVAsnSf5xQyNQyq
def interface_scence_data(request):
    """
    获取某个具体时刻的人流量
    :param request:
    :return:
    """
    pid = request.GET.get("pid")
    token = request.GET.get("token")  # 密钥
    ddate = request.GET.get("ddate")  # 日期
    ttime = request.GET.get("ttime")  # 时间

    if not (pid and token and ddate):
        return JsonResponse({""
                             "status": 0, "message": "参数缺失"})
    try:
        ddate: int = int(ddate)
        match_result = re.match("\d{2}:\d{2}:00", ttime)
        if not match_result:
            JsonResponse({"status": 0, "message": "时间参数格式有误"})

    except Exception as  e:
        print(e)
        return JsonResponse({"status": 0, "message": "日期参数格式有误"})

    obj = TableManager.objects.get(pid=pid, flag=0)  # 查询目标所在的表位置

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

    return JsonResponse({"1": num})
