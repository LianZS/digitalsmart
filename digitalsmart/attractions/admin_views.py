import datetime
from django.views.decorators.cache import cache_page
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from attractions.models import ScenceManager,ScenceImage
class Admin():

    def get_all_provinces(self,request):
        all = ScenceManager.objects.all().values("province","loaction","citypid").distinct().iterator()
        response = {"data":list(all)}
        response=JsonResponse(response)
        return response
    def get_cover_pic(self,request):
        pid =request.GET.get("pid")
        photo = ScenceImage.objects.filter(pid=pid).values("photo")
        if len(photo)==0:
            return JsonResponse({"url":{"photo":""}})
        photo=photo[0]
        return  JsonResponse({"url":photo})
