import datetime
import uuid
from django.core.cache import cache
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from attractions.models import SearchRate, CommentRate, NetComment, ScenceState
from .tool.processing_request import RequestMethod, check_request_method, get_request_args, conversion_args_type

from .tool.processing_response import access_control_allow_origin, cache_response


class CommentDetail(object):

    @staticmethod
    def get_search_heat_queryset(request):
        """
        景区搜索热度---链接格式：
        http://127.0.0.1:8000/attractions/api/getLocation_search_rate?&pid=158&sub_domain=&type_flag=0
        :param request:
        :return:
        """
        err_msg = {"status": 0, "code": 0, "message": "有误"}

        if check_request_method(request) == RequestMethod.GET:
            pid, type_flag = get_request_args(request, 'pid', 'type_flag')
            pid, type_flag = conversion_args_type({pid: int, type_flag: int})

            if not (pid and isinstance(type_flag,int)):
                response = err_msg
            else:
                # 缓存key构造规则--"searchrate"+str(pid * 1111 + flag)
                key = uuid.uuid5(uuid.NAMESPACE_OID, "searchrate" + str(pid * 1111 + type_flag))
                response = cache.get(key)
                if response is None:
                    # 数据从今年出开始
                    year = datetime.datetime.now().year
                    init_date = datetime.datetime(year, 1, 1)
                    begin_date = int(str(init_date.date()).replace("-", ""))
                    rows = SearchRate.objects.filter(pid=pid, tmp_date__gte=begin_date, flag=type_flag).values(
                        "tmp_date",
                        "name",
                        "rate"). \
                        iterator()
                    wechat = list()
                    baidu = list()
                    sougou = list()

                    for item in rows:
                        if item['name'] == 'wechat':
                            wechat.append(item)

                        elif item['name'] == 'sougou':
                            sougou.append(item)
                        else:
                            baidu.append(item)
                    response = {"wechat": wechat, "sougou": sougou, "baidu": baidu}
                    conditions = len(wechat) or len(baidu) or len(sougou)
                    cache_response(key, response, 60 * 60 * 10, conditions)

        else:
            response = err_msg
        jsonreponse = access_control_allow_origin(response)

        return jsonreponse

    @staticmethod
    def get_comment_rate_queryset(request):
        """
        获取评论指数--链接格式 ：
        http://127.0.0.1:8000/attractions/api/getCommentRate?pid=6
        :param request:
        :return:
        """
        err_msg = {"status": 0, "code": 0, "message": "有误"}

        if check_request_method(request) == RequestMethod.GET:

            pid = get_request_args(request, 'pid')
            pid = conversion_args_type({pid: int})
            if not pid:
                return JsonResponse(err_msg)

            key = uuid.uuid5(uuid.NAMESPACE_OID, "comment_rate" + str(pid))
            response = cache.get(key)
            if response is None:
                comment_rate_detail_query = CommentRate.objects.filter(pid=pid).values('pk', "adjectives",
                                                                                       "rate").iterator()
                comment_rate_detail_query = list(comment_rate_detail_query)

                response = {"comment": comment_rate_detail_query}
                cache_response(key, response, 60 * 60 * 10, len(comment_rate_detail_query))
        else:
            response = err_msg
        jsonreponse = access_control_allow_origin(response)
        return jsonreponse

    @staticmethod
    def get_comment_queryset(request):
        """
        获取评论---链接格式http://127.0.0.1:8000/attractions/api/getComment?pid=6
        :param request:
        :return:
        """
        err_msg = {"status": 0, "code": 0, "message": "有误"}

        if check_request_method(request) == RequestMethod.GET:
            pid = get_request_args(request, 'pid')
            pid = conversion_args_type({pid: int})

            if not pid:
                return JsonResponse(err_msg)
            key = uuid.uuid5(uuid.NAMESPACE_OID, "comment" + str(pid))
            response = cache.get(key)
            if response is None:
                comment_detail_query = NetComment.objects.filter(pid=pid).values("pk", "commentuser", "comment",
                                                                                 "commenttime",
                                                                                 "commentlike",
                                                                                 "userphoto").iterator()
                comment_detail_query = list(comment_detail_query)

                response = {"comment": comment_detail_query}
                cache_response(key, response, 60 * 60 * 10, len(comment_detail_query))
        else:
            response = err_msg
        jsonreponse = access_control_allow_origin(response)
        return jsonreponse

    @staticmethod
    def get_scenic_state_queryset(request):
        """
        获取景区状态---链接格式：
        http://127.0.0.1:8000/attractions/api/getState?pid=6
        :param request:
        :return:
        """
        err_msg = {"status": 0, "code": 0, "message": "有误"}

        if check_request_method(request) == RequestMethod.GET:
            pid = get_request_args(request, 'pid')
            pid = conversion_args_type({pid: int})

            if not pid:
                return JsonResponse(err_msg)
            key = uuid.uuid5(uuid.NAMESPACE_OID, "state" + str(pid))

            response = cache.get(key)

            if response is None:
                try:
                    obj = ScenceState.objects.get(pid=pid)
                except ObjectDoesNotExist:
                    return JsonResponse(err_msg)
                response = {"trafficstate": obj.trafficstate, "weatherstate": obj.weatherstate,
                            "coststate": obj.coststate,
                            "environmentstate": obj.environmentstate}
                response = {"state": response}
                cache_response(key, response, 60 * 60 * 10)
        else:
            response = err_msg
        jsonreponse = access_control_allow_origin(response)

        return jsonreponse
