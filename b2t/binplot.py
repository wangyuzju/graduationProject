#!/usr/bin/python
# -*- coding: utf-8 -*-

# The really simple Python version of Qwt-5.0.0/examples/simple


import platform
import sys
import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import PyQt4.Qwt5 as Qwt

from b2t2 import Bin2Txt
import qrc_resources


__version__ = "0.1.1"

CURVE_LIST=(
    (u'列车速度(KPH*10)', Qt.red, 1),
    (u'牵引制动输出', Qt.magenta, 1),
    (u'ATP EB速度(mm/s)', Qt.green, 0.036),
    (u'目标速度(KPH*10)', Qt.blue, 1),
    (u'加速度(mm/s)', Qt.gray, 1)
    )

X_AXIS = u'列车绝对位移(m)'

BIN_FILENAME = 'ATC1.0.0_CCATO01R_20120828_f.bin'


class Spy(QObject):
    
    def __init__(self, parent):
        QObject.__init__(self, parent)
        parent.setMouseTracking(True)
        parent.installEventFilter(self)

    # __init__()

    def eventFilter(self, _, event):
        if event.type() == QEvent.MouseMove:
            self.emit(SIGNAL("MouseMove"), event.pos())
        return False

    # eventFilter()

# class Spy

class SimplePlot(QMainWindow):

    def __init__(self, parent=None):
        super(SimplePlot, self).__init__(parent)

        self.buildStatusBar()
        self.buildMenu()
        self.restoreSetting()

        self.buildPlot()

        self.binFilename = ''

    def buildStatusBar(self):
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)

    def buildMenu(self):
        fileOpenAction = self.createAction("&Open...", self.fileOpen,
                QKeySequence.Open, "fileopen",
                "Open an existing  bin data file")

        fileQuitAction = self.createAction("&Quit", self.close,
                "Ctrl+Q", "filequit", "Close the application")

        helpAboutAction = self.createAction("&About", self.helpAbout,
                "F1", "editedit", tip="About the application")

        fileMenu = self.menuBar().addMenu("&File")
        self.addActions(fileMenu, ( fileOpenAction,
                None, fileQuitAction))
        helpMenu = self.menuBar().addMenu("&Help")
        self.addActions(helpMenu, (None, helpAboutAction))

        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        self.addActions(fileToolbar, ( fileOpenAction, None, helpAboutAction ))
        
    def restoreSetting(self):
        settings = QSettings()
        size = settings.value("MainWindow/Size",
                              QVariant(QSize(600, 500))).toSize()
        self.resize(size)
        position = settings.value("MainWindow/Position",
                                  QVariant(QPoint(0, 0))).toPoint()
        self.move(position)
        self.restoreState(
                settings.value("MainWindow/State").toByteArray())
        
        self.setWindowTitle("binplot - ato@insigma")
        # QTimer.singleShot(0, self.loadInitialFile)

    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action


    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)


    def closeEvent(self, event):
        settings = QSettings()
        settings.setValue("LastFile",
                QVariant(self.binFilename))
        settings.setValue("MainWindow/Size", QVariant(self.size()))
        settings.setValue("MainWindow/Position",
                QVariant(self.pos()))
        settings.setValue("MainWindow/State",
                QVariant(self.saveState()))


    def buildPlot(self):
        # Initial= Qwtize a QwPlot central widget
        self.plot = Qwt.QwtPlot(self)
        # self.plot.setTitle('bin2plot')

        self.plot.setCanvasBackground(Qt.white)

        self.plot.plotLayout().setCanvasMargin(0)
        self.plot.plotLayout().setAlignCanvasToScales(True)
        self.setCentralWidget(self.plot)

        grid = Qwt.QwtPlotGrid()
        pen = QPen(Qt.DotLine)
        pen.setColor(Qt.black)
        pen.setWidth(0)
        grid.setPen(pen)
        grid.attach(self.plot)

        self.__initTracking()
        self.__initZooming()

    def initPlotData(self):
        self.plot.Clear()

    def __initTracking(self):
        """Initialize tracking
        """        

        self.connect(Spy(self.plot.canvas()),
                     SIGNAL("MouseMove"),
                     self.showCoordinates) 

        self.statusBar().showMessage(
            'atoTeam@insigma')

    def showCoordinates(self, position):
        self.statusBar().showMessage(
            'x = %d, y = %d'
            % (self.plot.invTransform(Qwt.QwtPlot.xBottom, position.x()),
               self.plot.invTransform(Qwt.QwtPlot.yLeft, position.y())))

    def __initZooming(self):
        """Initialize zooming
        """

        self.zoomer = Qwt.QwtPlotZoomer(Qwt.QwtPlot.xBottom,
                                        Qwt.QwtPlot.yLeft,
                                        Qwt.QwtPicker.DragSelection,
                                        Qwt.QwtPicker.AlwaysOff,
                                        self.plot.canvas())
        self.zoomer.setRubberBandPen(QPen(Qt.black))

    def setZoomerMousePattern(self, index):
        """Set the mouse zoomer pattern.
        """

        if index == 0:
            pattern = [
                Qwt.QwtEventPattern.MousePattern(Qt.LeftButton,
                                                 Qt.NoModifier),
                Qwt.QwtEventPattern.MousePattern(Qt.MidButton,
                                                 Qt.NoModifier),
                Qwt.QwtEventPattern.MousePattern(Qt.RightButton,
                                                 Qt.NoModifier),
                Qwt.QwtEventPattern.MousePattern(Qt.LeftButton,
                                                 Qt.ShiftModifier),
                Qwt.QwtEventPattern.MousePattern(Qt.MidButton,
                                                 Qt.ShiftModifier),
                Qwt.QwtEventPattern.MousePattern(Qt.RightButton,
                                                 Qt.ShiftModifier),
                ]
            self.zoomer.setMousePattern(pattern)
        elif index in (1, 2, 3):
            self.zoomer.initMousePattern(index)
        else:
            raise ValueError, 'index must be in (0, 1, 2, 3)'

    def helpAbout(self):
        QMessageBox.about(self, "binplot - About",
                """<b>binplot</b> v %s
                <p>Copyright &copy; 2012 ato@insigma team.<br> 
                All rights reserved.
                <p>This application can read data from the 
                ato '.bin' file, and plot the curves. 
                <p>Python %s - Qt %s - PyQt %s on %s""" % (
                __version__, platform.python_version(),
                QT_VERSION_STR, PYQT_VERSION_STR, platform.system()))


    def fileOpen(self):
        path = QFileInfo(self.binFilename).path() \
                if len(self.binFilename) > 0  else "."
        fname = QFileDialog.getOpenFileName(self,
                    "bin files - Load Ato Log Data", path,
                    "Ato Log data files (%s)" % \
                    ("*.bin"))
        if not fname.isEmpty():
            # ok, msg = self.movies.load(fname)
            # self.statusBar().showMessage(msg, 5000)
            # self.updateTable()
            self.binFilename = fname
            loadnum = self.loadData(fname, 0, 0) #
            self.statusBar().showMessage(str(loadnum), 5000)

        

    def clearZoomStack(self):
        """Auto scale and clear the zoom stack
        """

        self.plot.setAxisAutoScale(Qwt.QwtPlot.xBottom)
        self.plot.setAxisAutoScale(Qwt.QwtPlot.yLeft)
        self.plot.replot()
        self.zoomer.setZoomBase()

    # clearZoomStack()

    def loadBinData(self, filename, start, num):
        test = Bin2Txt()

        # default use 'ato_f.xml' which is writen in b2t2.py
        # to change the default xml file, write like this:
        # recno = test.initFile(filename, 'ato_p.xml')
        recno = test.initFile(filename)
        if num == 0:
            num = recno

        fmt = test.makeRecordFmt()
        vnameList = test.globalVnameList # (v_name, v_type)
        
        # curveData = [[0]]*len(CURVE_LIST)
        curveData = []
        xdata = []
        indexes = []
        for idx in range(0, len(CURVE_LIST)):
            curveName = [x[0] for x in vnameList].index(CURVE_LIST[idx][0])
            indexes.append(curveName)
            a = []
            curveData.append(a)

        xidx = [x[0] for x in vnameList].index(X_AXIS)

        endRec = start+num
        if endRec > recno: endRec = recno
        for i in xrange(start, endRec):
            rec = test.loadBinRecord(i)
            if rec is None: break
            varData = test.parseRecordFmt(rec, fmt)
            for idx in range(0, len(CURVE_LIST)):
                #print varData[indexes[idx]]
                #print idx, curveData[idx], indexes[idx],  varData[indexes[idx]]
                curveData[idx].append(varData[indexes[idx]] * CURVE_LIST[idx][2])
            xdata.append(varData[xidx])

        num = i - start + 1

        return (num, curveData, xdata)

    def removeCurves(self):
      for i in self.plot.itemList():
        if isinstance(i, Qwt.QwtPlotCurve) \
            or isinstance(i, Qwt.QwtPlotMarker) :
          i.detach()


    # class Plot
    def loadData(self, binFilename, start, num):
        # make a QwtPlot widget

        self.removeCurves()
        
        self.plot.insertLegend(Qwt.QwtLegend(), Qwt.QwtPlot.RightLegend)
            
        # set axis titles
        self.plot.setAxisTitle(Qwt.QwtPlot.xBottom, 'cycle -->')
        self.plot.setAxisTitle(Qwt.QwtPlot.yLeft, 'speed/command -->')

        loadnum, curveData, xdata = self.loadBinData(binFilename, start, num)

        # print curveData
        # x = range(start, start+num)
        for i, curve in enumerate(CURVE_LIST):
            aCurve = Qwt.QwtPlotCurve(curve[0])
            aCurve.setPen(QPen(curve[1]))
            aCurve.setData(xdata, curveData[i])
            aCurve.attach(self.plot)

        mY = Qwt.QwtPlotMarker()
        mY.setLabel(Qwt.QwtText('Total: %d' % loadnum))
        mY.setLabelAlignment(Qt.AlignRight | Qt.AlignTop)
        mY.setLineStyle(Qwt.QwtPlotMarker.HLine)
        mY.setYValue(0.0)
        mY.attach(self.plot)

        self.plot.replot()

        self.clearZoomStack()

        return loadnum


def main(args):
    app = QApplication(args)
    app.setOrganizationName("ato@INSIGMA Team.")
    app.setOrganizationDomain("insigma.com")
    app.setApplicationName("binplot")
    app.setWindowIcon(QIcon(":/icon.png"))
    form = SimplePlot()
    form.show()
    app.exec_()

# main()


# Admire
if __name__ == '__main__':

    main(sys.argv)
        

# Local Variables: ***
# mode: python ***
# End: ***



