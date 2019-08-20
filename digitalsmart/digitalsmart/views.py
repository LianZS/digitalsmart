from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, Http404, HttpResponse, StreamingHttpResponse, HttpResponseRedirect
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from tool.identity_authentication import IdentityAuthentication
from attractions.models import UserProfile
from django.shortcuts import render
from django.contrib.auth.forms import PasswordChangeForm
from tool.file_hander import Hander_File


@csrf_exempt
def registered(request):
    # 字段idcard，password，user，email
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
        # 链接待转
        return render(request, "upload.html")
    else:
        user = User()

        return Http404


@csrf_exempt
def login_view(request):  # user，password
    if request.method == "POST":
        username = request.POST.get("user")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if request.user.is_authenticated:
            print("h活跃的")
        if user is not None:
            login(request, user)
            # 链接待转
            return render(request, "upload.html")
        else:
            # 链接待转
            return HttpResponse("404")
    return JsonResponse({"message": "error"})


@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({"STATUS": 0})


@csrf_exempt
def password_change(request):  # 密码更改时会话失效
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return JsonResponse({"STATUS": 1})

    return JsonResponse({"STATUS": 0})


@csrf_exempt
def upload_user_pic(request):  # 更新用户头像
    if request.user.is_authenticated:
        file = request.FILES.get("pic", None)
        file_type = file.name.split(".", 2)[1]  # 图片类型
        user = UserProfile.objects.get(user=request.user)
        filename = ''.join([user.user.username, '.', file_type])  # 以用户名命名图像
        user.photo.save(filename, file, save=True)
        return HttpResponse("success")
        # return  HttpResponseRedirect("http://127.0.0.1:8000/down/")
    return HttpResponse("error")


def down_user_pic(request): #下载用户头像
    if request.user.is_authenticated:

        user = UserProfile.objects.get(user=request.user)
        imgae = user.photo

        file_itertor = Hander_File().hander_file(imgae)

        return HttpResponse(file_itertor, content_type=" image/png")
    return HttpResponse("CSS")



    # the_file_name = "big.gif"

    # response = StreamingHttpResponse(file_itertor)
    # response['content_type'] = 'image/png'
    # response['Content-Disposition'] = 'attachment;filename={0}'.format(the_file_name)


