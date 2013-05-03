#coding: utf-8
# Create your views here.
from coffin.shortcuts import render_to_response
from django.db import connection


def init(request):
    return render_to_response('index.html', {'msg': 'graphic'})


def data(request):
    cursor = connection.cursor()
    query = 'select g3,g4,g5,atp29,debug0,debug1,debug2,debug3,debug4,debug5 ' \
            'FROM train LIMIT 1000,2000 '
    cursor.execute(query)
    data = cursor.fetchall()
    return render_to_response('index.html', {'data': data})
