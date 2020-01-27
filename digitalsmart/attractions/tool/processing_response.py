from django.http import JsonResponse
from django.core.cache import cache


def access_control_allow_origin(response: dict) -> JsonResponse:
    """
    解决异域请求返回数据异常
    :param response: 请求内容，
    :return:
    """
    response = JsonResponse(response)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"

    return response


def cache_response(key, content, cache_time, conditions=1):
    """

    :param key: 缓存key
    :param content: 缓存内容
    :param cache_time: 缓存时间
    :param conditions: 缓存条件
    :return:
    """
    if conditions:
        cache.set(key, content, cache_time)
        return True
    return False
