__author__ = 'yilu'

from PyQt4 import QtCore, QtGui, uic
import os

from enum import Enum
class KoalaMainWindowState(Enum):
    windowCreated = 1
    initializingServer = 2
    serverRunning = 3

class KoalaMainWindow(QtGui.QMainWindow, uic.loadUiType(os.path.dirname(os.path.realpath(__file__)) + "/KoalaMainWindow.ui")[0]):
    def __init__(self, reactor, server, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.reactor = reactor
        self.setupUi(self)
        self.state = KoalaMainWindowState.windowCreated

        self.BtnServerSwitch.clicked.connect()

    def startServer(self):
        self.state = KoalaMainWindowState.initializingServer

    def serverRunning(self):
        self.state = KoalaMainWindowState.serverRunning

    '''
    Callback bindings
    '''
    def onServerSwitchClicked(self, callback):
        if self.state == KoalaMainWindowState.windowCreated:
            callback(True)
        elif self.state == KoalaMainWindowState.serverRunning:
            callback(False)
        else:
            print "Server is initializing"

    # def startServerClicked(self):
