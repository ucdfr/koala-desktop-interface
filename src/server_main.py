__author__ = 'yilu'

import sys
from autobahn.twisted.websocket import WebSocketServerFactory
from twisted.web import server
from twisted.internet import reactor
from KSerialUtil import XBeeConnector

from twisted.python import log

from server.KoalaServerWebSocket import *
from server.KoalaServerTCP import *


if __name__ == '__main__':
    log.startLogging(sys.stdout)
    webSocketServer = BroadcastServerFactory(url="ws://localhost:9000", debug=False, reactor=reactor)
    webSocketServer.protocol = KoalaWebSocketServerProtocol
    TCPServer = server.Site(KoalaTCPServerResource())
    TCPPort = reactor.listenTCP(8888, TCPServer)
    webSocketPort = reactor.listenTCP(9000, webSocketServer)
    XBee = XBeeConnector.XBeeConnector()
    XBee.init()
    reactor.run()
