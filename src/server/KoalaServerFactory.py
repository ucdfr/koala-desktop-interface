__author__ = 'yilu'

import sys
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory

from twisted.python import log


class KoalaWebSocketProtocol(WebSocketServerProtocol):
    def __init__(self):
        pass

    def onConnect(self, request):
        print "Client connecting: {0}".format(request.peer)

    def onOpen(self):
        print "WebSocket connection open."

    def onMessage(self, payload, isBinary):
        if isBinary:
            print "Binary message received: {0} bytes".format(len(payload))
        else:
            print "Text message received: {0}".format(payload.decode('utf8'))

        ## echo back message verbatim
        self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print "WebSocket connection closed: {0}".format(reason)


class KoalaWebSocketServerFactory:
    def __init__(self):
        pass

    @staticmethod
    def produce(reactor):
        log.startLogging(sys.stdout)
        factory = WebSocketServerFactory("ws://localhost:9000", debug=False)
        factory.protocol = KoalaWebSocketProtocol
        port = reactor.listenTCP(9000, factory)
        return port