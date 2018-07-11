import threading
import jpype
import json
from django.http import HttpResponse

def findstatus(request):
    if request.method=='POST':
        req = json.loads(request.body)
        devicename=req['devicename']
        jvmPath = jpype.getDefaultJVMPath()
        # ext_classpath = '../../JavaJar/text.jar'
        ext_classpath = 'JavaJar/text.jar'
        jvmArg = '-Djava.class.path=' + ext_classpath

        if not jpype.isJVMStarted():
            jpype.startJVM(jvmPath, jvmArg)

        jpype.attachThreadToJVM()
        Main = jpype.JClass("yuer.yueriot")
        jd = Main()
        s = jd.yuerselectdeviceStatus(devicename)
        return HttpResponse(s)


# print(findstatus("CSDK"))