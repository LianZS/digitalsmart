import random
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from attractions.models import ScenceManager, ScenceImage, CommentRate,NetComment


class Admin():

    def get_all_provinces(self, request):
        all = ScenceManager.objects.filter(flag=0).values("province", "loaction", "citypid").distinct().iterator()
        response = {"data": list(all)}
        response = JsonResponse(response)
        return response

    def get_cover_pic(self, request):
        #flag为1时表示要请求的图片时作为封面的，只需要返回一张就就行
        pid = request.GET.get("pid")
        flag=int(request.GET.get("flag"))
        photo = ScenceImage.objects.filter(pid=pid).values("photo")

        if len(photo) == 0:
            return JsonResponse({"url": {"photo": ""}})
        if flag==1:
            photo = photo[0]
        else:
            photo=list(photo)

        return JsonResponse({"url": photo})

    @csrf_exempt
    def up_comment_rate(self, request):
        # {adjectives: ""，pk: xxx，rate: -1}==>表示被删除的数据，{adjectives: "xxx"，pk: -1，rate: YY} =>标识新增的数据
        data = request.POST.get("data")  # '[{"pk": 1, "adjectives": "", "rate": -1},,,,,]'序列化数组对象
        pid = request.POST.get("pid")
        data = eval(data)
        for item in data:
            pk = item['pk']  # 数据库id
            adjectives = item['adjectives']  # 形容词
            rate = item['rate']  # 评分
            if rate == -1:
                CommentRate.objects.filter(pk=pk).delete()

            else:
                if pk != -1:  # 更新

                    CommentRate.objects.filter(pk=pk).update(adjectives=adjectives, rate=rate)
                else:  # 插入
                    cr = CommentRate()
                    cr.pid = pid
                    cr.adjectives = adjectives
                    cr.rate = rate
                    cr.save()

        return JsonResponse({"state": "success"})

    @csrf_exempt

    def up_comment(self, request):
        '''post内容为{'data': ['[{"pk":18,"commentuser":"","comment":"","commenttime":"yyyy-mm-dd","commentlike":2}]'], 'pid': ['6']}
            当pk为整数时，表示要删除的评论，当为-1时表示增加的评论
        '''
        data = request.POST.get("data")  # '[{"pk": 1, "adjectives": "", "rate": -1},,,,,]'序列化数组对象
        pid = request.POST.get("pid")
        data = eval(data)
        for item in data:
            pk = item['pk'] # 数据库id
            commentuser = item['commentuser']  # 形容词
            comment = item['comment']  # 评论
            commenttime=item['commenttime']#评论时间---yyyy-mm-dd
            commentlike =item['commentlike'] #评分
            if pk>0:

                NetComment.objects.filter(pk=pk).delete()

            else:
                if pk == -1:  # 插入
                    try:
                        pic = random.randint(1,31)
                        nc = NetComment()
                        nc.pid=pid
                        nc.userphoto=''.join(["photo/",str(pic),".jpg"])
                        nc.comment=comment
                        nc.commentuser=commentuser
                        nc.commenttime=commenttime
                        nc.commentlike=commentlike
                        nc.save()
                    except Exception :
                        return HttpResponse("参数格式有误！！")

        return HttpResponse("success")
