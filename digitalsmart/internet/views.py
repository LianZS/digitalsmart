from django.shortcuts import render
from django.db.models import Q

from django.http import JsonResponse, HttpResponse
from tool.access_control_allow_origin import Access_Control_Allow_Origin
from .models import MobileBrand, BrandShare, MobileModel, MobileSystemRate


# Create your views here.
class MobileShare:
    def get_brand_list(self, request):
        # 获取品牌数据
        brands = MobileBrand.objects.filter(flag=1).values("id", "name").iterator()
        result = {"brand": list(brands)}
        return self.deal_response(result)

    def get_brand_share(self, request):
        # 获取某品牌占有率
        pid = request.GET.get("pid")
        brandshare = BrandShare.objects.filter(pid=pid).values("ddate", "rate").iterator()
        result = {"share": list(brandshare)}
        return self.deal_response(result)

    def get_public_brand_share(self, reuqest):
        # 获取固定的公开数据
        brandshare = BrandShare.objects.filter(pid__flag=1).values("pid__name", "ddate", "rate").order_by(
            "ddate").iterator()
        result = {"share": list(brandshare)}
        return self.deal_response(result)

    def get_mobile_type(self, request):
        # 获取机型数据
        brand_pid = request.GET.get("bpid")
        mobile_type = MobileModel.objects.filter(pid=brand_pid).values("mpid", "mmodel").distinct()
        result = {"mobile": list(mobile_type)}
        return self.deal_response(result)

    def get_mobiletype_share(self, request):
        # 获取某机型占有率
        brand_pid = request.GET.get("bpid")
        mobile_pid = request.GET.get("mpid")
        mobileshare = MobileModel.objects.filter(pid=brand_pid, mpid=mobile_pid).values("mmodel", "ddate",
                                                                                        "rate").iterator()
        result = {"share": list(mobileshare)}
        return self.deal_response(result)

    def get_mobile_system_rate(self, request):
        android = MobileSystemRate.objects.filter(pid__category="安卓").values("ddate", "rate").iterator()
        apple = MobileSystemRate.objects.filter(pid__category="苹果").values("ddate", "rate").iterator()
        result = {
            "android": list(android),
            "apple": list(apple)
        }
        return self.deal_response(result)

    def deal_response(self, result):
        response = JsonResponse(result)
        response = Access_Control_Allow_Origin(response)
        return response
