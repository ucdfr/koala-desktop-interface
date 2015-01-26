# from src import KoalaMainWindow

__author__ = 'yilu'
import sys
import signal

from PyQt4 import QtGui
from client.KoalaMainWindow import *


def signal_handler(_signal, _frame):
    myWindow.close()
    reactor.stop()
    sys.exit(0)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    # Keep PyQt and Twisted in same main loop
    try:
        import qt4reactor
    except ImportError:
        # Maybe qt4reactor is placed inside twisted.internet in site-packages?
        from twisted.internet import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor


    # server = KoalaWebSocketServerFactory.produce(reactor)
    # myWindow = KoalaMainWindow(reactor, server)

    myWindow = KoalaMain(reactor)
    myWindow.show()
    reactor.run()
    signal.signal(signal.SIGINT, signal_handler)
