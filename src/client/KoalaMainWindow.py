from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

import PyQt4.Qwt5 as Qwt

import KoalaMainServerStatusDisplay


class KoalaMain(QMainWindow):
    def __init__(self, reactor, parent=None):
        super(KoalaMain, self).__init__(parent)
        self.reactor = reactor
        self.resize(800, 600)
        self.__create_main_frame()
        self.__create_menu()

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
        # connect_to_server_action.triggered.connect(None)
        server_menu.addAction(connect_to_server_action)

    def __create_main_frame(self):
        self.main_tab = QTabWidget()
        self.status_tab = KoalaMainServerStatusDisplay.ServerStatusDisplay()
        self.status_tab.set_host("0.0.0.0")
        # host_label
        self.main_tab.addTab(self.status_tab, "Server Status (Alt+1)")
        self.tab_2 = QWidget()
        self.main_tab.addTab(self.tab_2, "Throttle Status (Alt+2)")
        self.tab_3 = QWidget()
        self.main_tab.addTab(self.tab_3, "Battery Status (Alt+3)")

        self.main_tab.setCurrentIndex(0)

        self.setCentralWidget(self.main_tab)

    def __close_app(self):
        self.close()
        self.reactor.stop()

    def keyPressEvent(self, QKeyEvent):
        modifier = QApplication.keyboardModifiers()
        if modifier == Qt.AltModifier:
            if QKeyEvent.key() == ord('1'):
                self.main_tab.setCurrentIndex(0)
            elif QKeyEvent.key() == ord('2'):
                self.main_tab.setCurrentIndex(1)
            elif QKeyEvent.key() == ord('3'):
                self.main_tab.setCurrentIndex(2)
            QKeyEvent.accept()

