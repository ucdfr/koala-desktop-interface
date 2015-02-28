__author__ = 'yilu'

from PyQt4.QtGui import *
from PyQt4.QtCore import *


class BatteryInfoTag(QWidget):

    def __init__(self, reactor):
        super(BatteryInfoTag, self).__init__()
        self.reactor = reactor
        self.main_layout = QVBoxLayout(self)

        self.pack_voltage = QLabel()
        self.pack_voltage.setText("Pack voltage: ### mV")
        self.insulation = QLabel()
        self.insulation.setText("Insulation: ###")
        pack_layout = QHBoxLayout()
        pack_layout.addWidget(self.pack_voltage)
        pack_layout.addWidget(self.insulation)

        self.main_layout.addLayout(pack_layout)

        self.grid = QGridLayout(self)
        self.last_active_cell = 0
        self.grid.setSpacing(0)
        self.cell_list = []

        for i in range(8):
            for j in range(8):
                new_cell = BatteryCellWidget(reactor, i * 8 + j)
                # new_cell.setFixedHeight(40)
                # new_cell.setFixedWidth(30)
                self.grid.addWidget(new_cell, i, j)
                self.cell_list.append(new_cell)

        self.main_layout.addLayout(self.grid)
        self.setLayout(self.main_layout)

    def got_new_data(self, packet):
        index = packet.cell_index
        cell_voltage = packet.cell_voltage_mV
        pack_voltage = packet.pack_voltage_mV
        insulation = packet.insulation_condition_from_bender

        self.cell_list[self.last_active_cell].unhighlight_cell()
        self.cell_list[index].update_voltage(cell_voltage)
        self.last_active_cell = index
        self.pack_voltage.setText("Pack voltage: %s mV" % pack_voltage)
        self.insulation.setText("Insulation: %s" % insulation)


class BatteryCellWidget(QLabel):
    def __init__(self, reactor, index):
        super(BatteryCellWidget, self).__init__()
        self.reactor = reactor
        self.index = index
        self.setText("#%s\n### mV" % self.index)
        self.unhighlight_cell()

    def update_voltage(self, voltage):
        self.setText("#%s\n%s mV" % (self.index, voltage))
        self.setStyleSheet("background-color: rgb(255,0,0);border:1px solid rgb(0, 255, 0); ")

    def unhighlight_cell(self):
        self.setStyleSheet("background-color: rgb(255,255,255);border:0px")