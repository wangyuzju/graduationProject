#!/usr/bin/python
# -*- coding: utf-8 -*-


''' 转换程序 bin+xml=>txt
    从ATO运行时生成的bin格式的log，与atoviewer配套的xml结合，生成txt形式的文件

    用法：./bin2txt.py [<atolog.bin> <atoxml.xml> [<start> <num>]]
    生成：<atolog.txt>

    * .bin文件和.xml文件如果没有在命令行给出则会提示输入
    * 参数中指定<start>为起始记录号，<num>为要转换的记录个数
      不指定时从第0个记录开始24000个记录，即约1个小时的数据
    * 生成的文件是utf-8编码

    o 生成的txt文件中:
        圆括号中如：(159) 中的数据是10进制
        方括号中如：[19ff]中数据是十六进制
        位数据和事件数据下划线_表示0，X表示1

    o 使用前需要修改代码中以下行，对应bin文件中一个记录的大小：

    # the length of ONE record in the .bin file
    G_RECORD_LEN = 187


    o G_DIFFVIEW 是指<start>对应的第一个记录作为参考数据，
      后续的数据只打印与它有差异的部分
     （*不包括global部分）。
     设为False则打印完整记录

    o G_RAWDATA 表示在txt中打印hex形式的原始数据
'''
import sys
import os
import struct
from datetime import datetime
import xml.etree.ElementTree as ET
import db

# the length of ONE record in the .bin file
G_RECORD_LEN = 654

# set True to make the startRec a BASE RECORD
# the following record is compared to the base 
# only the different key-value pair is writed.
G_DIFFVIEW = True

# set True if you want the raw data of a record in hex form
G_RAWDATA = False

# load the xml file.
RESULT = []

def loadXmlFile(fileName):
    global xmlRoot, xmlGlobal, xmlAllModules, xmlAllVariables

    xmlRoot = ET.parse(fileName).getroot()

    xmlGlobal = xmlRoot.find('global')
    xmlAllModules = xmlRoot.findall('module')

    if xmlAllModules:
        return True
    else:
        return False


def byte2int(bytes):
    # return int(bytes.encode('hex'), 16)
    if len(bytes) == 4:
        # > 大端法表示 L unsigned Long 4字节
        return struct.unpack(">L", bytes)[0]
    elif len(bytes) == 1:
        return ord(bytes[0])
    else:
        return int(bytes.encode('hex'), 16)
        #return struct.unpack(">L", bytes)[0]
        # ?not implemented :return int.from_bytes(bytes, 'big')


def parseNodeByte(varNode, nodeBytes, vType):
    if vType == 'VARS_DEC':
        nodeValue = str(byte2int(nodeBytes))
    elif vType == 'VARS_CYCLE':
        nodeValue = str(byte2int(nodeBytes))
    elif vType == 'VARS_HEX':
        nodeValue = nodeBytes.encode('hex')
    elif vType == 'VARS_LIST':
        nodeValue = nodeBytes.encode('hex')
    elif vType == 'VARS_EVENT':
        # TODO: temparory 
        nodeValue = nodeBytes.encode('hex') #+ '|'

        #defNode = varNode.find('definitions')
        #if defNode is not None:
        #    eventDefList = defNode.findall('v_def')
        #    for defItem in eventDefList:
        #        defName = defItem.find('def_value').text
        #        defOffset = int(defItem.find('def_offset').text)
        #        bytesValue = byte2int(nodeBytes)
        #        if bytesValue & (1 << defOffset):
        #            nodeValue += (' ' + defName + ':X')
        #        else:
        #            nodeValue += (' ' + defName + ':_')
        #nodeValue += ']'

    elif vType == 'ENUM':
        nodeEnum = varNode.find('v_enum')
        enumList = [eitem.text for eitem in nodeEnum.findall('v_enumname')]
        nodeValue = enumList[byte2int(nodeBytes) % len(enumList)]
    else:
        nodeValue = '<' + vType + '>'
    return nodeValue


def buildBaseRecord(binRec, secAllModules):
    for nodeMod in secAllModules:
        if nodeMod is None:
            continue

        # m_name = nodeMod.find('m_name')
        m_start = int(nodeMod.find('m_start').text)
        nodeVars = nodeMod.find('variables')
        if nodeVars is None:
            continue
        varList = nodeVars.findall('variable')
        for varNode in varList:
            # v_name = varNode.find('v_name').text
            v_start = int(varNode.find('v_start').text)
            bitStart = m_start + v_start
            v_size = int(varNode.find('v_size').text)

            byteStart = bitStart / 8
            b_size = v_size / 8
            if b_size <= 0:
                b_size = 1

            nodeString = binRec[byteStart: byteStart + b_size]
            gBaseRecord[bitStart] = nodeString

    return True


def sameWithBaseRecord(bitStart, nodeString):
    global gBaseRecord

    if bitStart in gBaseRecord:
        return (gBaseRecord[bitStart] == nodeString)
    else:
        return False


def parseBitInByte(byteChar, bitStart):
    bitInByte = bitStart % 8
    if ((ord(byteChar) & (1 << bitInByte)) > 0):
        return 'X'
    else:
        return '_'

# parse a record, using the xml setting

def xmlExtractStruct(binRecord, variableList, mStart):
    for varNode in variableList:
        v_name = varNode.find('v_name').text
        v_size = varNode.find('v_size').text
        v_start = int(varNode.find('v_start').text)
        bitStart = mStart + v_start

        v_size = int(varNode.find('v_size').text)
        v_type = varNode.find('v_type').text

        # extract binRecord from bitStart by v_size, 

        byteStart = bitStart / 8
        b_size = v_size / 8
        if (b_size <= 0):
            b_size = 1

        nodeString = binRecord[byteStart: byteStart + b_size]
        if len(nodeString) <= 0:
            print 'Null nodeString: v_name=%s, byteStart=%d, binRecord len=%d' % (
            v_name, byteStart, len(binRecord))
            break

        if v_size == 1:
            nodeValue = parseBitInByte(nodeString, bitStart)
        else:
            nodeValue = parseNodeByte(varNode, nodeString, v_type)

        global RESULT
        RESULT.append(nodeValue)
        #outputLine = '\t' + v_name + '\t' + v_type + '\t' + str(v_size) + '\t' + nodeValue
        #print outputLine


# process the global section, only one

def xmlProcessGlobal(binRecord, secGlobal):
    varRoot = secGlobal.find('variables')
    g_start = secGlobal.find('g_start').text
    if not g_start:
        return

    gStart = int(g_start)

    #print "\n====> GLOBAL\n"
    if len(varRoot):
        varList = varRoot.findall('variable')
        xmlExtractStruct(binRecord, varList, gStart)
        #print "\n<==== GLOBAL"
        return True
    else:
        return False


# process the modules, one by one

def xmlProcessModules(binRecord, secAllModules):
    for nodeMod in secAllModules:
        if len(nodeMod):
            varRoot = nodeMod.find('variables')
            m_name = nodeMod.find('m_name')
            m_start = nodeMod.find('m_start').text
            #print '\n====> %s \n' % m_name.text

            if len(varRoot):
                listVar = varRoot.findall('variable')
                xmlExtractStruct(binRecord, listVar, int(m_start))
            else:
                pass
            #print '\n<==== %s ' % m_name.text
        else:
            pass
    return True


# Error handling

def sysExit(reason):
    print 'xxxxxxxxxxxxxxxxxxxxxxxx File not ready. Error No: %d ' % reason
    sys.exit()


# main procedure

def parseBin():
    if not loadXmlFile('ato_f.xml'):
        sysExit(3)
    fpBin = open('../test.bin', 'rb')
    while True:
        data = fpBin.read(G_RECORD_LEN)
        # init the base record dict.
        #if G_DIFFVIEW:
        global gBaseRecord, RESULT
        gBaseRecord = {}
        RESULT = []
        buildBaseRecord(data, xmlAllModules)

        #startTime = datetime.now()
        #s = '======= Start record: %d time %s =======\n' % (0, startTime)
        #print s

        if len(data) > 0:
            xmlProcessGlobal(data, xmlGlobal)
            xmlProcessModules(data, xmlAllModules)

        s = "','".join(RESULT)

        db.save(s)

    #endTime = datetime.now()

    #s = (u'\n=================== Done. ===================\n' \
    #     + u'开始时间:    %s 	开始记录: %d \n' % (startTime, 0) \
    #     + u'结束时间:    %s 	记录个数：%d \n' % (endTime, 1) \
    #     + u'转换用时:    %s ' % str(endTime - startTime))
#
    #print s

if __name__ == '__main__':
    parseBin()
