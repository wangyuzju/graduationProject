#-*- coding: utf-8 -*-
import socket
from datetime import datetime
import thread
import dataHandle.parse as dataServer
import conf.config as config

address = ('127.0.0.1', 31500)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)

print 'UDP server listening at ', address


def dataHandle(data):
    #print data.encode('hex_codec')
    dataServer.parseBin(data)


def startServer():
    print config.MYSQL
    while True:
        data, address = s.recvfrom(654)
        if not data:
            print "client has exist"
            break
        thread.start_new(dataHandle, (data,))

if __name__ == '__main__':
    startServer()


s.close()