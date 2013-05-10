#!/usr/bin/python
# -*- coding: utf-8 -*-

''' 转换程序 bin+xml=>txt
....从ATO运行时生成的bin格式的log，与atoviewer配套的xml结合，生成txt形式的文件

....用法：./bin2txt.py [<atolog.bin> <atoxml.xml> [<start> <num>]]
....生成：<atolog.txt>

....* .bin文件和.xml文件如果没有在命令行给出则会提示输入
....* 参数中指定<start>为起始记录号，<num>为要转换的记录个数
....  不指定时从第0个记录开始24000个记录，即约1个小时的数据
....* 生成的文件是utf-8编码

....o 生成的txt文件中:
........圆括号中如：(159) 中的数据是10进制
........方括号中如：[19ff]中数据是十六进制
........位数据和事件数据下划线_表示0，X表示1

....o 使用前需要修改代码中以下行，对应bin文件中一个记录的大小：

....# the length of ONE record in the .bin file
....G_RECORD_LEN = 187

'''

import os
import sys
import struct
import xml.etree.ElementTree as ET


# the length of ONE record in the .bin file

# G_RECORD_LEN = 187
# G_XML_FILE   = 'ato_p.xml'

G_XML_FILE = 'ato_f.xml'


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


PrintType = enum('DEC', 'HEX', 'BIT', 'BITCLOSE', 'ENUM', 'UNKOWN')


class Bin2Txt:
    # re-calculated when loadXmlFile()
    G_RECORD_LEN = 0

    def __init__(self):
        pass

    def __delete__(self):
        if self.fpBin:
            self.fpBin.close()

    def loadXmlFile(self, fileName):
        self.xmlRoot = ET.parse(fileName).getroot()

        self.xmlGlobal = self.xmlRoot.find('global')
        self.xmlAllModules = self.xmlRoot.findall('module')

        fmt = self.makeRecordFmt()
        self.G_RECORD_LEN = struct.calcsize(fmt)

        return self.xmlRoot is not None

    def parseBitInByte(self, byteChar, bitStart):
        bitInByte = bitStart % 8
        if ord(byteChar) & 1 << bitInByte > 0:
            return 'X'
        else:
            return '_'

            #=======================================================

    def makeNodeFmt(self, varNode):
        v_name = varNode.find('v_name').text
        v_type = varNode.find('v_type').text
        v_start = int(varNode.find('v_start').text)
        v_size = int(varNode.find('v_size').text)

        # ptype = PrintType.DEC

        if v_size % 8 > 0:
            ptype = PrintType.BIT
            fmtString = ''
            return (v_name, PrintType.BIT, v_size, fmtString)

        if v_type == 'VARS_DEC':
            if v_size == 32:
                ptype = PrintType.DEC
                fmtString = 'l'
            elif v_size == 16:
                ptype = PrintType.DEC
                fmtString = 'h'
            elif v_size == 8:
                ptype = PrintType.DEC
                fmtString = 'b'
            else:
                ptype = PrintType.HEX
                fmtString = '%ds' % (v_size / 8)
        elif v_type == 'VARS_CYCLE':
            ptype = PrintType.DEC
            fmtString = 'L'
        elif v_type == 'VARS_HEX':
            ptype = PrintType.HEX
            fmtString = '%ds' % (v_size / 8)
        elif v_type == 'VARS_EVENT':
            ptype = PrintType.HEX
            fmtString = '%ds' % (v_size / 8)
        elif v_type == 'ENUM':
            assert (v_size >= 8) # protected in L:152 
            if v_size == 8:
                ptype = PrintType.ENUM
                fmtString = 'c'
            else:
                ptype = PrintType.ENUM
                fmtString = '%ds' % (v_size / 8)
        else:
            ptype = PrintType.HEX
            fmtString = '%ds' % (v_size / 8)

        return (v_name, ptype, v_size, fmtString)

    #=======================================================
    def makeVarListTuple(self, varListRoot):
        sectionFmtStr = ''
        sectionVname = []
        bitGroup = 'B'
        bitCount = 0
        variableList = varListRoot.findall('variable')
        for varNode in variableList:
        # struct_size = struct.calcsize(self.globalFormatStr)
            (strName, ptype, vsize, strFmt) = self.makeNodeFmt(varNode)
            if ptype == PrintType.BIT:
                bitGroup = bitGroup + '|' + strName
                bitCount += vsize
                if bitCount >= 8:
                    sectionVname.append((bitGroup, PrintType.BIT))
                    sectionFmtStr += 'c'
                    bitCount -= 8
                    bitGroup = 'B'
            else:
                if bitCount > 0:
                    sectionVname.append((bitGroup, PrintType.BIT))
                    sectionFmtStr += 'c'
                    bitCount = 0
                    bitGroup = 'B'
                sectionVname.append((strName, ptype))
                sectionFmtStr += strFmt
        return (sectionFmtStr, sectionVname)

    # generate the class-global dict  self.globalFormatDict
    # GLOBAL (0, 41, '>L4s4slll4slllc', [(u'ATO\u5468\u671f', 1), ....])
    def makeRecordFmtDict(self):
        self.globalFormatDict = {}
        self.globalDictKeys = ['GLOBAL']

        varListRoot = self.xmlGlobal.find('variables')
        if varListRoot is not None:
            g_start = int(self.xmlGlobal.find('g_start').text)
            g_size = int(self.xmlGlobal.find('g_size').text)

            (sectionFmtStr, sectionVnames) = self.makeVarListTuple(varListRoot)
            self.globalFormatDict['GLOBAL'] = (
                g_start / 8, g_size / 8, sectionFmtStr, sectionVnames)

        for nodeMod in self.xmlAllModules:
            m_name = nodeMod.find('m_name').text
            self.globalDictKeys.append(m_name)

            m_start = int(nodeMod.find('m_start').text)
            m_size = int(nodeMod.find('m_size').text)

            varListRoot = nodeMod.find('variables')
            if varListRoot is None:
                continue

            (sectionFmtStr, sectionVnames) = self.makeVarListTuple(varListRoot)
            self.globalFormatDict[m_name] = (
                m_start / 8, m_size / 8, sectionFmtStr, sectionVnames)

        return self.globalFormatDict

    # GLOBAL (0, 41, '>L4s4slll4slllc', [u'ATO\u5468\u671f', ....])
    # tuple[] = (m_start, m_size, fmt, v_name[])
    def parseRecordSection(self, sectionTuple, binRec):
        recSection = binRec[sectionTuple[0]:sectionTuple[0] + sectionTuple[1]]
        secVarList = struct.unpack('>' + sectionTuple[2], recSection)
        return secVarList

    #=======================================================
    def getNodeFormatStr(self, varNode):
        v_name = varNode.find('v_name').text
        v_type = varNode.find('v_type').text
        v_start = int(varNode.find('v_start').text)
        v_size = int(varNode.find('v_size').text)

        preStr = ''
        if (self.global_bit_count > 0) and (v_size > 1):
            preStr = 'c'
            self.global_bit_count = 0

        if v_type == 'VARS_DEC':
            if v_size == 32:
                fmtString = 'l'
            elif v_size == 8:
                fmtString = 'c'
            elif v_size < 8:
                fmtString = ''
                self.global_bit_count += v_size
                if self.global_bit_count >= 8:
                    fmtString = 'c'
                    self.global_bit_count -= 8
            else:
                fmtString = '%ds' % (v_size / 8)
        elif v_type == 'VARS_CYCLE':
            if v_size == 32:
                fmtString = 'L'
        elif v_type == 'VARS_HEX':
            fmtString = '%ds' % (v_size / 8)
        elif v_type == 'VARS_EVENT':
            fmtString = '%ds' % (v_size / 8)
        elif v_type == 'ENUM':
            if v_size == 8:
                fmtString = 'c'
            else:
                fmtString = '%ds' % (v_size / 8)
        else:
            fmtString = '%ds' % (v_size / 8)

        fmtString = preStr + fmtString
        return (v_name, fmtString)

    # generate the class-global Fmt string: 
    # self.globalFormatStr = '>L4s4slll4sl....'
    # self.globalVnameList = ['ATO周期', ....]
    def makeRecordFmt(self):
        self.globalFormatStr = '>'
        self.globalVnameList = []
        # self.global_bit_count = 0

        varListRoot = self.xmlGlobal.find('variables')
        if varListRoot is not None:
            g_start = int(self.xmlGlobal.find('g_start').text)
            g_size = int(self.xmlGlobal.find('g_size').text)

            (sectionFmtStr, sectionVnames) = self.makeVarListTuple(varListRoot)
            self.globalVnameList += sectionVnames
            self.globalFormatStr += sectionFmtStr

        for nodeMod in self.xmlAllModules:
            m_name = nodeMod.find('m_name').text
            m_start = int(nodeMod.find('m_start').text)
            m_size = int(nodeMod.find('m_size').text)

            varListRoot = nodeMod.find('variables')
            if varListRoot is None:
                continue

            (sectionFmtStr, sectionVnames) = self.makeVarListTuple(varListRoot)
            self.globalVnameList += sectionVnames
            self.globalFormatStr += sectionFmtStr

        return self.globalFormatStr


    def parseRecordFmt(self, binRec, fmt):
        if len(binRec) == self.G_RECORD_LEN:
            varList = struct.unpack(fmt, binRec)
            return varList

            # print varList

            #=======================================================

    def byte2int(self, bytes):
        # return int(bytes.encode('hex'), 16)
        if len(bytes) == 4:
            return struct.unpack(">L", bytes)[0]
        elif len(bytes) == 1:
            return ord(bytes[0])
        else:
            return int(bytes.encode('hex'), 16)
            #return struct.unpack(">L", bytes)[0]
            # ?not implemented :return int.from_bytes(bytes, 'big')

    def parseNodeByte(self, varNode, nodeBytes, vType):
        if vType == 'VARS_DEC':
            nodeValue = self.byte2int(nodeBytes)
        elif vType == 'VARS_CYCLE':
            nodeValue = self.byte2int(nodeBytes)
        elif vType == 'VARS_HEX':
            nodeValue = self.byte2int(nodeBytes)
        elif vType == 'VARS_EVENT':
            nodeValue = self.byte2int(nodeBytes)
        elif vType == 'ENUM':
            nodeValue = self.byte2int(nodeBytes)
        else:
            nodeValue = 0xffffff

        return nodeValue


    # parse a list of varibles
    def getVarListData(self,
                       binRecord,
                       moduleNode,
                       m_start,
                       dictOutput,
    ):
        variableList = moduleNode.findall('variable')
        for varNode in variableList:
            v_name = varNode.find('v_name').text
            v_start = int(varNode.find('v_start').text)
            bitStart = m_start + v_start

            v_size = int(varNode.find('v_size').text)
            v_type = varNode.find('v_type').text

            # extract binRecord from bitStart by v_size,

            byteStart = bitStart / 8
            b_size = v_size / 8
            if b_size <= 0:
                b_size = 1

            nodeString = binRecord[byteStart:byteStart + b_size]
            if len(nodeString) <= 0:
                print 'Null nodeString: v_name=%s, byteStart=%d, binRecord len=%d' \
                      % (v_name, byteStart, len(binRecord))
                break

            if v_size == 1:
                nodeValue = self.parseBitInByte(nodeString, bitStart)
            else:
                nodeValue = self.parseNodeByte(varNode, nodeString, v_type)

            dictOutput[v_name] = nodeValue

    # parse a bin record, refer to global vars:xmlGlobal, xmlAllModules
    def parseRecord(self, binRec):
        if len(binRec) < 0:
            return None

        recDataList = {}
        # xml global section 
        varListRoot = self.xmlGlobal.find('variables')
        if varListRoot is not None:
            g_start = int(self.xmlGlobal.find('g_start').text)
            self.getVarListData(binRec, varListRoot, g_start, recDataList)

        # xml modules sections
        for nodeMod in self.xmlAllModules:
            varListRoot = nodeMod.find('variables')
            if varListRoot is None:
                continue

            # m_name = nodeMod.find('m_name')
            m_start = nodeMod.find('m_start').text

            self.getVarListData(binRec, varListRoot, int(m_start), recDataList)

        return recDataList

    #=======================================================
    # load a record from <fpBin>, index of <recNo>
    def loadBinRecord(self, recNo):
        self.fpBin.seek(self.G_RECORD_LEN * recNo)
        rec = self.fpBin.read(self.G_RECORD_LEN)
        if (len(rec) > 0):
            return rec
        else:
            return None

    def initFile(self, binFilename, xmlFile=G_XML_FILE):
        if not self.loadXmlFile(xmlFile):
            return -2

        filesize = os.path.getsize(binFilename)
        self.fpBin = open(binFilename, 'rb')
        if not self.fpBin:
            return -1

        return filesize / self.G_RECORD_LEN

    def loadMain(self, binFilename, fromIndex, numRec):
        if self.initFiles(binFilename) <= 0:
            return False
            # startTime = datetime.now()

        for i in xrange(fromIndex, fromIndex + numRec):
            rec = self.loadBinRecord(i)
            recData = self.parseBinRecord(rec)


        # endTime = datetime.now()

        self.fpBin.close()
        return True

