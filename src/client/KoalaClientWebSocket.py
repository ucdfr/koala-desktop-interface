__author__ = 'yilu'

from twisted.application import service
from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol
import json

my_service = None


class KoalaWebSocketClientProtocol(WebSocketClientProtocol):
    def __init__(self):
        pass
        # self.main_UI = None

    def onConnect(self, response):
        print "Connecting..."

    def onOpen(self):
        print "Opening..."
        if my_service:
            my_service.connection_established()

    def onMessage(self, payload, isBinary):
        packet = json.loads(payload)
        if my_service:
            my_service.got_data(packet)

    def onClose(self, wasClean, code, reason):
        if my_service:
            my_service.connection_lost()


class KoalaWebSocketClientFactory(WebSocketClientFactory):
    def __init__(self, *args, **kwargs):
        WebSocketClientFactory.__init__(self, *args, **kwargs)
        self.protocol = None

    def buildProtocol(self, addr):
        self.protocol = KoalaWebSocketClientProtocol()
        self.protocol.factory = self
        return self.protocol

    # def stop_connection(self):
    #     if self.protocol:
    #         self.protocol.sendClose()


class KoalaWebSocketService(service.Service):
    def __init__(self, reactor, site, port, debug):
        self.reactor = reactor
        self.site = site
        self.port = port
        self.debug = debug
        self.factory = None
        self.connector = None
        self.main_UI = None
        global my_service
        my_service = self

    def start_service(self):
        print "ws://%s:%d" % (self.site, self.port)
        self.factory = KoalaWebSocketClientFactory("ws://%s:%d" % (self.site, self.port), debug=self.debug, reactor=self.reactor)
        self.connector = self.reactor.connectTCP(self.site, self.port, self.factory)

    def stop_service(self, callback):
        print "\nShutting down client"
        if self.connector:
            print "Disconnecting the connector"
            self.factory.protocol.sendClose()

            def on_protocol_close(wasClean, code, reason):
                print "on protocol close"
                self.connector.disconnect()
                if callback:
                    callback()
            self.factory.protocol.onClose = on_protocol_close

    def got_data(self, packet):
        if packet["type"] == "data":
            self.main_UI.got_message_from_server(packet["payload"])

    def connection_established(self):
        self.main_UI.update_server_status(connected=True, host=self.site, port=self.port)

    def connection_lost(self):
        self.main_UI.update_server_status(connected=False, host="0.0.0.0", port="00")

    @property
    def main_UI(self):
        return self.main_UI

    @main_UI.setter
    def main_UI(self, value):
        self.main_UI = value
        self.factory.protocol.main_UI = value
