__author__ = 'yilu'

import random
import json
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory

from twisted.python import log


class KoalaWebSocketServerProtocol(WebSocketServerProtocol):
    def __init__(self):
        self.counter = 0

    def onConnect(self, request):
        print "Client connecting: {0}".format(request.peer)

    def onOpen(self):
        print "WebSocket connection open."
        print self.counter
        self.counter += 1
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        # if isBinary:
        #     print "Binary message received: {0} bytes".format(len(payload))
        # else:
        #     print "Text message received: {0}".format(payload.decode('utf8'))

        ## echo back message verbatim
        self.sendMessage(payload, isBinary)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)

    def onClose(self, wasClean, code, reason):
        print "WebSocket connection closed: {0}".format(reason)


class BroadcastServerFactory(WebSocketServerFactory):
    """
    Simple broadcast server broadcasting any message it receives to all
    currently connected clients.
    """

    def __init__(self, url, debug=False, debugCodePaths=False, reactor=None):
        WebSocketServerFactory.__init__(self, url, debug=debug, debugCodePaths=debugCodePaths)
        self.clients = []
        # self.tickcount = 0
        # self.send_fake_data()
        self.reactor = reactor

    # def send_fake_data(self):
    #     self.tickcount += 1
    #     packet = {
    #         "data": random.random(),
    #         "time": self.tickcount,
    #         "type": "throttle"
    #     }
    #     self.broadcast(json.dumps(packet))
    #     # self.reactor.callLater(1, self.send_fake_data)

    def send_data(self, type, payload):
        # print "sending data"
        packet = {
            "type": type,
            "payload": payload
        }
        self.broadcast(packet)

    def register(self, client):
        if not client in self.clients:
            print("registered client {}".format(client.peer))
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            print("unregistered client {}".format(client.peer))
            self.clients.remove(client)

    def broadcast(self, msg):
        # print("broadcasting message '{}' ..".format(msg))
        for c in self.clients:
            # c.sendMessage(msg.encode('utf8'))
            c.sendMessage(json.dumps(msg))
            # print("message sent to {}".format(c.peer))