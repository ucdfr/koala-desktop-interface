# from src import KoalaMainWindow

__author__ = 'yilu'
# import sys
import signal
from PyQt4 import QtGui
from client.KoalaMainWindow import *
from client.KoalaClientWebSocket import KoalaWebSocketService


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

    koala_main_interface = KoalaMain(reactor)
    web_socket_service = KoalaWebSocketService(reactor=reactor, site="localhost", port=9000, debug=True)
    koala_main_interface.webSocketService = web_socket_service
    web_socket_service.main_UI = koala_main_interface
    koala_main_interface.show()

    def sigint_handler(signal, frame):
        print "SIGINT received"

        def service_closed():
            reactor.callFromThread(reactor.stop)

        koala_main_interface.close()
        web_socket_service.stop_service(service_closed)

    signal.signal(signal.SIGINT, sigint_handler)

    reactor.run()
