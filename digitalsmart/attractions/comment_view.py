import datetime
import uuid
from django.core.cache import cache
from django.http import JsonResponse

from attractions.tool.access_control_allow_origin import Access_Control_Allow_Origin
from attractions.models import SearchRate, CommentRate, NetComment, ScenceState
from .tool.request_check import RequestMethod, check_request_method


class Comment(object):

    @staticmethod
    def search_heat(request):
        """
        景区搜索热度---链接格式：
        http://127.0.0.1:8000/attractions/api/getLocation_search_rate?&pid=158&sub_domain=&type_flag=0
        :param request:
        :return:
        """
        if check_request_method(request) == RequestMethod.GET:

            pid = request.GET.get("pid")
            type_flag = request.GET.get("type_flag")
            err_msg = {"status": 0, "code": 0, "message": "参数有误"}
            if not pid and not type_flag:
                return JsonResponse(err_msg)
            try:
                pid = int(pid)
                flag = int(type_flag)
            except Exception:
                return JsonResponse(err_msg)
            # 缓存key构造规则--"searchrate"+str(pid * 1111 + flag)
            key = uuid.uuid5(uuid.NAMESPACE_OID, "searchrate" + str(pid * 1111 + flag))
            response = cache.get(key)
            if response is None:
                # 数据从今年出开始
                year = datetime.datetime.now().year
                init_date = datetime.datetime(year, 1, 1)
                begin_date = int(str(init_date.date()).replace("-", ""))

                rows = SearchRate.objects.filter(pid=pid, tmp_date__gte=begin_date, flag=type_flag).values("tmp_date",
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
                if len(wechat) or len(baidu) or len(sougou):
                    cache.set(key, response, 60 * 60 * 10)
        else:
            return JsonResponse({"status": 0, "code": 0, "message": "请求方式有误"})

        return Comment.deal_response(response)

    @staticmethod
    def get_comment_rate(request):
        """
        获取评论指数--链接格式 ：
        http://127.0.0.1:8000/attractions/api/getCommentRate?pid=6
        :param request:
        :return:
        """
        pid = request.GET.get("pid")
        if not pid:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        try:
            pid = int(pid)
        except ValueError:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})

        key = uuid.uuid5(uuid.NAMESPACE_OID, "comment_rate" + str(pid))
        response = cache.get(key)
        if response is None:
            all = CommentRate.objects.filter(pid=pid).values('pk', "adjectives", "rate").iterator()
            response = {"comment": list(all)}
            cache.set(key, response, 60 * 60 * 10)
        return Comment.deal_response(response)

    @staticmethod
    def get_comment(request):
        """
        获取评论---链接格式http://127.0.0.1:8000/attractions/api/getComment?pid=6
        :param request:
        :return:
        """

        pid = request.GET.get("pid")
        if not pid:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        try:
            pid = int(pid)
        except ValueError:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        key = uuid.uuid5(uuid.NAMESPACE_OID, "comment" + str(pid))
        response = cache.get(key)
        if response is None:
            all = NetComment.objects.filter(pid=pid).values("pk", "commentuser", "comment", "commenttime",
                                                            "commentlike",
                                                            "userphoto").iterator()
            response = {"comment": list(all)}
            cache.set(key, response, 60 * 60 * 10)

        return Comment.deal_response(response)

    def get_state(self, request):
        """
        获取景区状态---链接格式：
        http://127.0.0.1:8000/attractions/api/getState?pid=6
        :param request:
        :return:
        """
        pid = request.GET.get("pid")
        if not pid:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        try:
            pid = int(pid)
        except ValueError:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        key = uuid.uuid5(uuid.NAMESPACE_OID, "state" + str(pid))

        response = cache.get(key)
        if response is None:
            try:
                obj = ScenceState.objects.get(pid=pid)
            except Exception:
                return JsonResponse({"status": 0, "code": 0, "message": "error"})
            response = {"trafficstate": obj.trafficstate, "weatherstate": obj.weatherstate, "coststate": obj.coststate,
                        "environmentstate": obj.environmentstate}
            response = {"state": response}
            cache.set(key, response, 60 * 60 * 10)

        return Comment.deal_response(response)

    @staticmethod
    def deal_response(response):
        response = Access_Control_Allow_Origin(response)

        return response
