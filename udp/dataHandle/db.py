# -*- coding: utf-8 -*-
from datetime import datetime
import MySQLdb

conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='python', charset='utf8')

cursor = conn.cursor()

values = []


def save(data):
    global values
    values.append('(' + data + ')')
    if len(values) > 99:
        query = 'insert into train values ' + ','.join(values)
        values = []
        cursor.execute(query)
        conn.commit()
        print str(datetime.now()) + 'inserted!'


def safe_exit():
    global values
    if len(values):
        query = 'insert into train values ' + ','.join(values)
        values = []
        cursor.execute(query)
        conn.commit()
    print 'Mysql connection Closed!'


def show():
    print cursor.execute('select * from train')
    res = cursor.fetchall()
