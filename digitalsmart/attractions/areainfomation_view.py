import uuid
from django.core.cache import cache
from django.http import JsonResponse
from django.http.request import HttpRequest
from attractions.models import ScenceManager
from django.db import connection


def access_control_allow_origin(httpresponse: dict) -> JsonResponse:
    httpresponse = JsonResponse(httpresponse)
    httpresponse["Access-Control-Allow-Origin"] = "*"
    httpresponse["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    httpresponse["Access-Control-Max-Age"] = "1000"
    httpresponse["Access-Control-Allow-Headers"] = "*"

    return httpresponse


class RequestMethod(object):
    GET = 1
    POST = 2


def check_request_method(request: HttpRequest):
    """
    检查request方法
    :param request:HttpRequest对象
    :return:
    """

    if request.method == "GET":
        return RequestMethod.GET
    else:
        return RequestMethod.POST


class AreaInfoDetail(object):

    @staticmethod
    def get_city_queryset(request):
        """
        景区地理基本信息--链接格式：
        http://127.0.0.1:8000/attractions/api/getCitysByProvince?province=广东省
        :param request:
        :return:
        """
        jsonreponse: JsonResponse = None
        if check_request_method(request) == RequestMethod.GET:

            province = request.GET.get('province')  # 广东省
            if province is None:
                jsonreponse = JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
            else:
                response = cache.get(province)
                if response is None:
                    result = ScenceManager.objects.filter(province=province).values("loaction", "citypid").distinct()
                    response = {"province": province, "city": list(result)}
                    cache.set(province, response, 60 * 60 * 10)
                jsonreponse = access_control_allow_origin(response)
        # 站点跨域请求的问题
        return jsonreponse

    @staticmethod
    def get_scenic_queryset(request):
        """
        景区数据---flag=1的景点暂时不公开--链接格式：
        http://127.0.0.1:8000/attractions/api/getRegionsByCity?province=广东省&location=深圳市&citypid=340
        :param request:
        :return:
        """
        jsonreponse: JsonResponse = None
        if check_request_method(request) == RequestMethod.GET:
            province = request.GET.get("province", None)
            city = request.GET.get("location", None)  # 深圳市
            citypid = request.GET.get("citypid", None)  # 123
            if not (province and city and citypid):
                jsonreponse = JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
            # 作为城市唯一缓存key---province + city + citypid
            else:
                key = uuid.uuid5(uuid.NAMESPACE_OID, province + city + citypid)
                response = cache.get(key)
                if response is None:
                    result = ScenceManager.objects.filter(province=province, loaction=city, citypid=citypid,
                                                          flag=0).values(
                        "area",
                        "pid",
                        "longitude",
                        "latitude", "type_flag")
                    response = {"city": city, "area": list(result)}
                    cache.set(key, response, 60 * 60 * 10)
                jsonreponse = access_control_allow_origin(response)

            # 站点跨域请求的问题
        return jsonreponse

    @staticmethod
    def get_scenic_geographic(request):
        """
         景区地理数据--链接格式：
         http://127.0.0.1:8000/attractions/api/getLocation_geographic_bounds?pid=1398&type_flag=1
        :param request:
        :return:
        """
        jsonreponse: JsonResponse = None

        if check_request_method(request) == RequestMethod.GET:

            pid = request.GET.get("pid")
            type_flag = request.GET.get("type_flag")  # 避免同pid冲突
            if not (pid and type_flag):
                jsonreponse = JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
            else:
                try:
                    pid = int(pid)
                    flag = int(type_flag)
                except Exception:
                    jsonreponse = JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
                    return jsonreponse
                # 生产该景点的唯一key
                key = uuid.uuid5(uuid.NAMESPACE_OID, "geographic" + str(pid * 1111 + flag))
                response = cache.get(key)
                if response is None:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "select longitude,latitude from digitalsmart.geographic where pid=%s and flag=%s",
                            [pid, flag])
                        rows = cursor.fetchall()

                    response = {"bounds": rows}
                    cache.set(key, response, 60 * 60 * 10)
                jsonreponse = access_control_allow_origin(response)
        else:
            jsonreponse = JsonResponse({"status": 0, "code": 0, "message": "请求方式有误"})

        return jsonreponse

    @staticmethod
    def get_scenic_map(request):
        """
        获取景区数据,用于绘制地图--链接格式：
        http://127.0.0.1:8000/attractions/api/getScenceInfo
        :param request:
        :return:
        """
        jsonreponse: JsonResponse = None

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
