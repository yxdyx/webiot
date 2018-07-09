import json

import simplejson as simplejson
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def hello(request):
    return HttpResponse("Hello world ! ")


@login_required(login_url='/')
def recv_data(request):
    if request.method == 'GET':
        try:
            req = json.loads(request.body)
            # req = simplejson.loads(request.raw_post_data)
            username = req['username']
            password = req['password']
            # print(request.body.decode())
            print(username, password)
            print(req)
            j = json.dumps(req)
            return HttpResponse(j)
        except:
            return HttpResponse('为什么不执行')
    else:
        print('abc')
        return HttpResponse("没收到 ")
