__author__ = 'yilu'

import sys
from autobahn.twisted.websocket import WebSocketServerFactory
from twisted.web import server
from twisted.internet import reactor
from KSerialUtil import XBeeConnector
from KSerialUtil import demoParser

from twisted.python import log

from server.KoalaServerWebSocket import *
from server.KoalaServerTCP import *

from KSerialUtil.CANPacket import *

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    webSocketServer = BroadcastServerFactory(url="ws://localhost:9000", debug=False, reactor=reactor)
    webSocketServer.protocol = KoalaWebSocketServerProtocol
    TCPServer = server.Site(KoalaTCPServerResource())
    TCPPort = reactor.listenTCP(8888, TCPServer)
    webSocketPort = reactor.listenTCP(9000, webSocketServer)
    # parser = demoParser.DemoParser()

    # def onParsedMessageArrive(throttle1, throttle2, time):
    #     webSocketServer.send_data(throttle1, throttle2, time)
    # parser.onDataReady(onParsedMessageArrive)

    # XBee = XBeeConnector.XBeeConnector()
    #
    # def onXBeeMessage(message):
    #     parser.parse(message)
    #
    # XBee.on_data_arrive(onXBeeMessage)
    #
    # XBee.init()

    def timed_event():
        packet = CANTrottleBrakeSteering.CANThrottleSignalPacket(0x00FF009900000000)
        webSocketServer.send_data("data", packet.serialized())

        brake = CANTrottleBrakeSteering.CANBrakeSteeringAndStatusPacket(0x00D400D6002D00A3)
        webSocketServer.send_data("data", brake.serialized())

        bms = CANBMS.CANVoltageDataPacket(0x0800F60034E31A0E)
        webSocketServer.send_data("data", bms.serialized())

        reactor.callLater(0.5, timed_event)

    reactor.callLater(0.5, timed_event)

    reactor.run()
