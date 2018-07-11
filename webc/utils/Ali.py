import jpype
import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from webc.models import UandD

jvmPath = jpype.getDefaultJVMPath()
ext_classpath = './JavaJar/text.jar'
jvmArg = '-Djava.class.path=' + ext_classpath


# 用于编辑要发送的json信息
def jsonedit(reason=None, logininfo="success"):
    if reason != None:
        logininfo = "fail"
    j = json.dumps({"logininfo": logininfo, "reason": reason}, ensure_ascii=False)
    return j


# 已登录
# 管理员请求查看所有设备信息
@login_required(login_url='/')
def device_status_all(request):
    adder = request.user.username
    if User.objects.get(username=adder).is_staff != 1:
        reason = "普通用户无此权限"
        j = jsonedit(reason)
        return HttpResponse(j)
    se = search_device_all()
    return HttpResponse(se)


# 已登录
# 用户请求查看所拥有的设备信息
@login_required(login_url='/')
def device_status_solo(request):
    username = request.user.username
    s = search_device_solo(username)
    return HttpResponse(s)


# 已登录
# 管理员请求查看所有用户信息
@login_required(login_url='/')
def user_info_all(request):
    adder = request.user.username
    if User.objects.get(username=adder).is_staff != 1:
        reason = "普通用户无此权限"
        j = jsonedit(reason)
        return HttpResponse(j)
    se = search_user_all()
    return HttpResponse(se)


# 已登录
# 用户请求查看用户信息
@login_required(login_url='/')
def user_info_solo(request):
    username = request.user.username
    s = search_user_solo(username)
    return HttpResponse(s)


# 设备信息的json包
def search_device_all():
    dd = []
    users = User.objects.all()

    if not jpype.isJVMStarted():
        jpype.startJVM(jvmPath, jvmArg)

    jpype.attachThreadToJVM()
    Main = jpype.JClass("yuer.yueriot")
    jd = Main()
    for user in users:
        devices = UandD.objects.all().filter(userid_id=user.id)
        if devices:
            for device in devices:
                s = jd.yuerselectdeviceStatus(device.devicename)
                q = jd.yuerselectdeviceSecret(device.devicename)
                re = deviceInfoJson(device.deviceid_id, device.devicename, q, device.username, s)
                dd.append(re)
    s = json.dumps(dd, indent=4)
    return s


def deviceInfoJson(did, dname, dsect, user, status):
    dic = {"newsId": str(did), "newsName": dname, "newsPwd": dsect, "newsAuthor": user, "newsStatus": status}
    return dic


def search_device_solo(username):
    dd = []

    if not jpype.isJVMStarted():
        jpype.startJVM(jvmPath, jvmArg)
    jpype.attachThreadToJVM()
    Main = jpype.JClass("yuer.yueriot")
    jd = Main()

    users = User.objects.filter(username=username)
    for user in users:
        devices = UandD.objects.all().filter(userid_id=user.id)
        if devices:
            for device in devices:
                s = jd.yuerselectdeviceStatus(device.devicename)
                q = jd.yuerselectdeviceSecret(device.devicename)
                re = deviceInfoJson(device.deviceid_id, device.devicename, q, device.username, s)
                dd.append(re)
    s = json.dumps(dd, indent=4)
    return s


def search_user_all():
    dd = []
    users = User.objects.all()

    for user in users:
        print(user.username)
        deviceinfo = ''
        i = 0
        devices = UandD.objects.all().filter(userid_id=user.id)
        if devices:
            for device in devices:
                if i == 0:
                    deviceinfo = device.devicename
                    i = i + 1
                else:
                    deviceinfo = deviceinfo + ',' + device.devicename
        else:
            deviceinfo = "null"
        print(deviceinfo)
        re = userInfoJson(user.id, user.username, user.is_staff, deviceinfo, str(user.last_login))
        dd.append(re)
    s = json.dumps(dd, indent=4)
    return s


def search_user_solo(username):
    dd = []
    users = User.objects.filter(username=username)
    for user in users:
        print(user.username)
        deviceinfo = ''
        i = 0
        devices = UandD.objects.all().filter(userid_id=user.id)
        if devices:
            for device in devices:
                if i == 0:
                    deviceinfo = device.devicename
                    i = i + 1
                else:
                    deviceinfo = deviceinfo + ',' + device.devicename
        else:
            deviceinfo = "null"
        print(deviceinfo)
        re = userInfoJson(user.id, user.username, user.is_staff, deviceinfo, str(user.last_login))
        dd.append(re)
    s = json.dumps(dd, indent=4)
    print(s)
    return s


def userInfoJson(userid, username, usergrade, userstatus, lastlogint):
    dic = {"usersId": userid, "userName": username, "userGrade": usergrade,
           "userStatus": userstatus, "userEndTime": lastlogint}
    return dic
