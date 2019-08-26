import datetime
import uuid
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.http import JsonResponse

from attractions.tool.access_control_allow_origin import Access_Control_Allow_Origin
from attractions.models import SearchRate, CommentRate, NetComment, ScenceState


class Comment():
    # http://127.0.0.1:8000/attractions/api/getLocation_search_rate?&pid=158&sub_domain=&type_flag=0
    @staticmethod
    def search_heat(
            request):  # 搜索热度
        # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:  # 反爬虫
        #
        #     return JsonResponse({"status": 0})
        pid = request.GET.get("pid")
        type_flag = request.GET.get("type_flag")
        sub_domain = request.GET.get('sub_domain')  # 是否为开发者标识
        if not pid and not type_flag:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        try:
            pid = int(pid)
            flag = int(type_flag)
        except Exception:
            return JsonResponse({"status": 0, "code": 0, "message": "参数有误"})
        # 缓存key构造规则--"searchrate"+str(pid * 1111 + flag)
        key = uuid.uuid5(uuid.NAMESPACE_OID, "searchrate" + str(pid * 1111 + flag))
        response = cache.get(key)
        if response is None:
            old = datetime.datetime.today() - datetime.timedelta(days=30)
            olddate = int(str(old.date()).replace("-", ""))

            rows = SearchRate.objects.filter(pid=pid, tmp_date__gt=olddate, flag=type_flag).values("tmp_date", "name",
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
            cache.set(key, response, 60 * 60 * 10)
        return Comment.deal_response(response)

    # http://127.0.0.1:8000/attractions/api/getCommentRate?pid=6
    @staticmethod
    def get_comment_rate(request):
        # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:  # 反爬虫
        #
        #     return JsonResponse({"status": 0})
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

    # http://127.0.0.1:8000/attractions/api/getComment?pid=6

    @staticmethod
    def get_comment(request):
        # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:  # 反爬虫
        #
        #     return JsonResponse({"status": 0})
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

    #:http://127.0.0.1:8000/attractions/api/getState?pid=6
    def get_state(self, request):
        # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:  # 反爬虫
        #
        #     return JsonResponse({"status": 0})
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
        response = JsonResponse(response)

        response = Access_Control_Allow_Origin(response)

        return response
