from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from tool.identity_authentication import IdentityAuthentication

from attractions.models import UserProfile


@csrf_exempt
def registered(request):
    if request.method == "POST":

        idcard = request.POST.get('idcard')

        person = IdentityAuthentication().check(idcard=idcard)  # 检查身份证是否正确
        if not person:
            return JsonResponse({"message": "身份证信息有误"})
        password = request.POST.get('password')
        username = request.POST.get('user')
        email = request.POST.get('email')
        # 创建用户
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
        except IntegrityError:
            return JsonResponse({"message": "已存在该用户名"})
        user.save()
        # 将信息存在数据库
        profile = UserProfile()
        profile.idcard = person.idcard
        profile.user = user
        profile.save()
        return JsonResponse({"status": 1, "message": "success"})
    else:
        user = User()
    return JsonResponse({"status": 0, "message": "error"})


@csrf_exempt
def change_password(request):
    if request.method == "POST":
        oldpassword = request.POST.get("oldpassword")
        newpassword = request.POST.get("newpassword")
        username = request.POST.get("user")
        user = authenticate(username=username, password=oldpassword)
        if user is not None:  # 改密码
            u = User.objects.get(username=username)
            u.set_password(newpassword)
            u.save()
            return JsonResponse({"status": 1, "message": "修改成功"})
        else:
            return JsonResponse({"status": 0, "message": "修改失败"})


@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST.get("user")
        password = request.POST.get("password")
