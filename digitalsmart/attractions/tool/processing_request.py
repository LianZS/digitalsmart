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


def get_request_args(request: HttpRequest, *args):
    args_list = list()
    for request_arg in args:
        args_list.append(request.GET.get(request_arg, None))
    if len(args_list) == 1:
        return args_list[0]
    elif len(args_list) == 0:
        return None
    else:
        return args_list
