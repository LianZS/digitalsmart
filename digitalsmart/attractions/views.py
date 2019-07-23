from django.shortcuts import render, HttpResponse,Http404
from attractions.models import ScenceManager


# Create your views here.


def scencelist(request):
    # if len(request.COOKIES.values())==0 : #反爬虫
    #     return Http404
    # ScenceManager.objects.filter(citypid=)
    return HttpResponse(request.COOKIES)
