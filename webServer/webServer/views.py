#coding: utf-8
from coffin.shortcuts import render_to_response


def homepage(request):
    return render_to_response('index.html', {'msg': 'hello world!'})
