from src import KoalaMainWindow

__author__ = 'yilu'
import sys

from PyQt4 import QtGui
from server.KoalaServerWebSocket import KoalaWebSocketServerFactory

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


    server = KoalaWebSocketServerFactory.produce(reactor)
    myWindow = KoalaMainWindow(reactor, server)
    myWindow.show()
    reactor.run()
    # app.exec_()