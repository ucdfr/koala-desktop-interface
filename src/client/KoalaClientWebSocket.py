__author__ = 'yilu'

from twisted.application import service
from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol


class KoalaWebSocketClientProtocol(WebSocketClientProtocol):
    def __init__(self):
        self.main_UI = None

    def onConnect(self, response):
        print "Connecting..."

    def onOpen(self):
        print "Opening..."
        self.main_UI.update_server_status(True, "localhost", 9000)

    def onMessage(self, payload, isBinary):
        print "got message"

    @property
    def main_UI(self):
        return self.main_UI

    @main_UI.setter
    def main_UI(self, value):
        print "protocol setting main ui"
        self.main_UI = value


class KoalaWebSocketService(service.Service):
    def __init__(self, reactor, site, port, debug):
        self.reactor = reactor
        self.site = site
        self.port = port
        self.debug = debug
        self.factory = None
        self.listener = None
        self.main_UI = None

    def start_service(self):
        print "ws://%s:%d" % (self.site, self.port)
        self.factory = WebSocketClientFactory("ws://%s:%d" % (self.site, self.port), debug=self.debug)
        self.factory.protocol = KoalaWebSocketClientProtocol
        # factory.startFactory()
        self.listener = self.reactor.connectTCP(self.site, self.port, self.factory)

    def stop_service(self):
        print "Shutting down client"
        self.factory.protocol.sendClose()
        self.factory.stopFactory()
        self.listener.stopListening()

    @property
    def main_UI(self):
        return self.main_UI

    @main_UI.setter
    def main_UI(self, value):
        self.main_UI = value
        self.factory.protocol.main_UI = value
