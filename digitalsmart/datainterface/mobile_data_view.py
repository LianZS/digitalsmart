from internet.models import BrandShare, MobileSystemRate, OperatorRate, NetworkShare
from attractions.tool.processing_response import access_control_allow_origin
from attractions.tool.processing_request import check_request_method, get_request_args, conversion_args_type, \
    RequestMethod


class MobileDataDetail:

    @staticmethod
    def get_public_brand_share_queryset(request):
        """
            获取固定的品牌公开数据
            http://127.0.0.1:8000/interface/api/getBrandShare?token=bGlhbnpvbmdzaGVuZw==

        :param request:
        :return:
        """
        err_msg = {"status": 0, "message": "错误"}

        if check_request_method(request) == RequestMethod.GET:
            token = get_request_args(request, 'token')
            token = conversion_args_type({token: str})
            if token != "bGlhbnpvbmdzaGVuZw==":
                response = err_msg
            else:
                brandshare = BrandShare.objects.filter(pid__flag=1).values("pid__name", "ddate", "rate").order_by(
                    "ddate").iterator()
                response = {"share": list(brandshare)}
        else:
            response = err_msg

        json_response = access_control_allow_origin(response)
        return json_response

    @staticmethod
    def get_mobile_system_rate_queryset(request):
        """
        http://127.0.0.1:8000/interface/api/getMobileSystemShare?token=bGlhbnpvbmdzaGVuZw==
        获取手机系统数据
        :param request:
        :return:
        """

        err_msg = {"status": 0, "message": "错误"}

        if check_request_method(request) == RequestMethod.GET:
            token = get_request_args(request, 'token')
            if token != "bGlhbnpvbmdzaGVuZw==":
                response = err_msg
            else:
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

        else:
            response = err_msg

        json_response = access_control_allow_origin(response)
        return json_response

    @staticmethod
    def get_operator_rate_queryset(request):
        """
        http://127.0.0.1:8000/interface/api/getOperatorShare?token=bGlhbnpvbmdzaGVuZw==
        获取运营商数据
        :param request:
        :return:
        """

        err_msg = {"status": 0, "message": "错误"}

        if check_request_method(request) == RequestMethod.GET:
            token = get_request_args(request, 'token')
            if token != "bGlhbnpvbmdzaGVuZw==":
                response = err_msg
            else:
                operator = OperatorRate.objects.all().values("pid__name", "ddate", "rate").order_by("ddate").iterator()
                response = {
                    "share": list(operator)
                }

        else:
            response = err_msg

        json_response = access_control_allow_origin(response)
        return json_response

    @staticmethod
    def get_network_rate__queryset(request):
        """
        http://127.0.0.1:8000/interface/api/getNetShare?token=bGlhbnpvbmdzaGVuZw==
        获取网络数据
        :param request:
        :return:
        """

        err_msg = {"status": 0, "message": "错误"}

        if check_request_method(request) == RequestMethod.GET:
            token = get_request_args(request, 'token')
            if token != "bGlhbnpvbmdzaGVuZw==":
                response = err_msg
            else:
                network = NetworkShare.objects.all().values("pid__name", "ddate", "rate").order_by("ddate").iterator()
                response = {
                    "share": list(network)
                }


        else:
            response = err_msg

        json_response = access_control_allow_origin(response)
        return json_response
