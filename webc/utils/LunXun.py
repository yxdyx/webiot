import jpype
import base64
import json

jvmPath = jpype.getDefaultJVMPath()
ext_classpath = '../../JavaJar/text.jar'
jvmArg = '-Djava.class.path=' + ext_classpath



def Lx():

    if not jpype.isJVMStarted():
        jpype.startJVM(jvmPath, jvmArg)

    jpype.attachThreadToJVM()
    Main = jpype.JClass("yuerr.yuermns")
    jd = Main()

    s=jd.yuermnscycle()
    print(s+'\n'+'\n')
    a=base64.b64decode(s).decode('utf-8')
    print(a)
    print("\n\n")
    # b=a.decode('utf-8')
    # print(b)
    # print("\n\n")
    c=eval(a)
    d=base64.b64decode(c['payload']).decode('utf-8')
    print(d)
    begin=c['topic'].find('/',1,len(c['topic']))
    # print(begin)
    end=c['topic'].rfind('/')
    # print(end)
    print(c['topic'][begin+1:end])
    # print(a.decode())


def order():
    if not jpype.isJVMStarted():
        jpype.startJVM(jvmPath, jvmArg)

    jpype.attachThreadToJVM()
    Main = jpype.JClass("yuer.yueriot")
    jd = Main()
    s=jd.yuerorder("CSDK","0")


# if __name__=='__main__':
#     order()
#     LunX()

# 从轮询中取消息
def LunX():

    # if not jpype.isJVMStarted():
    #     jpype.startJVM(jvmPath, jvmArg)
    #
    # jpype.attachThreadToJVM()
    # Main = jpype.JClass("yuerr.yuermns")
    # jd = Main()
    # s = jd.yuermnscycle()
    all={"qq":"qq","oo":"oo"}
    q=[]
    q.append(all)
    i={"dd":"dd"}
    q.append(i)
    print(q)
    p=json.dumps(q)
    print(p)
    d=json.loads(p)
    print(d+type(d))
    # e=json.loads(str(d))
    # print(e)

LunX()

