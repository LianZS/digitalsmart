import uuid
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.http import JsonResponse
from attractions.tool.access_control_allow_origin import Access_Control_Allow_Origin
from attractions.models import ScenceManager
from django.db import connection


class AreaInfo():
    # 景区地理基本信息
    # http://127.0.0.1:8000/attractions/api/getCitysByProvince?province=广东省
    @staticmethod
    def citylist(request):
        # 城市列表
        # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:  # 反爬虫
        #
        #     return JsonResponse({"status": 0})
        province = request.GET.get('province')  # 广东省
        if province is None:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        response = cache.get(province)
        if response is None:
            result = ScenceManager.objects.filter(province=province).values("loaction", "citypid").distinct()
            response = {"province": province, "city": list(result)}
            cache.set(province, response, 60 * 60 * 10)
        # 站点跨域请求的问题
        return AreaInfo.deal_response(response)

    ## http://127.0.0.1:8000/attractions/api/getRegionsByCity?province=广东省&location=深圳市&citypid=340
    @staticmethod
    def scencelist(request):
        # 景区数据---flag=1的景点暂时不公开
        # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:  # 反爬虫
        #     return JsonResponse({"status": 0})
        province = request.GET.get("province")
        city = request.GET.get("location")  # 深圳市
        citypid = request.GET.get("citypid")  # 123
        if not len(city) or not len(province) or not citypid:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        # 作为城市唯一缓存key
        key = uuid.uuid5(uuid.NAMESPACE_OID, province + city + citypid)
        response = cache.get(key)

        if response is None:
            result = ScenceManager.objects.filter(province=province, loaction=city, citypid=citypid, flag=0).values(
                "area",
                "pid",
                "longitude",
                "latitude", "type_flag")
            response = {"city": city, "area": list(result)}
            cache.set(key, response, 60 * 60 * 10)
        # 站点跨域请求的问题
        return AreaInfo.deal_response(response)

    # http://127.0.0.1:8000/attractions/api/getLocation_geographic_bounds?pid=1398&type_flag=1
    @staticmethod
    def scence_geographic(request):
        # 景区地理数据
        # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:  # 反爬虫
        #     return JsonResponse({"status": 0})
        pid = request.GET.get("pid")
        type_flag = request.GET.get("type_flag")  # 避免同pid冲突
        if not pid:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        try:
            pid = int(pid)
            flag = int(type_flag)
        except Exception:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        # 生产该景点的唯一key
        key = uuid.uuid5(uuid.NAMESPACE_OID, str(pid * 1111 + flag))
        response = cache.get(key)
        if response is None:
            with connection.cursor() as cursor:
                cursor.execute("select longitude,latitude from digitalsmart.geographic where pid=%s and flag=%s",
                               [pid, flag])
                rows = cursor.fetchall()

            response = {"bounds": rows}
            cache.set(key, response, 60 * 60 * 10)
        return AreaInfo.deal_response(response)

    # http://127.0.0.1:8000/attractions/api/getScenceInfo
    @staticmethod
    def scence_map(request):
        # 获取景区数据,用于绘制地图
        # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:  # 反爬虫
        #     return JsonResponse({"status": 0})
        key = "scence_map"
        response = cache.get(key)

        if response is None:
            scence_info = ScenceManager.objects.filter(flag=0).values("area", "longitude", "latitude", "province",
                                                                      "loaction").iterator()
            response = {"data": list(scence_info)}
            cache.set(key, response,60*60*10)
        return AreaInfo.deal_response(response)

    @staticmethod
    def deal_response(response):
        response = JsonResponse(response)

        response = Access_Control_Allow_Origin(response)

        return response
