import datetime
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from tool.access_control_allow_origin import Access_Control_Allow_Origin
from attractions.models import SearchRate,CommentRate,NetComment
class Comment():
    # http://127.0.0.1:8000/attractions/api/getLocation_search_rate?&pid=158&sub_domain=
    @staticmethod
    @cache_page(timeout=60 * 60 * 12)
    def search_heat(
            request):  # 搜索热度

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
        response = JsonResponse(response)
        response = Access_Control_Allow_Origin(response)
        return response
    @staticmethod
    @cache_page(timeout=60 * 60 * 24)
    def get_comment_rate(request):
        pid = request.GET.get("pid")
        if pid is None:
            return JsonResponse({"status": 0})
        all = CommentRate.objects.filter(pid=pid).values("adjectives", "rate").iterator()
        response = {"comment": list(all)}
        response = JsonResponse(response)
        response = Access_Control_Allow_Origin(response)
        return response

    def get_comment(self,request):
        pid = request.GET.get("pid")
        if pid is None:
            return JsonResponse({"status": 0})
        all = NetComment.objects.filter(pid=pid).values("commentuser","comment","commenttime","commentlike").iterator()
        response={"comment":list(all)}
        response=JsonResponse(response)
        response=Access_Control_Allow_Origin(response)
        return response
    def get_state(self,request):
        pid = request.GET.get("pid")
        return JsonResponse({"s":1})

