import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from .models import DeviceInfo
from .utils.Ali import user_info_all,device_status_all

# Create your views here.

# 用于编辑要发送的json信息
def jsonedit(reason=None, info="success"):
    if reason != None:
        info = "fail"
    j = json.dumps({"info": info, "reason": reason}, ensure_ascii=False)
    return j


# 管理员/用户登录
def login(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        username = req['username']
        password = req['password']
        if username == '' or password == '':
            reason = "没有数据耶"
            j = jsonedit(reason)
            return HttpResponse(j)
        print(req)
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                reason = None
            else:
                reason = "该用户无效"
        else:
            reason = "无此用户或密码错误"
        j = jsonedit(reason)
        return HttpResponse(j)
    else:
        return render(request, 'login.html')

# 已登录
# 管理员增加用户/管理员
@login_required
def add_user(request):
    if request.method == 'POST':

        adder = request.user.username
        if User.objects.get(username=adder).is_staff != 1:
            info = "fail"
            reason = "普通用户无此权限"
            j = jsonedit(info, reason)
            return HttpResponse(j)

        try:
            req = json.loads(request.body)
            username = req['username']
            password = req['password']
            staff = req['staff']  # 0 user 1 manager
        except:
            reason = "没有数据耶"
            j = jsonedit(reason)
            return HttpResponse(j)

        try:
            user = User.objects.create_user(username=username, email=None, password=password, is_staff=staff)
        except:
            reason = "add_user出错啦"
            j = jsonedit(reason)
            return HttpResponse(j)

        user.save()
        user_info_all()
        reason = None
        j = jsonedit(reason)
        return HttpResponse(j)



# 已登录
# 管理员删除用户/管理员
@login_required
def delete_user(request):
    if request.method == 'POST':

        adder = request.user.username
        if User.objects.get(username=adder).is_staff != 1:
            reason = "普通用户无此权限"
            j = jsonedit(reason)
            return HttpResponse(j)

        try:
            req = json.loads(request.body)
            username = req['username']
        except:
            reason = "没有这个人耶"
            j = jsonedit(reason)
            return HttpResponse(j)

        try:
            User.objects.filter(username=username).delete()
        except:

            reason = "delete_user出错啦"
            j = jsonedit(reason)
            return HttpResponse(j)

        user_info_all()
        device_status_all()

        reason = None
        j = jsonedit(reason)
        return HttpResponse(j)


# 已登录
# 管理员删除设备
@login_required
def delete_device(request):
    if request.method == 'POST':

        adder = request.user.username
        if User.objects.get(username=adder).is_staff != 1:
            reason = "普通用户无此权限"
            j = jsonedit(reason)
            return HttpResponse(j)

        try:
            req = json.loads(request.body)
            device_id = req['id']
        except:

            reason = "没有这个设备耶"
            j = jsonedit(reason)
            return HttpResponse(j)

        try:
            DeviceInfo.objects.filter(id=device_id).delete()
        except:

            reason = "delete_device出错啦"
            j = jsonedit(reason)
            return HttpResponse(j)

        user_info_all()
        device_status_all()

        reason = None
        j = jsonedit(reason)
        return HttpResponse(j)


# 已登录
# 管理员修改用户密码
@login_required
def change_user_pwd(request):
    if request.method == 'POST':

        adder = request.user.username
        if User.objects.get(username=adder).is_staff != 1:
            reason = "普通用户无此权限"
            j = jsonedit(reason)
            return HttpResponse(j)

        try:
            req = json.loads(request.body)
            username = req['username']
            password = req['password']
            n_pwd = req['n_password']
        except:

            reason = "没有这数据耶"
            j = jsonedit(reason)
            return HttpResponse(j)

        user = auth.authenticate(username=username, password=password)
        try:
            if user is not None:
                user.set_password(n_pwd)
                user.save()
                reason = None
            else:
                reason = "无此用户"
        except:

            reason = "改密码出错啦"
            j = jsonedit(reason)
            return HttpResponse(j)

        j = jsonedit(reason)
        return HttpResponse(j)


# 登出
@login_required
def logout(request):
    print(request.user.username + " ou")
    auth.logout(request)
    return HttpResponse(redirect('/'))



@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def main(request):
    return render(request, 'page/main.html')

@login_required
def newsAdd(request):
    return render(request,'page/machine/newsAdd.html')

@login_required
def machineList(request):
    return render(request,'page/machine/machineList.html')

@login_required
def machineEdit(request):
    return render(request,'page/machine/machineEdit.html')

@login_required
def addUser(request):
    return render(request,'page/user/addUser.html')

@login_required
def allUsers(request):
    return render(request,'page/user/allUsers.html')

@login_required
def changePwd(request):
    return render(request,'page/user/changePwd.html')

@login_required
def editUser(request):
    return render(request,'page/user/editUser.html')

