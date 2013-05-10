#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import struct
import os
from datetime import datetime
from b2t2 import Bin2Txt, PrintType


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

def val2str(vnode, val):
    vtype = vnode[1]
    if vtype == PrintType.BIT:
        valstr = '%s:[%s]' % (vnode[0], ByteToBits(val))
    elif vtype == PrintType.HEX:
        valstr = '%s:[0x%s]' % (vnode[0], ByteToHex(val))
    elif vtype == PrintType.DEC:
        valstr = '%s:(%s)' % (vnode[0], val)
    elif vtype == PrintType.ENUM:
        valstr = '%s:<%s>' % (vnode[0], ByteToHex(val))
    else:
        valstr = '%s:(%s)' % (vnode[0], ByteToHex(val))
    return valstr    

def function():
    pass

def main():
    fnBin = ''
    startRec = 0  # start from the begining of the file
    numRec = 10000  # one hour, one record per 150ms, 60*60/0.15

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

    fmt = test.makeRecordFmt()
    print fmt 
    print struct.calcsize(fmt)

    # print ByteToBits('ABCD')

    print 'file record: %d' % recno
    startTime = datetime.now()
    s = '======= Start record: %d time %s =======\n' % (startRec, startTime)
    outputTxt(s)
    
    vnameList = test.globalVnameList # (v_name, v_type)
    vnames = map(lambda x:x[0], vnameList)
    # print repr(vnames).decode('raw_unicode_escape')

    for recNo in xrange(startRec, startRec+numRec):
        rec = test.loadBinRecord(recNo)
        outputTxt('\n%d ====== \n' % recNo)
        # print rec.encode('hex')
        varData = test.parseRecordFmt(rec, fmt)


        # s1 = map(val2str, vnameList, varData)         #16s
        
        # s1 =[]                                        #22s
        # for i, val in enumerate(varData):
        #     s1 += val2str(vnameList[i], val)


        # s1 = zip(vnames, varData)
        # s = "".join(str(s1)).strip('[]')                  #11s
        # s = '\t'.join(':'.join(str(x)) for x in s1)       #24s
        # s = ''.join(x for x in s1)                        #7.3s
        # fpTxt.write(repr(s).decode('raw_unicode_escape'))

        # s = '\t'.join([str(x) for x in vnames])
        s = '\t'.join(map(val2str, vnameList, varData))     # 16s

        outputTxt(s)

        # print varData
        # recData = test.parseBinRecord(rec)
        # print recData


    endTime = datetime.now()

    s = (u'\n=================== Done. ===================\n'  \
    + u'开始时间:    %s     开始记录: %d \n' % (startTime, startRec)  \
    + u'结束时间:    %s     记录个数：%d \n' % (endTime, numRec)  \
    + u'转换用时:    %s ' % str(endTime - startTime))

    print s
    outputTxt(s)

    fpTxt.close()

if __name__ == '__main__':
    main()
