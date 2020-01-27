import datetime
import uuid
from django.http import JsonResponse, HttpResponse
from django.core.cache import cache

from django.views.decorators.csrf import csrf_exempt
from attractions.tool.processing_response import access_control_allow_origin
from attractions.models import ScenceImage


@csrf_exempt
def upload_photo(request):
    # 上传图片
    pid = request.POST.get("pid")

    file = request.FILES.get("pic", None)

    file_type = file.name.split(".", 2)[1]  # 图片类型

    name = str(datetime.datetime.now().timestamp())
    filename = "".join([name, '.', file_type])
    file.name = filename
    image = ScenceImage()
    image.pid = pid
    image.photo = file
    image.save()

    return HttpResponse("success")


def get_photo_url(request):
    # 获取照片链接
    pid = request.GET.get("pid")
    key = "pic" + pid
    key = uuid.uuid5(uuid.NAMESPACE_OID, key)
    response = cache.get(key)
    if response is None:
        images = ScenceImage.objects.filter(pid=pid).values("photo").iterator()
        response = {"url": list(images)}

    return access_control_allow_origin(response)
