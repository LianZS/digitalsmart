from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from tool.access_control_allow_origin import Access_Control_Allow_Origin
from .models import MobileBrand, BrandShare, MobileModel


# Create your views here.
class MobileShare:
    def get_brand_list(self, request):
        #获取品牌数据
        brands = MobileBrand.objects.all().values("id", "name").iterator()
        result = {"brand": list(brands)}
        return self.deal_response(result)

    def get_brand_share(self, request):
        #获取品牌占有率
        pid = request.GET.get("pid")
        brandshare = BrandShare.objects.filter(pid=pid).values("ddate", "rate").iterator()
        result = {"share": list(brandshare)}
        return self.deal_response(result)
    def get_mobile_type(self,request):
        #获取机型数据
        brand_pid = request.GET.get("bpid")
        mobile_type = MobileModel.objects.filter(pid=brand_pid).values("mpid","mmodel").distinct()
        result = {"mobile":list(mobile_type)}
        return self.deal_response(result)

    def get_mobiletype_share(self, request):
        #获取机型占有率
        brand_pid = request.GET.get("bpid")
        mobile_pid = request.GET.get("mpid")
        mobileshare = MobileModel.objects.filter(pid=brand_pid, mpid=mobile_pid).values("mmodel", "ddate",
                                                                                        "rate").iterator()
        result = {"share": list(mobileshare)}
        return self.deal_response(result)

    def deal_response(self, result):
        response = JsonResponse(result)
        response = Access_Control_Allow_Origin(response)
        return response
