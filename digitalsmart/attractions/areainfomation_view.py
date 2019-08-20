from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from tool.access_control_allow_origin import Access_Control_Allow_Origin
from attractions.models import ScenceManager
from django.db import connection


class AreaInfo():
    # 景区地理基本信息
    # http://127.0.0.1:8000/attractions/api/getCitysByProvince?province=广东省
    @staticmethod
    @cache_page(timeout=None)  # 永久缓存
    def citylist(request):
        # 城市列表
        # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:  # 反爬虫
        #
        #     return JsonResponse({"status": 0})
        province = request.GET.get('province')  # 广东省
        if not province:
            return JsonResponse({"status": 0})
        result = ScenceManager.objects.filter(province=province).values("loaction", "citypid").distinct()
        response = {"province": province, "city": list(result)}
        # 站点跨域请求的问题
        return AreaInfo.deal_response(response)

    ## http://127.0.0.1:8000/attractions/api/getRegionsByCity?province=广东省&location=深圳市&citypid=340
    @staticmethod
    @cache_page(timeout=None)
    def scencelist(request):
        # 景区数据---flag=1的景点暂时不公开
        # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:  # 反爬虫
        #     return JsonResponse({"status": 0})
        province = request.GET.get("province")
        city = request.GET.get("location")  # 深圳市
        citypid = request.GET.get("citypid")  # 123
        if not len(city) or not len(province) or not citypid:
            return JsonResponse({"status": 0})

        result = ScenceManager.objects.filter(province=province, loaction=city, citypid=citypid, flag=0).values("area",
                                                                                                                "pid",
                                                                                                                'longitude',
                                                                                                                "latitude")
        response = {"city": city, "area": list(result)}
        # 站点跨域请求的问题
        return AreaInfo.deal_response(response)

    # http://127.0.0.1:8000/attractions/api/getLocation_geographic_bounds?pid=1398&flag=1
    @staticmethod
    @cache_page(timeout=60 * 60 * 12)
    def scence_geographic(request):
        # 景区地理数据
        # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:  # 反爬虫
        #     return JsonResponse({"status": 0})
        pid = request.GET.get("pid")
        flag = request.GET.get("flag")  # 避免同pid冲突
        if not pid:
            return JsonResponse({"status": "标识有误"})
        try:
            pid = int(pid)
            flag = int(flag)
        except Exception:
            return JsonResponse({"status": 0})
        with connection.cursor() as cursor:
            cursor.execute("select longitude,latitude from digitalsmart.geographic where pid=%s and flag=%s",
                           [pid, flag])
            rows = cursor.fetchall()
        response = {"bounds": rows}
        return AreaInfo.deal_response(response)

    # http://127.0.0.1:8000/attractions/api/getScenceInfo
    def scence_map(self, request):
        # 获取景区数据,用于绘制地图
        # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:  # 反爬虫
        #     return JsonResponse({"status": 0})
        scence_info = ScenceManager.objects.filter(flag=0).values("area", "longitude", "latitude", "province",
                                                                  "loaction").iterator()
        response = {"data": list(scence_info)}
        return AreaInfo.deal_response(response)

    @staticmethod
    def deal_response(response):
        response = JsonResponse(response)

        response = Access_Control_Allow_Origin(response)

        return response
