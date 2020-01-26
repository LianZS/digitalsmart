from django.http.request import HttpRequest


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
