import uuid
from django.core.cache import cache
from django.http import JsonResponse

from attractions.models import ScenceManager
from django.db import connection
from .tool.processing_request import RequestMethod, check_request_method, get_request_args, conversion_args_type
from .tool.processing_response import access_control_allow_origin, cache_response


class AreaInfoDetail(object):

    @staticmethod
    def get_city_queryset(request):

        """
        获取省份下所有城市列表
        景区地理基本信息--链接格式：
        http://127.0.0.1:8000/attractions/api/getCitysByProvince?province=广东省
        :param request:
        :return:
        """
        jsonreponse: JsonResponse = None
        err_msg = {"status": 0, "code": 0, "message": "参数有误"}
        if check_request_method(request) == RequestMethod.GET:

            province = get_request_args(request, 'province')
            province = conversion_args_type({province: str})
            if not province:
                jsonreponse = JsonResponse(err_msg)
            else:
                response = cache.get(province)
                if response is None:
                    city_query = ScenceManager.objects.filter(province=province).values("loaction",
                                                                                        "citypid").distinct().iterator()
                    city_query = list(city_query)

                    response = {"province": province, "city": city_query}
                    cache_response(province, response, 60 * 60 * 10, len(city_query))

                jsonreponse = access_control_allow_origin(response)
        # 站点跨域请求的问题
        return jsonreponse

    @staticmethod
    def get_scenic_queryset(request):
        """
        获取城市下所有地区列表
        景区数据---flag=1的景点暂时不公开--链接格式：
        http://127.0.0.1:8000/attractions/api/getRegionsByCity?province=广东省&location=深圳市&citypid=340
        :param request:
        :return:
        """
        jsonreponse: JsonResponse = None
        if check_request_method(request) == RequestMethod.GET:
            province, city, citypid = get_request_args(request, 'province', 'location', 'citypid')
            province, city, citypid = conversion_args_type({province: str, city: str, citypid: int})
            if not (province and city and citypid):
                jsonreponse = JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
            # 作为城市唯一缓存key---province + city + citypid
            else:

                key = uuid.uuid5(uuid.NAMESPACE_OID, province + city + str(citypid))
                response = cache.get(key)
                if response is None:
                    area_detail_query = ScenceManager.objects.filter(province=province, loaction=city, citypid=citypid,
                                                                     flag=0).values(
                        "area",
                        "pid",
                        "longitude",
                        "latitude", "type_flag")
                    area_detail_query = list(area_detail_query)

                    response = {"city": city, "area": area_detail_query}
                    cache_response(key, response, 60 * 60 * 10, len(area_detail_query))

                jsonreponse = access_control_allow_origin(response)

            # 站点跨域请求的问题
        return jsonreponse

    @staticmethod
    def get_scenic_geographic(request):
        """
        地区经纬度范围
         景区地理数据--链接格式：
         http://127.0.0.1:8000/attractions/api/getLocation_geographic_bounds?pid=1398&type_flag=1
        :param request:
        :return:
        """
        err_msg = {"status": 0, "code": 0, "message": "参数有误"}

        if check_request_method(request) == RequestMethod.GET:

            pid, type_flag = get_request_args(request, 'pid', 'type_flag')
            pid, type_flag = conversion_args_type({pid: int, type_flag: int})
            if not (pid and isinstance(type_flag,int)):
                jsonreponse = JsonResponse(err_msg)
            else:
                # 生产该景点的唯一key
                key = uuid.uuid5(uuid.NAMESPACE_OID, "geographic" + str(pid * 1111 + type_flag))
                response = cache.get(key)
                if response is None:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "select longitude,latitude from digitalsmart.geographic where pid=%s and flag=%s",
                            [pid, type_flag])
                        bounds_detail_query = cursor.fetchall()
                    response = {"bounds": bounds_detail_query}
                    cache_response(key, response, 60 * 60 * 10, len(bounds_detail_query))
                jsonreponse = access_control_allow_origin(response)
        else:
            jsonreponse = JsonResponse(err_msg)

        return jsonreponse

    @staticmethod
    def get_scenic_map(request):
        """
        获取景区数据,用于绘制地图--链接格式：
        http://127.0.0.1:8000/attractions/api/getScenceInfo
        :param request:
        :return:
        """

        if check_request_method(request) == RequestMethod.GET:

            key = "scence_map"
            response = cache.get(key)

            if response is None:
                scence_info = ScenceManager.objects.filter(flag=0).values("area", "longitude", "latitude", "province",
                                                                          "loaction").iterator()
                response = {"data": list(scence_info)}
                cache.set(key, response, 60 * 60 * 10)
            jsonreponse = access_control_allow_origin(response)
        else:
            jsonreponse = JsonResponse({"status": 0, "code": 0, "message": "请求方式有误"})

        return jsonreponse
