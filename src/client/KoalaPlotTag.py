__author__ = 'yilu'

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import PyQt4.Qwt5 as Qwt
# import KoalaSteeringWheelWidget
import math
import numpy as np


class KoalaPlotBaseTag(QWidget):
    def __init__(self, reactor, x_axis_name=None, y_axis_name=None, x_scale=None, y_scale=None):
        if x_axis_name is None:
            x_axis_name = "Time"
        if y_axis_name is None:
            y_axis_name = "Dummy Y Label"
        if x_scale is None:
            x_scale = 10
        if y_scale is None:
            y_scale = 1000

        super(KoalaPlotBaseTag, self).__init__()
        self.reactor = reactor
        self.main_layout = QHBoxLayout()

        self.leftAxis = Qwt.QwtPlot(self)
        self.leftAxis.setCanvasBackground(Qt.black)
        self.leftAxis.setAxisTitle(Qwt.QwtPlot.xBottom, x_axis_name)
        self.leftAxis.setAxisScale(Qwt.QwtPlot.xBottom, 0, x_scale, x_scale)
        self.leftAxis.setAxisTitle(Qwt.QwtPlot.yLeft, y_axis_name)
        self.leftAxis.setAxisScale(Qwt.QwtPlot.yLeft, 0, y_scale, y_scale)
        self.leftAxis.setFixedWidth(53)
        self.main_layout.addWidget(self.leftAxis)

        self.plot = Qwt.QwtPlot(self)
        self.plot.setCanvasBackground(Qt.black)
        self.plot.setAxisTitle(Qwt.QwtPlot.xBottom, x_axis_name)
        self.plot.setAxisScale(Qwt.QwtPlot.xBottom, 0, x_scale, x_scale)
        self.plot.enableAxis(Qwt.QwtPlot.yLeft, False)
        self.plot.replot()

        self.curvet1 = Qwt.QwtPlotCurve('')
        # self.curvet1.setRenderHint(Qwt.QwtPlotItem.RenderAntialiased)
        pen = QPen(QColor('limegreen'))
        pen.setWidth(0.5)
        self.curvet1.setPen(pen)
        self.curvet1.attach(self.plot)

        self.dotst1 = Qwt.QwtPlotCurve('')
        # self.dotst1.setRenderHint(Qwt.QwtPlotItem.RenderAntialiased)
        self.dotst1.setStyle(Qwt.QwtPlotCurve.Dots)
        dots_pen = QPen(QColor('yellow'))
        dots_pen.setWidth(3)
        self.dotst1.setPen(dots_pen)
        self.dotst1.attach(self.plot)

        self.curvet2 = Qwt.QwtPlotCurve('')
        # self.curvet2.setRenderHint(Qwt.QwtPlotItem.RenderAntialiased)
        # pen = QPen(QColor('blue'))
        pen = QPen(QColor(116, 242, 242))
        pen.setWidth(0.5)
        self.curvet2.setPen(pen)
        self.curvet2.attach(self.plot)

        self.dotst2 = Qwt.QwtPlotCurve('')
        # self.dotst2.setRenderHint(Qwt.QwtPlotItem.RenderAntialiased)
        self.dotst2.setStyle(Qwt.QwtPlotCurve.Dots)
        dots_pen2 = QPen(QColor(242, 116, 240))
        dots_pen2.setWidth(3)
        self.dotst2.setPen(dots_pen2)
        self.dotst2.attach(self.plot)

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
        self.t1data = []
        self.t2data = []
        # xdata = np.arange(0, 40, 0.1)
        # ydata = map(lambda a: math.sin(a) * (math.e**(-0.1*a)), xdata)
        # self.curve.setData(xdata, ydata)

    # def got_new_data(self, packet):
    #     new_x = float(packet["time"]) / 1000
    #     new_t1 = float(packet["t1"])
    #     new_t2 = float(packet["t2"])
    #     if new_t2 > 900:
    #         print "x: %s, throttle2: %s" % (new_x, new_t2)
    #     self.xdata.append(new_x)
    #     self.t1data.append(new_t1)
    #     self.t2data.append(new_t2)
    #     while len(self.xdata) > 500:
    #         self.xdata.pop(0)
    #         self.t1data.pop(0)
    #         self.t2data.pop(0)
    #     self.plot.setAxisScale(Qwt.QwtPlot.xBottom, self.xdata[0], self.xdata[0] + 10, 1)
    #     self.curvet1.setData(self.xdata, self.t1data)
    #     self.dotst1.setData(self.xdata, self.t1data)
    #     self.curvet2.setData(self.xdata, self.t2data)
    #     self.dotst2.setData(self.xdata, self.t2data)
    #     self.currentMarker.setXValue(new_x)
    #     self.currentMarker.setYValue(new_t1)
    #     self.currentMarker.attach(self.plot)
    #     self.plot.replot()
    #     self.reactor.callLater(0.5, self.remove_current_marker)

    def remove_current_marker(self):
        self.currentMarker.detach()
        self.plot.replot()


class KoalaThrottlePositionTag(KoalaPlotBaseTag):
    def __init__(self, reactor):
        super(KoalaThrottlePositionTag, self).__init__(reactor=reactor, x_axis_name="Time", y_axis_name="Throttle Position")

    def got_new_data(self, packet):
        new_x = float(packet["time"]) / 1000
        new_t1 = float(packet["t1"])
        new_t2 = float(packet["t2"])
        if new_t2 > 900:
            print "x: %s, throttle2: %s" % (new_x, new_t2)
        self.xdata.append(new_x)
        self.t1data.append(new_t1)
        self.t2data.append(new_t2)
        while len(self.xdata) > 500:
            self.xdata.pop(0)
            self.t1data.pop(0)
            self.t2data.pop(0)
        self.plot.setAxisScale(Qwt.QwtPlot.xBottom, self.xdata[0], self.xdata[0] + 10, 1)
        self.curvet1.setData(self.xdata, self.t1data)
        self.dotst1.setData(self.xdata, self.t1data)
        self.curvet2.setData(self.xdata, self.t2data)
        self.dotst2.setData(self.xdata, self.t2data)
        self.currentMarker.setXValue(new_x)
        self.currentMarker.setYValue(new_t1)
        self.currentMarker.attach(self.plot)
        self.plot.replot()
        self.reactor.callLater(0.5, self.remove_current_marker)


class KoalaBrakePositionTag(KoalaPlotBaseTag):
    def __init__(self, reactor):
        super(KoalaBrakePositionTag, self).__init__(reactor=reactor, x_axis_name="Time", y_axis_name="Brake Position")

        self.side_panel = QVBoxLayout()
        self.steering_wheel = QLabel()
        self.error_flags = QTableWidget(9, 2)
        #Disable editting
        self.error_flags.setEditTriggers(QAbstractItemView.EditTrigger(0))
        self.error_flags.setFixedWidth(220)
        self.error_flags.setFixedHeight(400)
        self.error_flags.verticalHeader()
        self.side_panel.addWidget(self.steering_wheel)
        self.side_panel.addWidget(self.error_flags)

        self.main_layout.addLayout(self.side_panel)
        self.set_error_flags(0xff)
        self.set_steering_position(0)

    def set_steering_position(self, position):
        self.steering_wheel.setText("Steering position: %s" % position)

    def set_error_flags(self, flags):
        self.error_flags.clear()
        self.error_flags.setItem(0, 0, QTableWidgetItem("Flags"))
        self.error_flags.setItem(0, 1, QTableWidgetItem("Message"))

        self.error_flags.setItem(1, 0, QTableWidgetItem("0x0000"))
        self.error_flags.setItem(2, 0, QTableWidgetItem("0x0001"))
        self.error_flags.setItem(3, 0, QTableWidgetItem("0x0002"))
        self.error_flags.setItem(4, 0, QTableWidgetItem("0x0004"))
        self.error_flags.setItem(5, 0, QTableWidgetItem("0x0008"))
        self.error_flags.setItem(6, 0, QTableWidgetItem("0x0010"))
        self.error_flags.setItem(7, 0, QTableWidgetItem("0x0020"))
        self.error_flags.setItem(8, 0, QTableWidgetItem("0x0040"))

        if flags is 0:
            self.error_flags.setItem(1, 1, QTableWidgetItem("No error"))

        if flags & 0x0001:
            self.error_flags.setItem(2, 1, QTableWidgetItem("Throttle 1 out of range"))

        if flags & 0x0002:
            self.error_flags.setItem(3, 1, QTableWidgetItem("Throttle 2 out of range"))

        if flags & 0x0004:
            self.error_flags.setItem(4, 1, QTableWidgetItem("Brake 1 out of range"))

        if flags & 0x0008:
            self.error_flags.setItem(5, 1, QTableWidgetItem("Brake 2 out of range"))

        if flags & 0x0010:
            self.error_flags.setItem(6, 1, QTableWidgetItem("Steering out of range"))

        if flags & 0x0020:
            self.error_flags.setItem(7, 1, QTableWidgetItem("Throttle curve match"))

        if flags & 0x0040:
            self.error_flags.setItem(8, 1, QTableWidgetItem("Soft throttle/brake plausibility"))


    def got_new_data(self, packet):
        pass
