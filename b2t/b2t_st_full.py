#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    转换程序 bin+xml=>txt
    从ATO运行时生成的bin格式的log，与atoviewer配套的xml结合，生成txt形式的文件

    使用struct.unpack函数进行数据解包，分段打印所有数据，比bit版快3倍以上

    ./b2t_st_1.py [<atolog.bin> [<start> <num>]]

    o xml文件名和相应的字段大小在b2t2.py中设定G_XML_FILE & G_RECORD_LEN

    * .bin文件和.xml文件如果没有在命令行给出则会提示输入
    * 参数中指定<start>为起始记录号，<num>为要转换的记录个数
      不指定时从第0个记录开始24000个记录，即约1个小时的数据
    * 生成的文件是utf-8编码

'''
import sys
import os
from datetime import datetime
from b2t2 import Bin2Txt, PrintType

# 生成txt文件名，打开

def openTxtFile(binFilename):
    global fpTxt

    (txtFilename, binext) = os.path.splitext(binFilename)
    txtFilename = txtFilename + '.txt'
    if txtFilename is not None:
        fpTxt = open(txtFilename, 'w')
        return fpTxt
    else:
        return None

# Error handling

def sysExit(reason):
    print 'xxxxxxxxxxxxxxxxxxxxxxxx File not ready. Error No: %d '% reason
    sys.exit()

def outputTxt(s):
    # print s
    fpTxt.write(s.encode('utf-8'))
    # pass

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

#-------------------------------------------------------------------------------

def HexToByte( hexStr ):
    """
    Convert a string hex byte values into a byte string. The Hex Byte values may
    or may not be space separated.
    """
    # The list comprehension implementation is fractionally slower in this case    
    #
    #    hexStr = ''.join( hexStr.split(" ") )
    #    return ''.join( ["%c" % chr( int ( hexStr[i:i+2],16 ) ) \
    #                                   for i in range(0, len( hexStr ), 2) ] )
 
    bytes = []

    hexStr = ''.join( hexStr.split(" ") )

    for i in range(0, len(hexStr), 2):
        bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )

    return ''.join( bytes )

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

    fmtdic = test.makeRecordFmtDict()

    # print 'file record: %d' % recno
    startTime = datetime.now()
    s = '======= Start record: %d time %s =======\n' % (startRec, startTime)
    outputTxt(s)


    endRec = startRec+numRec
    if endRec > recno: endRec = recno
    for recNo in xrange(startRec, endRec):
        outputTxt('================== %d' % recNo)
        rec = test.loadBinRecord(recNo)

        for secStr in test.globalDictKeys:
            # GLOBAL (0, 41, '>L4s4slll4slllc', [(u'ATO\u5468\u671f', 1), ....])
            secTuple = test.globalFormatDict[secStr]
            outputTxt('\n---> %s \n' % secStr)

            valList = test.parseRecordSection(secTuple, rec)
            vnameList = secTuple[3] # (v_name, v_type)
            s = ''
            for i, val in enumerate(valList):
                if vnameList[i][1] == PrintType.BIT:
                    valstr = '[%s]' % ByteToHex(val)
                elif vnameList[i][1] == PrintType.HEX:
                    valstr = '[0x%s]' % ByteToHex(val)
                elif vnameList[i][1] == PrintType.DEC:
                    valstr = '(%d)' % int(val)
                elif vnameList[i][1] == PrintType.ENUM:
                    # print vnameList[i][0], val
                    valstr = '<%s>' % ByteToHex(val)
                else:
                    valstr = '(%s)' % val
                s += '\t%s:%s' % (vnameList[i][0], valstr)
                # print i, vnameList[i][0],vnameList[i][1], val
            outputTxt(s)
            outputTxt(u'\n<--- %s \n' % secStr)

        # print rec.encode('hex')

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
