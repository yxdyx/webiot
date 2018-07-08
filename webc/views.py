import json

import simplejson as simplejson
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def hello(request):
    return HttpResponse("Hello world ! ")


def recv_data(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        # req = simplejson.loads(request.raw_post_data)
        username = req['username']
        password = req['password']
        # print(request.body.decode())
        print(username, password)
        print(req)
        j = json.dumps(req)
        return HttpResponse(j)
    else:
        print('abc')
        return HttpResponse("没收到 ")
