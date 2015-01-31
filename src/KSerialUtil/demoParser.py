__author__ = 'yilu'

from enum import Enum


class DemoParserState(Enum):
    WaitingFor7E = 1,
    ReadingLength = 2,
    Reading = 3


class DemoParser:
    def __init__(self):
        self.state = DemoParserState.WaitingFor7E
        self.data_callback = None

    @staticmethod
    def get_hex_representation(data_str):
        return ":".join("{:02x}".format(ord(c)) for c in data_str)

    def onDataReady(self, callback):
        self.data_callback = callback

    def parse(self, data):
        packet = [''] * 31
        counter = 0
        for i in range(len(data)):
            char = data[i]
            if self.state == DemoParserState.WaitingFor7E:
                if i + 2 < len(data):
                    if char == chr(0x7E) and data[i+1] == chr(0x00) and data[i+2] == chr(0x1D):
                        packet = [''] * 31
                        counter = 0
                        self.state = DemoParserState.Reading
                        # print "7E detected"
            elif self.state == DemoParserState.Reading:
                packet[counter] = char
                counter += 1
                if counter == 31:
                    self.state = DemoParserState.WaitingFor7E
                    # print self.get_hex_representation(packet)
                    self.analysis_packet(packet)
        print "Data ended"
        self.state = DemoParserState.WaitingFor7E

    def analysis_packet(self, packet):
        # if packet[16] != chr(0x97):
        frame = packet[16:-1]
        # print self.get_hex_representation(frame)
        # print frame.size()
        time = frame[0:3]
        ID = frame[3:5]
        length = ord(frame[5])
        payload = frame[6:14]

        decoded_time = ord(time[0])
        decoded_time <<= 8
        decoded_time |= ord(time[1])
        decoded_time <<= 8
        decoded_time |= ord(time[2])
        decoded_ID = (ord(ID[0]) << 8) | ord(ID[1])
        decoded_payload = ord(payload[0])
        for i in range(7):
            decoded_payload <<= 8
            decoded_payload |= ord(payload[i + 1])
        decoded_time = 0xFFFFFFFFFFFF - decoded_time
        print "time is %s, ID is %s, length is %s, payload is %s" % (decoded_time, decoded_ID, length, decoded_payload)
        print hex(decoded_payload)
        if decoded_ID == 0x205:
        # if True:
            throttle1 = (0xFFFF000000000000 & decoded_payload) >> 48
            throttle2 = (0x0000FFFF00000000 & decoded_payload) >> 32

            print "Throttle packet detected, throttle 1 = %s, throttle 2 = %s at time %s" % (throttle1, throttle2, decoded_time)
            if self.data_callback:
                self.data_callback(throttle1, throttle2, decoded_time)