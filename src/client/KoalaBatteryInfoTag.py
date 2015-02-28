__author__ = 'yilu'

from PyQt4.QtGui import *
from PyQt4.QtCore import *


class BatteryInfoTag(QWidget):

    def __init__(self, reactor):
        super(BatteryInfoTag, self).__init__()
        self.reactor = reactor
        self.grid = QGridLayout(self)
        self.grid.setSpacing(0)

        for i in range(8):
            for j in range(8):
                new_cell = BatteryCellWidget(reactor, i * 8 + j)
                # new_cell.setFixedHeight(40)
                # new_cell.setFixedWidth(30)
                self.grid.addWidget(new_cell, i, j)

        self.setLayout(self.grid)


class BatteryCellWidget(QLabel):
    def __init__(self, reactor, index):
        super(BatteryCellWidget, self).__init__()
        self.reactor = reactor
        self.index = index
        self.setText("#%s\n!!!" % self.index)
        self.setStyleSheet("background-color: rgb(255,0,0);border:1px solid rgb(0, 255, 0); ")

    def set_precentage(self, percentage):
        self.setText("#%s\n%s\%" % self.index, percentage)