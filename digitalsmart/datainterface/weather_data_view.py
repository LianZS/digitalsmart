from django.db import connection
from django.http import JsonResponse


class WeatherData(object):
    # http://127.0.0.1:8000/interface/api/getWeather?pid=11&ddate=20180901&token=bGlhbnpvbmdzaGVuZw==
    def get_hisroty_day_weather(self, request):
        """
        获取单天历史数据
        :param request:
        :return:
        """
        """
        获取单天历史数据
        :param request:
        :return:
        """
        token = request.GET.get("token")
        if token != "bGlhbnpvbmdzaGVuZw==":
            return JsonResponse({"status": 0, "message": "appkey错误"})
        pid = request.GET.get("pid")
        ddate = request.GET.get("ddate")
        if not (pid and ddate):
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        try:
            pid = int(pid)
            ddate = int(ddate)
        except Exception:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        with connection.cursor() as cursor:
            sql = "select ddate,weatherstate, template,wind from digitalsmart.weatherdb where  pid=%s and ddate=%s"
            cursor.execute(sql, [pid, ddate])
            result = cursor.fetchall()
            response = {"data": list(result)}
            return JsonResponse(response)

    # http://127.0.0.1:8000/interface/api/getMonthWeather?pid=11&year_month=201809&token=bGlhbnpvbmdzaGVuZw==

    def get_hisroty_month_weather(self, request):

        token = request.GET.get("token")
        if token != "bGlhbnpvbmdzaGVuZw==":
            return JsonResponse({"status": 0, "message": "appkey错误"})
        pid = request.GET.get("pid")
        year_month = request.GET.get("year_month")
        if not (pid and year_month):
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        try:
            pid = int(pid)
            year_month = int(year_month)
        except Exception:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        with connection.cursor() as cursor:
            sql = "select ddate,weatherstate, template,wind from digitalsmart.weatherdb where  " \
                  "pid=%s   and ddate between %s  and %s"
            #若要查201801的数据，则需要查ddate在20180101-20180201间断数据
            cursor.execute(sql, [pid, year_month * 100, (year_month + 1) * 100])
            result = cursor.fetchall()
            response = {"data": list(result)}
            return JsonResponse(response)
