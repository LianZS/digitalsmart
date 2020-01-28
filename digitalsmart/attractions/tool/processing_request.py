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
    """
    获取request里面的请求参数
    :param request:
    :param args:提取的关键词字符串参数
    :return:
    """
    args_list = list()
    for request_arg in args:
        args_list.append(request.GET.get(request_arg, None))
    if len(args_list) == 1:
        return args_list[0]
    elif len(args_list) == 0:
        return None
    else:
        return args_list


def conversion_args_type(arg_type_map: dict):
    """
    数据类型转换
    :param arg_type_map: 参数转换映射表{参数值：转换类型}
    :return:
    """
    args_list = list()

    for arg, arg_type in arg_type_map.items():
        try:
            arg = arg_type(arg)
            args_list.append(arg)
        except ValueError as e:
            print("参数 %s 转换类型有误" % arg, e)
            args_list.append(False)

    if len(args_list) == 1:
        return args_list[0]
    elif len(args_list) == 0:
        return False
    else:
        return args_list
