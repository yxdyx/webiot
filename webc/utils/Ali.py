import jpype
import json
from django.http import HttpResponse
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from webc.models import UandD, DeviceInfo
from .SaveJson import newssave, userssave
from django.contrib import auth

jvmPath = jpype.getDefaultJVMPath()
ext_classpath = './JavaJar/text.jar'
jvmArg = '-Djava.class.path=' + ext_classpath


# 用于编辑要发送的json信息
def jsonedit(reason=None, info="success"):
    if reason != None:
        info = "fail"
    j = json.dumps({"info": info, "reason": reason}, ensure_ascii=False)
    return j


# 用户登录验证 0：未登录 1：普通用户 2：管理员
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


# 保存所获取的所有设备信息
def device_status_all():
    search_device_all()


# 已登录
# 用户请求查看所拥有的设备信息
def device_status_solo(request):
    req = json.loads(request.body)
    keyuser = req['keyusername']
    keypwd = req['keypassword']
    a = login_require(keyuser, keypwd)
    if a == 0:
        reason = "未登录"
        s = jsonedit(reason)
    else:
        s = search_device_solo(keyuser)
    return HttpResponse(s)


# 保存所有用户信息
def user_info_all():
    search_user_all()


# 已登录
# 用户请求查看用户信息
def user_info_solo(request):
    req = json.loads(request.body)
    keyuser = req['keyusername']
    keypwd = req['keypassword']
    a = login_require(keyuser, keypwd)
    if a == 0:
        reason = "未登录"
        s = jsonedit(reason)
    else:
        s = search_user_solo(keyuser)
    return HttpResponse(s)


# 已登录
# 管理员增加设备同时与已有用户绑定
# 若用户名为空 则只是单纯注册设备
def add_device(request):
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
                devicename = req['devicename']
                type = req['type']
            except:
                reason = "没有数据耶"
                j = jsonedit(reason)
                return HttpResponse(j)

            username = req['username']
            if username:  # 单纯添加设备，不与用户绑定
                try:
                    userid = User.objects.get(username=username).id
                except:
                    reason = "无此用户"
                    j = jsonedit(reason)
                    return HttpResponse(j)
                flag = 1
            else:
                flag = 0

            device = DeviceInfo.objects.filter(devicename=devicename)
            if device.exists():
                print(device)
                reason = "重名啦"
                j = jsonedit(reason)
                return HttpResponse(j)

            if not jpype.isJVMStarted():
                jpype.startJVM(jvmPath, jvmArg)

            jpype.attachThreadToJVM()
            Main = jpype.JClass("yuer.yueriot")
            jd = Main()
            secret = jd.yuerregist(devicename)

            try:
                id = DeviceInfo.objects.create(devicename=devicename, devicesecret=secret, type=type).id
            except:
                reason = "add_device出错"
                j = jsonedit(reason)
                return HttpResponse(j)

            if flag == 1:
                UandD.objects.create(username=username, deviceid_id=id, devicename=devicename, userid_id=userid,
                                     device_type=type)

            user_info_all()
            device_status_all()

            reason = None
        j = jsonedit(reason)
        return HttpResponse(j)


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
            # print(devices)
            for device in devices:
                try:
                    s = jd.yuerselectdeviceStatus(device.devicename)
                except:
                    s = "ERROR"

                uad = DeviceInfo.objects.filter(devicename=device.devicename).first()
                re = deviceInfoJson(device.deviceid_id, device.devicename, uad.devicesecret, device.username, s,
                                    uad.type)
                dd.append(re)
    # s = json.dumps(dd, indent=4)
    # print(s)
    newssave(dd)


def deviceInfoJson(did, dname, dsect, user, status, type):
    dic = {"newsId": str(did), "newsName": dname, "newsPwd": dsect, "newsAuthor": user, "newsStatus": status,
           "type": type}
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
                try:
                    s = jd.yuerselectdeviceStatus(device.devicename)
                except:
                    s = "ERROR"
                # q = DeviceInfo.objects.get(devicename=device.devicename).devicesecret
                # q = DeviceInfo.objects.filter(devicename=device.devicename).first().devicesecret
                uad = DeviceInfo.objects.filter(devicename=device.devicename).first()
                re = deviceInfoJson(device.deviceid_id, device.devicename, uad.devicesecret, device.username, s,
                                    uad.type)
                print(re)
                dd.append(re)
    s = json.dumps(dd, indent=4)
    return s


def search_user_all():
    dd = []
    users = User.objects.all()

    for user in users:
        # print(user.username)
        deviceinfo = ''
        i = 0
        devices = UandD.objects.all().filter(userid_id=user.id)
        if devices:
            for device in devices:
                if i == 0:
                    deviceinfo = device.device_type + ':' + device.devicename
                    i = i + 1
                else:
                    deviceinfo = deviceinfo + ',' + device.device_type + ':' + device.devicename
        else:
            deviceinfo = "null"
        # print(deviceinfo)
        re = userInfoJson(user.id, user.username, user.is_staff, deviceinfo, str(user.last_login))
        dd.append(re)
    # s = json.dumps(dd, indent=4)
    # return s
    userssave(dd)


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
                    deviceinfo = device.device_type + ':' + device.devicename
                    i = i + 1
                else:
                    deviceinfo = deviceinfo + ',' + device.device_type + ':' + device.devicename
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
