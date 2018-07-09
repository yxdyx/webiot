import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from .models import DeviceInfo


# Create your views here.


#
# def hello(request):
#     return HttpResponse("Hello world ! ")
#
#
# @login_required(login_url='/')
# def recv_data(request):
#     if request.method == 'POST':
#         try:
#             req = json.loads(request.body)
#             username = req['username']
#             password = req['password']
#             print(username, password)
#             print(req)
#             j = json.dumps(req)
#             return HttpResponse(j)
#         except:
#             return HttpResponse('为什么不执行')
#     else:
#         print('abc')
#         return HttpResponse("没收到 ")
#

# class User(forms.Form):
#


# 管理员登录
def login(request):
    if request.method == 'POST':
        try:
            req = json.loads(request.body)
            print(req)
            username = req['username']
            password = req['password']
            print(username+password)
        except:
            return HttpResponse("没有耶")
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active and user.is_staff:
                auth.login(request, user)
                print("yes")
                # return HttpResponse(redirect('/manage'))
                j=json.dumps({"info":"success"})
                return HttpResponse(j)

            else:
                return HttpResponse("该用户无效")
        else:
            return HttpResponse("无此用户")


# 已登录
# 管理员增加用户
@login_required(login_url='/')
def add_user(request):
    if request.method == 'POST':
        try:
            req = json.loads(request.body)
            username = req['username']
            password = req['password']
        except:
            return HttpResponse("没有耶")

        try:
            user = User.objects.create_user(username=username, email=None, password=password,is_staff=1)
        except:
            return HttpResponse("add_user出错啦")

        user.save()
        print("woo")
        return HttpResponse(redirect('/manage'))


# 已登录
# 管理员增加设备
@login_required(login_url='/')
def add_device(request):
    if request.method == 'POST':
        try:
            req = json.loads(request.body)
            devicename = req['devicename']
            devicesecret = req['devicesecret']
        except:
            return HttpResponse("没有耶")

        try:
            device = DeviceInfo.objects.create(devicename=devicename, devicesecret=devicesecret)
        except:
            return HttpResponse("add_device出错啦")

        device.save()
        return HttpResponse(redirect('/manage'))


# 已登录
# 管理员删除用户
@login_required(login_url='/')
def delete_user(request):
    if request.method == 'POST':
        try:
            req = json.loads(request.body)
            username = req['username']
        except:
            return HttpResponse("没有这个人耶")
        try:
            User.objects.filter(username=username).delete()
        except:
            return HttpResponse("delete_user出错啦")

        return HttpResponse(redirect('/manage'))


# 已登录
# 管理员删除设备
@login_required(login_url='/')
def delete_device(request):
    if request.method == 'POST':
        try:
            req = json.loads(request.body)
            device_id = req['id']
        except:
            return HttpResponse("没有耶")
        try:
            DeviceInfo.objects.filter(id=device_id).delete()
        except:
            return HttpResponse("delete_device出错啦")

        return HttpResponse(redirect('/manage'))


# 已登录
# 管理员修改用户密码
@login_required(login_url='/')
def change_user_pwd(request):
    if request.method == 'POST':
        try:
            req = json.loads(request.body)
            username = req['username']
            password = req['password']
            n_pwd = req['n_password']
        except:
            return HttpResponse("没有耶")
        user = auth.authenticate(username=username, password=password)
        try:
            if user is not None:
                user.set_password(n_pwd)
                user.save()
        except:
            return HttpResponse("change出错啦")

        return HttpResponse(redirect('/manage'))


@login_required(login_url='/')
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return HttpResponse(redirect('/'))
