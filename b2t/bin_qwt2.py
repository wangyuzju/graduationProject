# -*- coding: utf-8 -*-
#


"""CurveDialog test"""

SHOW = True # Show test in GUI-based test launcher

from guidata.qt.QtGui import QFont

from guiqwt.plot import CurveDialog
from guiqwt.builder import make
from b2t2 import Bin2Txt

def plot(*items):
    win = CurveDialog(edit=False, toolbar=True, wintitle="CurveDialog test",
                      options=dict(title="Title", xlabel="xlabel",
                                   ylabel="ylabel"))
    plot = win.get_plot()
    for item in items:
        plot.add_item(item)
    plot.set_axis_font("left", QFont("Courier"))
    win.get_itemlist_panel().show()
    plot.set_items_readonly(False)
    win.show()
    win.exec_()

def loadBinData(filename, start_rec, num):
    test = Bin2Txt()   

    recno = test.initFile(filename) 
    fmt = test.makeRecordFmt()
    vnameList = test.globalVnameList # (v_name, v_type)
    
    index_y1 = [x[0] for x in vnameList].index(u'列车当前速度2(KPH*10)')
    index_y2 = [x[0] for x in vnameList].index(u'列车EB速度(KPH*10)')
    
    # i1 = [i for i, v in enumerate(vnameList) if v[0] == u'列车当前速度(KPH*10)']
    # i2 = [i for i, v in enumerate(vnameList) if v[0] == u'多普勒速度']


    y1 = []
    y2 = []
    for i in xrange(start_rec, start_rec+num):
        rec = test.loadBinRecord(i)
        varData = test.parseRecordFmt(rec, fmt)
        y1.append( varData[index_y1] )
        y2.append( varData[index_y2] )

    return ((vnameList[index_y1][0],vnameList[index_y2][0]), (y1, y2))

def test():
    """Test"""
    # -- Create QApplication
    import guidata
    _app = guidata.qapplication()
    # --
    # from numpy import linspace, sin
    #x = linspace(-10, 10, 200)

    start_rec = 819
    num_rec = 10000

    x = range(start_rec, start_rec + num_rec)
    vname, y = loadBinData('ATOLOG_01R_1.atp', start_rec, num_rec)
    plot(make.curve(x, y[0], title=vname[0], color="b"),
         make.curve(x, y[1], title=vname[1], color="g"),
         #make.curve(x, sin(2*y), color="r"),
         #make.merror(x, y/2, dy),
         #make.label("Relative position <b>outside</b>",
         #           (x[0], y[0]), (-10, -10), "BR"),
         #make.label("Relative position <i>inside</i>",
         #           (x[0], y[0]), (10, 10), "TL"),
         #make.label("Absolute position", "R", (0,0), "R"),
         make.legend("TR"),
         #make.marker(position=(5., .8), label_cb=lambda x, y: u"A = %.2f" % x,
         #            markerstyle="|", movable=False)
         )

if __name__ == "__main__":
    test()
