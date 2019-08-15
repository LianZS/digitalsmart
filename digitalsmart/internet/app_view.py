import datetime
import json
import time
from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .models import AppInfo, SexShare, AgeShare, AppActive, AppProvinceShare, AppLike
from tool.access_control_allow_origin import Access_Control_Allow_Origin


class AppInfoView():
    def get_app_list(self, request):
        name = request.GET.get("app")

        applist = AppInfo.objects.filter(appname__contains=name).values("id", "appname").iterator()
        response = JsonResponse({"applist": list(applist)})
        response = Access_Control_Allow_Origin(response)
        return response

    def get_page_all_data(self, request):
        appanme = request.GET.get("appname")
        appid = request.GET.get("appid")
        sex_result = SexShare.objects.filter(pid=appid).values("ddate", "boy", "girl").iterator()  # 性别分布
        age_result = AgeShare.objects.filter(pid=appid).values("ddate", "under_nineth", "nin_twen", "twe_thir",
                                                               "thir_four", "four_fift",
                                                               "over_fift").iterator()  # 年龄分布
        active_result = AppActive.objects.filter(pid=appid).values("ddate", "activenum", "activerate",
                                                                   "base_activerate",
                                                                   "aver_activerate").iterator()  # app活跃度
        area_result = AppProvinceShare.objects.filter(pid=appid).values("ddate", "province", "rate").iterator()  # 省份热度
        like_keyword = AppLike.objects.filter(pid=appid).values("ddate", "keyword", "rate").iterator()  # 应用偏好关键词
        result = {
            "sex": list(sex_result),
            "age": list(age_result),
            "active": list(active_result),
            "area": list(area_result),
            "like": list(like_keyword)
        }
        response = JsonResponse(result)

        response = Access_Control_Allow_Origin(response)
        return response
