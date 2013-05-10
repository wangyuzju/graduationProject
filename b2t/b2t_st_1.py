#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    转换程序 bin+xml=>txt
    从ATO运行时生成的bin格式的log，与atoviewer配套的xml结合，生成txt形式的文件

    使用struct.unpack进行数据解包，只打印一个字段的数据，为最快解析速度

    ./b2t_st_1.py [<atolog.bin> [<start> <num>]]

    o xml文件名和相应的字段大小在b2t2.py中设定G_XML_FILE & G_RECORD_LEN
    o 需要显示的字段名 修改下面：FIELD_NAME

    * .bin文件和.xml文件如果没有在命令行给出则会提示输入
    * 参数中指定<start>为起始记录号，<num>为要转换的记录个数
      不指定时从第0个记录开始24000个记录，即约1个小时的数据
    * 生成的文件是utf-8编码

'''

import sys
import struct
import os
from datetime import datetime
from b2t2 import Bin2Txt, PrintType

# 需要显示的字段名
FIELD_NAME = u'列车当前速度(KPH*10)'



def outputTxt(s):
    # print s
    fpTxt.write(s.encode('utf-8'))
    # pass

def openTxtFile(binFilename):
    global fpTxt

    (txtFilename, binext) = os.path.splitext(binFilename)
    txtFilename = txtFilename + '.txt'
    if txtFilename is not None:
        fpTxt = open(txtFilename, 'w')
        return fpTxt
    else:
        return None

#-------------------------------------------------------------------------------

def ByteToHex( byteStr ):
    """
    Convert a byte string to it's hex string representation e.g. for output.
    """
    
    # Uses list comprehension which is a fractionally faster implementation than
    # the alternative, more readable, implementation below
    #   
    #    hex = []
    #    for aChar in byteStr:
    #        hex.append( "%02X " % ord( aChar ) )
    #
    #    return ''.join( hex ).strip()        

    return ''.join( [ "%02X" % ord( x ) for x in byteStr ] ).strip()

def ByteToBits( byteStr ):
    bytes = (ord(b) for b in byteStr)
    s = ''
    for b in bytes:
        for i in reversed(xrange(8)):
            s += str((b >> i) & 1)
        # s += ' '
    return s

def val2str(vtype, val):
    if vtype == PrintType.BIT:
        valstr = '[%s]' % ByteToBits(val)
    elif vtype == PrintType.HEX:
        valstr = '[0x%s]' % ByteToHex(val)
    elif vtype == PrintType.DEC:
        valstr = '(%d)' % int(val)
    elif vtype == PrintType.ENUM:
        valstr = '<%s>' % ByteToHex(val)
    else:
        valstr = '(%s)' % ByteToHex(val) 
    return valstr    

def function():
    pass

def main():
    fnBin = ''
    startRec = 0  # start from the begining of the file
    numRec = 24000  # one hour, one record per 150ms, 60*60/0.15

    if len(sys.argv) < 2:
        fnBin = raw_input('Input the BIN filename: ')
    else:
        fnBin = sys.argv[1]

    # if start & num specified, use them

    if len(sys.argv) > 2:
        startRec = int(sys.argv[2])
    if len(sys.argv) > 3:
        numRec = int(sys.argv[3])

    fpTxt = openTxtFile(fnBin)
    if fpTxt is None: sysExit(2)

    test = Bin2Txt()
    recno = test.initFile(fnBin)
    print 'File total record: %d' % recno
    if recno <= 0: sysExit(1)

    fmt = test.makeRecordFmt()
    print 'Format string: %s' % fmt 
    print 'Record size: %d' % struct.calcsize(fmt)

    # print ByteToBits('ABCD')

    startTime = datetime.now()
    s = '======= Start record: %d time %s =======\n' % (startRec, startTime)
    outputTxt(s)


    vnameList = test.globalVnameList # (v_name, v_type)

    # for x in vnameList:
    #     print x[0]

    index_y1 = [x[0] for x in vnameList].index(FIELD_NAME)
    print 'Field name: %s \t field index: %d' % (FIELD_NAME, index_y1)

    endRec = startRec+numRec
    if endRec > recno: endRec = recno
    for recNo in xrange(startRec, endRec):
        rec = test.loadBinRecord(recNo)
        outputTxt('\n%d ====== \n' % recNo)
        # print rec.encode('hex')
        varData = test.parseRecordFmt(rec, fmt)

        i = 0
        # for i, val in enumerate(varData):
        outputTxt(vnameList[index_y1][0]+val2str(vnameList[index_y1][1], varData[index_y1]))

        # print varData
        # recData = test.parseBinRecord(rec)
        # print recData


    endTime = datetime.now()

    s = (u'\n=================== Done. ===================\n'  \
    + u'开始时间:    %s     开始记录: %d \n' % (startTime, startRec)  \
    + u'结束时间:    %s     记录个数：%d \n' % (endTime, recNo-startRec+1)  \
    + u'转换用时:    %s ' % str(endTime - startTime))

    print s
    outputTxt(s)

    fpTxt.close()

if __name__ == '__main__':
    main()
