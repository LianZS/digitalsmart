import uuid
from django.core.cache import cache
from django.http import JsonResponse
from attractions.tool.access_control_allow_origin import Access_Control_Allow_Origin
from .models import MobileBrand, BrandShare, MobileModel, MobileSystemRate, OperatorRate, NetworkShare


class MobileShare:
    # http://127.0.0.1:8000/internet/api/mobile/brand 获取品牌列表
    def get_brand_list(self, request):
        # 获取品牌数据
        # 缓存key
        key = "brandlist"
        key = uuid.uuid5(uuid.NAMESPACE_OID, key)
        response = cache.get(key)
        if response is None:
            brands = MobileBrand.objects.filter(flag=1).values("id", "name").iterator()
            response = {"brand": list(brands)}
            cache.set(key, response, 60 * 60 * 10)
        return self.deal_response(response)

    # http://127.0.0.1:8000/internet/api/mobile/allBrandShare?pid=22
    def get_brand_share(self, request):
        # 获取某品牌占有率
        pid = request.GET.get("pid")
        if pid is None:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        try:
            pid = int(pid)
        except ValueError:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        # 缓存key
        key = "brand_share" + str(pid)
        key = uuid.uuid5(uuid.NAMESPACE_OID, key)
        response = cache.get(key)
        if response is None:
            brandshare = BrandShare.objects.filter(pid=pid).values("ddate", "rate").iterator()
            response = {"share": list(brandshare)}
            cache.set(key, response, 60 * 10)
        return self.deal_response(response)

    # http://127.0.0.1:8000/internet/api/mobile/brandShare
    def get_public_brand_share(self, reuqest):
        # 获取固定的公开数据
        key = "public_brand_share"
        key = uuid.uuid5(uuid.NAMESPACE_OID, key)
        response = cache.get(key)
        if response is None:
            brandshare = BrandShare.objects.filter(pid__flag=1).values("pid__name", "ddate", "rate").order_by(
                "ddate").iterator()
            response = {"share": list(brandshare)}
            cache.set(key, response, 60 * 60 * 10)
        return self.deal_response(response)

    # http://127.0.0.1:8000/internet/api/mobile/mobileType?bpid=39
    def get_mobile_type(self, request):
        # 获取机型数据
        # 品牌标识
        brand_pid = request.GET.get("bpid")
        if brand_pid is None:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        try:
            pid = int(brand_pid)
        except ValueError:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        # 缓存key
        key = "mobiletype" + str(pid)
        key = uuid.uuid5(uuid.NAMESPACE_OID, key)
        response = cache.get(key)
        if response is None:
            mobile_type = MobileModel.objects.filter(pid=brand_pid).values("mpid", "mmodel").distinct()
            response = {"mobile": list(mobile_type)}
            cache.set(key, response, 60 * 60 * 5)
        return self.deal_response(response)

    # http://127.0.0.1:8000/internet/api/mobile/mobileShare?bpid=38&mpid=201
    def get_mobiletype_share(self, request):
        # 获取某机型占有率
        brand_pid = request.GET.get("bpid")  # 品牌标志
        mobile_pid = request.GET.get("mpid")  # 机型标识
        if not (brand_pid and mobile_pid):
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        try:
            brand_pid = int(brand_pid)
            mobile_pid = int(mobile_pid)
        except ValueError:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        key = "mobiletype_share" + str(brand_pid * 1111) + str(mobile_pid)
        key = uuid.uuid5(uuid.NAMESPACE_OID, key)
        response = cache.get(key)
        if response is None:
            mobileshare = MobileModel.objects.filter(pid=brand_pid, mpid=mobile_pid).values("mmodel", "ddate",
                                                                                            "rate").iterator()
            response = {"share": list(mobileshare)}
            cache.set(key, response, 60 * 60 * 5)

        return self.deal_response(response)

    # http://127.0.0.1:8000/internet/api/mobile/systemShare
    def get_mobile_system_rate(self, request):
        # 获取手机系统数据
        key = "mobile_system_rate"
        key = uuid.uuid5(uuid.NAMESPACE_OID, key)
        response = cache.get(key)
        if response is None:
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
            cache.set(key, response, 60 * 60 * 5)

        return self.deal_response(response)

    # http://127.0.0.1:8000/internet/api/mobile/operatorShare
    def get_operator_rate(self, request):
        # 获取运营商数据
        key = "mobile_system_rate"
        key = uuid.uuid5(uuid.NAMESPACE_OID, key)
        response = cache.get(key)
        if response is None:
            operator = OperatorRate.objects.all().values("pid__name", "ddate", "rate").order_by("ddate").iterator()
            response = {
                "share": list(operator)
            }
            cache.set(key, response, 60 * 60 * 5)

        return self.deal_response(response)

    # http://127.0.0.1:8000/internet/api/mobile/networkShare
    def get_network_rate(self, request):
        # 获取网络数据
        key = "network_rate"
        key = uuid.uuid5(uuid.NAMESPACE_OID, key)
        response = cache.get(key)
        if response is None:
            network = NetworkShare.objects.all().values("pid__name", "ddate", "rate").order_by("ddate").iterator()
            response = {
                "share": list(network)
            }
            cache.set(key, response, 60 * 60 * 5)

        return self.deal_response(response)

    def deal_response(self, response):
        response = Access_Control_Allow_Origin(response)
        return response
