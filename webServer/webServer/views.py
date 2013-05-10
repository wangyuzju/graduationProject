#coding:utf-8
from coffin.shortcuts import render_to_response


def homepage(request):
    return render_to_response('hello.html', {'message': u'列车运行状态监测服务器软件设计'})
