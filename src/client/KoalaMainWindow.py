from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

import PyQt4.Qwt5 as Qwt

import KoalaMainServerStatusTag
import KoalaPlotTag
import KoalaBatteryInfoTag
import dialog.ChooseServerDialog
from src.KSerialUtil.CANPacket import *


class KoalaMain(QMainWindow):
    def __init__(self, reactor, parent=None):
        super(KoalaMain, self).__init__(parent)
        self.reactor = reactor
        self.resize(800, 600)
        self.__create_main_frame()
        self.__create_menu()
        self.web_socket_service = None

    def __create_menu(self):
        menu_bar = self.menuBar()

        '''
        Koala Main menu
        '''
        koala_menu = menu_bar.addMenu('&Koala')
        close_action = QAction('Close', self)
        close_action.setShortcut('Ctrl+Q')
        close_action.setStatusTip('Close Notepad')
        close_action.triggered.connect(self.__close_app)
        koala_menu.addAction(close_action)

        '''
        Server menu
        '''
        server_menu = menu_bar.addMenu('&Server')
        connect_to_server_action = QAction("Connect to server...", self)
        connect_to_server_action.setStatusTip("Connect to a server")
        connect_to_server_action.triggered.connect(self.__connect_to_server)
        server_menu.addAction(connect_to_server_action)

    def __create_main_frame(self):
        self.main_tab = QTabWidget()
        self.server_status_tab = KoalaMainServerStatusTag.ServerStatusTag()
        self.server_status_tab.set_host(host="0.0.0.0:00")
        # host_label
        self.main_tab.addTab(self.server_status_tab, "Server Status (Alt+1)")
        self.throttle_pos_tag = KoalaPlotTag.KoalaThrottlePositionTag(reactor=self.reactor)
        self.main_tab.addTab(self.throttle_pos_tag, "Throttle Status (Alt+2)")
        self.tab_3 = KoalaPlotTag.KoalaBrakePositionTag(reactor=self.reactor)
        self.main_tab.addTab(self.tab_3, "Brake Status (Alt+3)")

        self.tab_4 = KoalaBatteryInfoTag.BatteryInfoTag(reactor=self.reactor)
        self.main_tab.addTab(self.tab_4, "Battery Status (Alt+4")

        self.main_tab.setCurrentIndex(0)

        self.setCentralWidget(self.main_tab)

    def __close_app(self):
        self.close()
        self.reactor.stop()

    def __connect_to_server(self):
        if self.web_socket_service is not None:
            self.web_socket_service.start_service()

    def keyPressEvent(self, QKeyEvent):
        modifier = QApplication.keyboardModifiers()
        if modifier == Qt.AltModifier:
            if QKeyEvent.key() == ord('1'):
                self.main_tab.setCurrentIndex(0)
            elif QKeyEvent.key() == ord('2'):
                self.main_tab.setCurrentIndex(1)
            elif QKeyEvent.key() == ord('3'):
                self.main_tab.setCurrentIndex(2)
            elif QKeyEvent.key() == ord('4'):
                self.main_tab.setCurrentIndex(3)
            QKeyEvent.accept()

    def update_server_status(self, connected, host, port):
        if connected:
            self.server_status_tab.set_server_state(KoalaMainServerStatusTag.KoalaServerStatusDisplayConnectionStatus.connected)
            self.server_status_tab.set_host("%s:%s" % (host, port))
        else:
            self.server_status_tab.set_server_state(KoalaMainServerStatusTag.KoalaServerStatusDisplayConnectionStatus.notConnected)
            self.server_status_tab.set_host("0.0.0.0:00")

    def got_message_from_server(self, packet):
        result = CANParser.CANParser.parse(packet)
        if isinstance(result, CANTrottleBrakeSteering.CANThrottleSignalPacket):
            self.throttle_pos_tag.got_new_data(result)
        elif isinstance(result, CANTrottleBrakeSteering.CANBrakeSteeringAndStatusPacket):
            self.tab_3.got_new_data(result)
        elif isinstance(result, CANBMS.CANVoltageDataPacket):
            self.tab_4.got_new_data(result)


    @property
    def webSocketService(self):
        return self.web_socket_service

    @webSocketService.setter
    def webSocketService(self, value):
        self.web_socket_service = value
