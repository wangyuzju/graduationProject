#coding: utf-8
import json
import datetime
from b2t2 import Bin2Txt
import db

CURVE_LIST=(
    (u'列车速度(KPH*10)', 1),
    (u'牵引制动输出', 1),
    (u'ATP EB速度(mm/s)', 0.036),
    (u'目标速度(KPH*10)',1),
    (u'加速度(mm/s)',1)
)

X_AXIS = u'列车绝对位移(m)'


def var_dump(obj):
    print json.dumps(obj, encoding="utf-8", ensure_ascii=False)


def loadBinDate():
    filename = 'data.bin'
    test = Bin2Txt()

    # default use 'ato_f.xml' which is writen in b2t2.py
    # to change the default xml file, write like this:
    # recno = test.initFile(filename, 'ato_p.xml')
    recno = test.initFile(filename)

    #generate formatstring from 'ato_f.xml' file
    fmt = test.makeRecordFmt()
    vNameList = test.globalVnameList  # (v_name, v_type)

    #startTime = datetime.now()
    for i in xrange(0, recno):
        rec = test.loadBinRecord(i)
        if rec is None: 
            break
        varData = test.parseRecordFmt(rec, fmt)
        record = []
        for item in varData:
            if type(item) is str:
                item = "'" + item.encode('hex') + "'"
            else:
                item = str(item)
            record.append(item)
        s = ",".join(record)
        db.save(s)
    db.safe_exit()

if __name__ == '__main__':
    loadBinDate()
