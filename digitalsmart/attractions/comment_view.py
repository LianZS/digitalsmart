import datetime
from django.views.decorators.cache import cache_page
from django.http import JsonResponse

from attractions.tool.access_control_allow_origin import Access_Control_Allow_Origin
from attractions.models import SearchRate,CommentRate,NetComment,ScenceState
class Comment():
    # http://127.0.0.1:8000/attractions/api/getLocation_search_rate?&pid=158&sub_domain=
    @staticmethod
    @cache_page(timeout=60 * 60 * 12)
    def search_heat(
            request):  # 搜索热度
        # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:  # 反爬虫
        #
        #     return JsonResponse({"status": 0})
        pid = request.GET.get("pid")
        flag =request.GET.get("flag")
        sub_domain = request.GET.get('sub_domain')  # 是否为开发者标识
        if not pid and not flag:
            return JsonResponse({"status": 0})
        try:
            pid = int(pid)
        except Exception:
            return JsonResponse({"status": 0})
        old = datetime.datetime.today() - datetime.timedelta(days=30)
        olddate = int(str(old.date()).replace("-", ""))
        rows = SearchRate.objects.filter(pid=pid, tmp_date__gt=olddate,flag=flag).values("tmp_date", "name", "rate").\
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
        return Comment.deal_response(response)
    @staticmethod
    @cache_page(timeout=60 * 60 * 12)
    def get_comment_rate(request):
        # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:  # 反爬虫
        #
        #     return JsonResponse({"status": 0})
        pid = request.GET.get("pid")
        if pid is None:
            return JsonResponse({"status": 0})
        all = CommentRate.objects.filter(pid=pid).values('pk',"adjectives", "rate").iterator()
        response = {"comment": list(all)}
        return Comment.deal_response(response)
    @staticmethod
    @cache_page(60*60*12)
    def get_comment(request):
        # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:  # 反爬虫
        #
        #     return JsonResponse({"status": 0})
        pid = request.GET.get("pid")
        if pid is None:
            return JsonResponse({"status": 0})
        all = NetComment.objects.filter(pid=pid).values("pk","commentuser","comment","commenttime","commentlike","userphoto").iterator()
        response={"comment":list(all)}
        return Comment.deal_response(response)
    def get_state(self,request):
        # if not 'User-Agent' in request.headers or len(request.COOKIES.values()) == 0:  # 反爬虫
        #
        #     return JsonResponse({"status": 0})
        pid = request.GET.get("pid")
        if pid is None:
            return JsonResponse({"status": 0})
        try:
            obj = ScenceState.objects.get(pid=pid)
        except Exception:
            return JsonResponse({"statue":0})
        response={"trafficstate":obj.trafficstate,"weatherstate":obj.weatherstate,"coststate":obj.coststate,
                  "environmentstate":obj.environmentstate}
        response = {"state": response}
        return Comment.deal_response(response)

    @staticmethod
    def deal_response(response):
        response = JsonResponse(response)

        response = Access_Control_Allow_Origin(response)

        return response