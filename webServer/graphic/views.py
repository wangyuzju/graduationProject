#coding: utf-8
import json
from django.db import connection
from django.http import HttpResponse
from coffin.shortcuts import render_to_response


def data(request):
    """select data for draw the graphic from database"""
    cursor = connection.cursor()
    query = ('select g4,g5,g6,atp30,debug2,debug5'
             ' FROM train')
    cursor.execute(query)
    data = cursor.fetchall()
    #return render_to_response('index.html', {'data': data})
    response_data = {}
    for item in data:
        response_data[item[0]] = item[1:]
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def list_all(request):
    """
    cursor = connection.cursor()
    query = ('select g4,g5,g6,atp30,debug2,debug5'
             ' FROM train')
    cursor.execute(query)
    data = cursor.fetchall()
    """
    return render_to_response('graphic.html', {'data': data})
