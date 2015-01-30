__author__ = 'yilu'

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import PyQt4.Qwt5 as Qwt
import math
import numpy as np


class ThrottlePositionTag(QWidget):
    def __init__(self, reactor):
        super(ThrottlePositionTag, self).__init__()
        self.reactor = reactor
        self.main_layout = QHBoxLayout()

        # left_scale = Qwt.QwtScaleWidget()
        # left_scale.setAlignment(Qwt.QwtScaleDraw.LeftScale)
        # left_scale.setTitle("Position")
        # left_scale.setFixedWidth(30)
        # self.main_layout.addWidget(left_scale)

        self.plot = Qwt.QwtPlot(self)
        self.plot.setCanvasBackground(Qt.black)
        self.plot.setAxisTitle(Qwt.QwtPlot.xBottom, 'Time')
        self.plot.setAxisScale(Qwt.QwtPlot.xBottom, 0, 10, 1)
        self.plot.setAxisTitle(Qwt.QwtPlot.yLeft, 'Position')
        self.plot.setAxisScale(Qwt.QwtPlot.yLeft, 0, 1, 0.1)
        self.plot.replot()

        self.curve = Qwt.QwtPlotCurve('')
        self.curve.setRenderHint(Qwt.QwtPlotItem.RenderAntialiased)
        pen = QPen(QColor('limegreen'))
        pen.setWidth(2)
        self.curve.setPen(pen)
        self.curve.attach(self.plot)

        self.currentMarker = Qwt.QwtPlotMarker()
        symbol = Qwt.QwtSymbol(Qwt.QwtSymbol.Cross, QBrush(Qt.yellow), QPen(Qt.red), QSize(7, 7))
        self.currentMarker.setSymbol(symbol)
        self.currentMarker.setLineStyle(Qwt.QwtPlotMarker.NoLine)
        self.currentMarker.attach(self.plot)

        scroll = QScrollArea()
        scroll.setWidget(self.plot)
        # plot.setFixedWidth(2000)
        scroll.setWidgetResizable(True)
        # scroll.setFixedHeight(500)
        # scroll.setBaseSize(300, 500)
        self.main_layout.addWidget(scroll)
        self.setLayout(self.main_layout)

        self.xdata = []
        self.ydata = []
        # xdata = np.arange(0, 40, 0.1)
        # ydata = map(lambda a: math.sin(a) * (math.e**(-0.1*a)), xdata)
        # self.curve.setData(xdata, ydata)

    def got_new_data(self, packet):
        new_x = float(packet["time"]) / 10
        new_y = packet["data"]
        self.xdata.append(new_x)
        self.ydata.append(new_y)
        while len(self.xdata) > 100:
            self.xdata.pop(0)
            self.ydata.pop(0)
        self.plot.setAxisScale(Qwt.QwtPlot.xBottom, self.xdata[0], self.xdata[0] + 10, 1)
        self.curve.setData(self.xdata, self.ydata)
        self.currentMarker.setXValue(new_x)
        self.currentMarker.setYValue(new_y)
        self.currentMarker.attach(self.plot)
        self.plot.replot()
        self.reactor.callLater(0.5, self.remove_current_marker)

    def remove_current_marker(self):
        self.currentMarker.detach()
        self.plot.replot()