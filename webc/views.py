import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from .models import DeviceInfo
from .utils.Ali import user_info_all, device_status_all


# Create your views here.

# 用于编辑要发送的json信息
def jsonedit(reason=None, info="success"):
    if reason != None:
        info = "fail"
    j = json.dumps({"info": info, "reason": reason}, ensure_ascii=False)
    return j

#用户登录验证 0：未登录 1：普通用户 2：管理员
def login_require(keyname, keypwd):
    user = auth.authenticate(username=keyname, password=keypwd)
    print(user)
    if user is not None:
        if user.is_staff:
            return 2
        else:
            return 1
    else:
        return 0


# 管理员/用户登录
def login(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        username = req['keyusername']
        password = req['keypassword']
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
        user_info_all()
        device_status_all()
        j = jsonedit(reason)
        return HttpResponse(j)



# 已登录
# 管理员增加用户/管理员
# @login_required
def add_user(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        keyuser = req['keyusername']
        keypwd = req['keypassword']
        a = login_require(keyuser, keypwd)
        if a == 0:
            reason = "未登录"
        elif a == 1:
            reason = "普通用户无此权限"
        elif a == 2:

            try:
                username = req['username']
                password = req['password']
                staff = req['staff']  # 0 user 1 manager
                print(req)
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
        print(j)
        return HttpResponse(j)


# 已登录
# 管理员删除用户/管理员

def delete_user(request):
    if request.method == 'POST':

        req = json.loads(request.body)
        keyuser = req['keyusername']
        keypwd = req['keypassword']
        a = login_require(keyuser, keypwd)
        if a == 0:
            reason = "未登录"
        elif a == 1:
            reason = "普通用户无此权限"
        elif a == 2:

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
# @login_required
def delete_device(request):
    if request.method == 'POST':

        req = json.loads(request.body)
        keyuser = req['keyusername']
        keypwd = req['keypassword']
        a = login_require(keyuser, keypwd)
        if a == 0:
            reason = "未登录"
        elif a == 1:
            reason = "普通用户无此权限"
        elif a == 2:

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

        req = json.loads(request.body)
        keyuser = req['keyusername']
        keypwd = req['keypassword']
        a = login_require(keyuser, keypwd)
        if a == 0:
            reason = "未登录"
        elif a == 1:
            reason = "普通用户无此权限"
        elif a == 2:

            try:
                req = json.loads(request.body)
                username = req['username']
                # password = req['password']
                n_pwd = req['n_password']
            except:
                reason = "没有数据耶"
                j = jsonedit(reason)
                return HttpResponse(j)




            try:
                user=User.objects.filter(username=username).first()
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

#已登录
#更改设备使用用户
# def turn_user(request):
#     req = json.loads(request.body)
#     keyuser = req['keyusername']
#     keypwd = req['keypassword']
#     a = login_require(keyuser, keypwd)
#     if a == 0:
#         reason = "未登录"
#     elif a == 1:
#         reason = "普通用户无此权限"
#     elif a == 2:
#         try:
#             req = json.loads(request.body)
#             username = req['username']
#             devicename=req['devicename']
#         except:
#             reason = "没有数据耶"
#             j = jsonedit(reason)
#             return HttpResponse(j)



# 登出
def logout(request):
    auth.logout(request)
    return HttpResponse(redirect('/'))


# def index(request):
#     return render(request, 'index.html')
#
#
#
# def main(request):
#     return render(request, 'page/main.html')
#
#
# def newsAdd(request):
#     return render(request, 'page/machine/newsAdd.html')
#
#
# def machineList(request):
#     return render(request, 'page/machine/machineList.html')
#
#
#
# def machineEdit(request):
#     return render(request, 'page/machine/machineEdit.html')
#
#
#
# def addUser(request):
#     return render(request, 'page/user/addUser.html')
#
#
#
# def allUsers(request):
#     return render(request, 'page/user/allUsers.html')
#
#
#
# def changePwd(request):
#     return render(request, 'page/user/changePwd.html')
#
#
# def editUser(request):
#     return render(request, 'page/user/editUser.html')
