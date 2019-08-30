import uuid
from django.core.cache import cache
from django.http import JsonResponse
from internet.models import MobileBrand, BrandShare, MobileModel, MobileSystemRate, OperatorRate, NetworkShare


class MobileData:

    # http://127.0.0.1:8000/interface/api/getBrandShare?token=bGlhbnpvbmdzaGVuZw==
    def get_public_brand_share(self, request):
        # 获取固定的公开数据
        token = request.GET.get("token")
        if token != "bGlhbnpvbmdzaGVuZw==":
            return JsonResponse({"status": 0, "message": "appkey错误"})
        brandshare = BrandShare.objects.filter(pid__flag=1).values("pid__name", "ddate", "rate").order_by(
            "ddate").iterator()
        response = {"share": list(brandshare)}
        return JsonResponse(response)

    # http://127.0.0.1:8000/interface/api/getMobileSystemShare?token=bGlhbnpvbmdzaGVuZw==
    def get_mobile_system_rate(self, request):
        # 获取手机系统数据
        token = request.GET.get("token")
        if token != "bGlhbnpvbmdzaGVuZw==":
            return JsonResponse({"status": 0, "message": "appkey错误"})
        android = MobileSystemRate.objects.filter(pid__category="安卓").values("pid__version", "ddate",
                                                                             "rate").order_by(
            "ddate").iterator()
        apple = MobileSystemRate.objects.filter(pid__category="苹果").values("pid__version", "ddate",
                                                                           "rate").order_by(
            "ddate").iterator()
        response = {
            "android": list(android),
            "apple": list(apple)
        }

        return JsonResponse(response)

    # http://127.0.0.1:8000/interface/api/getOperatorShare?token=bGlhbnpvbmdzaGVuZw==
    def get_operator_rate(self, request):
        # 获取运营商数据
        token = request.GET.get("token")
        if token != "bGlhbnpvbmdzaGVuZw==":
            return JsonResponse({"status": 0, "message": "appkey错误"})
        operator = OperatorRate.objects.all().values("pid__name", "ddate", "rate").order_by("ddate").iterator()
        response = {
            "share": list(operator)
        }

        return JsonResponse(response)

    # http://127.0.0.1:8000/interface/api/getNetShare?token=bGlhbnpvbmdzaGVuZw==
    def get_network_rate(self, request):
        # 获取网络数据
        token = request.GET.get("token")
        if token != "bGlhbnpvbmdzaGVuZw==":
            return JsonResponse({"status": 0, "message": "appkey错误"})
        network = NetworkShare.objects.all().values("pid__name", "ddate", "rate").order_by("ddate").iterator()
        response = {
            "share": list(network)
        }

        return JsonResponse(response)
