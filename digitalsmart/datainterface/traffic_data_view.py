from django.core.exceptions import ObjectDoesNotExist
from traffic.models import CityInfoManager, CityTraffic, RoadTraffic, YearTraffic, RoadInfoManager, AirState
from attractions.tool.processing_response import access_control_allow_origin
from attractions.tool.processing_request import check_request_method, get_request_args, conversion_args_type, \
    RequestMethod


class CityTrafficDetail:

    @staticmethod
    def get_daily_traffic_index_queryset(request):
        """
        http://127.0.0.1:8000/interface/api/getCitydailyIndex?cityCode=340&ddate=20190722&token=bGlhbnpvbmdzaGVuZw==
        日常交通数据
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
                try:
                    cityname = CityInfoManager.objects.get(pid=pid).cityname
                except ObjectDoesNotExist:
                    return access_control_allow_origin(err_msg)
                city_traffic_queryset = CityTraffic.objects.filter(pid=pid, ddate=ddate).values("ttime",
                                                                                                "rate").iterator()
                response = {"data":
                    {
                        "city": cityname,
                        "cityCode": pid,
                        "indexlist": list(city_traffic_queryset),
                        "date": ddate
                    }
                }

        else:
            response = err_msg

        json_response = access_control_allow_origin(response)
        return json_response

    @staticmethod
    def get_road_list_queryset(request):
        """
        http://127.0.0.1:8000/interface/api/getCityRoadlist?cityCode=100&token=bGlhbnpvbmdzaGVuZw==
        道路交通数据
        :param request:
        :return:
        """
        err_msg = {"status": 0, "message": "错误"}

        if check_request_method(request) == RequestMethod.GET:
            city_code, token = get_request_args(request, 'cityCode', 'token')
            city_code = conversion_args_type({city_code: int})
            if token != "bGlhbnpvbmdzaGVuZw==" or not city_code:
                response = err_msg
            else:

                updateSet = RoadInfoManager.objects.filter(citypid=city_code).values("up_date")
                # 找出最早的时间，避免因为挖掘数据时出现了一个差错而导致部分未能正常录入，保证数据能完全展示给用户
                up_date = sorted(updateSet, key=lambda x: x['up_date'])[0]['up_date']
                road_traffic_queryset = RoadTraffic.objects.filter(citypid=city_code, up_date=up_date).values(
                    "roadname",
                    "speed",
                    "direction",
                    "roadpid",
                    "rate")
                response = {

                    "roadlist": list(road_traffic_queryset),
                    "cityCode": city_code

                }
        else:
            response = err_msg

        json_response = access_control_allow_origin(response)
        return json_response

    @staticmethod
    def get_city_year_traffic_queryset(request):
        """
        http://127.0.0.1:8000/interface/api/getCityMonthsTraffic?cityCode=235&token=bGlhbnpvbmdzaGVuZw==
        年度交通数据
        :param request:
        :return:
        """
        err_msg = {"status": 0, "message": "错误"}

        if check_request_method(request) == RequestMethod.GET:
            city_code, token = get_request_args(request, 'cityCode', 'token')
            city_code = conversion_args_type({city_code: int})
            if token != "bGlhbnpvbmdzaGVuZw==" or not city_code:
                response = err_msg
            else:

                try:
                    obj = CityInfoManager.objects.get(pid=city_code)
                    yearpid = obj.yearpid
                    cityname = obj.cityname
                except ObjectDoesNotExist:
                    return access_control_allow_origin(err_msg)

                year_traffic_queryset = YearTraffic.objects.filter(yearpid=yearpid, tmp_date__gt=20190101).values(
                    "tmp_date",
                    "rate").distinct()
                response = {
                    "cityCode": city_code,
                    "city": cityname,

                    "indexSet": list(year_traffic_queryset),

                }
        else:
            response = err_msg

        json_response = access_control_allow_origin(response)
        return json_response

    @staticmethod
    def get_city_air_queryset(request):
        """
         http://127.0.0.1:8000/interface/api/getCityAirState?&cityCode=810000&token=bGlhbnpvbmdzaGVuZw==
         获取城市空气状况
        :param request:
        :return:
        """

        err_msg = {"status": 0, "message": "错误"}

        if check_request_method(request) == RequestMethod.GET:
            city_code, token = get_request_args(request, 'cityCode', 'token')
            city_code = conversion_args_type({city_code: int})
            if token != "bGlhbnpvbmdzaGVuZw==" or not city_code:
                response = err_msg
            else:

                try:
                    obj = AirState.objects.filter(citypid=city_code, flag=True).order_by("-lasttime"). \
                        values("lasttime", 'aqi', 'pm2', 'pm10', 'co', 'no2', 'o3', 'so2')[0]
                except IndexError:
                    return access_control_allow_origin(err_msg)
                lasttime = obj['lasttime']
                aqi = obj['aqi']
                pm2 = obj['pm2']
                pm10 = obj['pm10']
                co = obj['co']
                no2 = obj['no2']
                o3 = obj['o3']
                so2 = obj['so2']
                response = {
                    "cityCode": city_code,
                    "lasttime": lasttime,
                    "data": {
                        "aqi": aqi,
                        "pm2": pm2,
                        "pm10": pm10,
                        "co": co,
                        "no2": no2,
                        "o3": o3,
                        "so2": so2

                    }
                }
        else:
            response = err_msg

        json_response = access_control_allow_origin(response)
        return json_response
