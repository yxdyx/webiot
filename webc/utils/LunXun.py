import jpype
import base64
import json
import os
from webc.models import UandD, DeviceInfo
from django.http import HttpResponse
from django.contrib import auth

jvmPath = jpype.getDefaultJVMPath()
ext_classpath = './JavaJar/text.jar'
jvmArg = '-Djava.class.path=' + ext_classpath


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


# 用于编辑要发送的json信息
def jsonedit(reason=None, info="success"):
    if reason != None:
        info = "fail"
    j = json.dumps({"info": info, "reason": reason}, ensure_ascii=False)
    return j


# 发送命令
def order(devicename, ord):
    if not jpype.isJVMStarted():
        jpype.startJVM(jvmPath, jvmArg)

    jpype.attachThreadToJVM()
    Main = jpype.JClass("yuer.yueriot")
    jd = Main()
    try:
        s = jd.yuerorder(devicename, ord)
    except:
        return False
    return s


def airtemp(data, devicename):
    dir = 'static/Devices/air/' + devicename + '_airTemp.json'
    print(dir)
    old_data = []
    if os.path.exists(dir):
        with open(dir, 'r', encoding='utf-8') as json_file:
            # json.dump(data, json_file, ensure_ascii=False, indent=4)
            # json_file.write(',')
            old_data = json.load(json_file)
            print("old")
            print(old_data)
            old_data = eval(old_data)

    # data=json.dumps(data,ensure_ascii=False)
    old_data.append(data)
    pr = json.dumps(old_data, ensure_ascii=False)
    print("pr")
    print(pr)
    with open(dir, 'w', encoding='utf-8') as json_file:
        # json.dump(pr, json_file, ensure_ascii=False, indent=4)
        json_file.write(json.dumps(pr, ensure_ascii=False, indent=4))


def feedtemp(data, devicename):
    dir = 'static/Devices/feedback/' + devicename + '_feed.json'
    with open(dir, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


# 从轮询中取消息
def LunX():
    if not jpype.isJVMStarted():
        jpype.startJVM(jvmPath, jvmArg)
    jpype.attachThreadToJVM()
    Main = jpype.JClass("yuerr.yuermns")
    jd = Main()
    try:
        s = jd.yuermnscycle()
    except:
        return int(0)
    if s is None:
        return int(1)
    allmix = base64.b64decode(s).decode('utf-8')
    temp = eval(allmix)
    payload = base64.b64decode(temp['payload']).decode('utf-8')
    print("payload")
    print(payload)
    begin = temp['topic'].find('/', 1, len(temp['topic']))
    end = temp['topic'].rfind('/')
    devicename = temp['topic'][begin + 1:end]

    # feedtemp(payload,devicename)

    compmes = json.dumps(eval(payload), separators=(',', ':'), ensure_ascii=False)
    print("compmes")
    compmes = eval(compmes)
    print(compmes)
    # print(isinstance(compmes,))
    try:
        opt = compmes['opt']
        print(opt)
        if opt == "temperature":
            value = DeviceInfo.objects.filter(devicename=devicename).first().value
            if value != "-1":  # 阈值为-1代表自动开机禁止
                if value > temp:  # 空调超过阈值开机
                    order(devicename, "1")
                airtemp(compmes, devicename)
        else:
            feedtemp(compmes, devicename)
    except:
        return int(0)

    return int(2)


# 请求反馈
def cycle(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        keyuser = req['keyusername']
        keypwd = req['keypassword']
        a = login_require(keyuser, keypwd)
        if a == 0:
            reason = "未登录"
            s = jsonedit(reason)
        else:
            type = req['type']
            devicename = req['devicename']
            ns = req['ns']
            value = req['value']

            if type == "1":
                device = DeviceInfo.objects.filter(devicename=devicename).first()
                device.update()

            if type != "leave":
                if not order(devicename, ns):
                    reason = "设备故障"
            else:
                uads = UandD.objects.filter(username=keyuser)
                if uads.exists():
                    for uad in uads:
                        if not order(uad.devicename, "0"):
                            reason = "设备故障"

            a = 2
            while a != 1:
                a = LunX()
                if a == 0:
                    reason = "出错"
                    j = jsonedit(reason)
                    return j

            reason = None
        j = jsonedit(reason)
        return HttpResponse(j)
