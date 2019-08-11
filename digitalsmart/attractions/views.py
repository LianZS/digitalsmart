import datetime
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from tool.access_control_allow_origin import Access_Control_Allow_Origin
from attractions.models import  ScenceImage


# Create your views here.

@csrf_exempt
def upload_photo(request):
    # 上传图片
    pid = request.POST.get("pid")

    file = request.FILES.get("pic", None)
    file_type = file.name.split(".", 2)[1]  # 图片类型

    name = str(datetime.datetime.now().timestamp())
    filename ="".join([name,'.',file_type])
    file.name=filename
    image = ScenceImage()
    image.pid = pid
    image.photo = file
    image.save()

    return HttpResponse("success")


def get_photo_url(request):
    #获取照片链接
    pid = request.GET.get("pid")
    images = ScenceImage.objects.filter(pid=pid).values("photo").iterator()
    response = {"url": list(images)}
    response = JsonResponse(response)
    response = Access_Control_Allow_Origin(response)
    return response



