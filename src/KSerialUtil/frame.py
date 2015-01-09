__author__ = 'yilu'

from coder import *
from enum import Enum
import datetime


class KoalaFrameType(Enum):
    base_frame = 1
    command_frame = 2
    telemetry_frame = 3
    acknowledgement_frame = 4


class KoalaFrameDataType(object):
    # TODO: determine the real frame type representation for each type
    invalid_frame_type = 0x1ADF
    command_frame_type = 0xC0DF
    telemetry_frame_type = 0x717F
    acknowledgement_frame = 0xAC1F


class KoalaBaseFrame:
    def __init__(self):
        self.frame_type = KoalaFrameType.base_frame


class CommandFrame(KoalaBaseFrame):
    def __init__(self):
        KoalaBaseFrame.__init__(self)
        self.frame_type = KoalaFrameType.command_frame
        self.payload = []
        self.CRC = []


class TelemetryFrame(KoalaBaseFrame):
    def __init__(self):
        KoalaBaseFrame.__init__(self)
        self.frame_type = KoalaFrameType.telemetry_frame
        self.time = datetime.datetime.fromtimestamp(0)
        self.data = []

    def set_time(self, time_int):
        """
        Set the time for telemetry frame, take an int representation and store it as unix timestamp
        :param time_int: Epoch representation of unix timestamp
        :return: None
        """
        self.time = datetime.datetime.fromtimestamp(time_int)


class AcknowledgementFrame(KoalaBaseFrame):
    def __init__(self):
        KoalaBaseFrame.__init__(self)
        self.frame_type = KoalaFrameType.acknowledgement_frame


'''
Frame collector and producer, used to construct a frame from data or serialize a list of bytes from a frame
'''


class KoalaFrameCollector:
    def __init__(self):
        self.frame_type = KoalaFrameType.base_frame
        self.decoder = RFC1662Decoder()

    def read_byte(self, next_byte):
        """
        Read bytes into collector, actually read stuff into the underlying RFC1662 decoder

        :param next_byte: Byte to be read
        :return: None
        """
        self.decoder.read_byte(next_byte)

    def read_bytes(self, next_bytes):
        """
        Similar to read_bytes in RFC1662Decoder

        :param next_bytes: list of bytes to be read next
        :return: None
        """
        self.decoder.read_bytes(next_bytes)

    def frame_ready_for_fetch(self):
        """
        Flag if the frame is ready for use

        :return: True on frame ready, false otherwise
        """
        return self.decoder.decode_done()

    def generate_frame(self):
        """
        Main function to generate frames. Will cut off byte reading of the underlying decoder.
        If any error occurred such as broken frames or CRC mismatch, the collector will return a shell
        frame of either KoalaBaseFrame or corresponding empty frame and give warning in console.

        :return: A KoalaBaseFrame or subclasses
        """
        raw_data = self.decoder.get_result()
        if len(raw_data) <= 2:
            print "length of bytes is too short"
            return KoalaBaseFrame()

        data_type_bytes = (raw_data[0] << 8) + raw_data[1]
        if data_type_bytes == KoalaFrameDataType.command_frame_type:
            self.frame_type = KoalaFrameType.command_frame
            frame = CommandFrame()
            # The offset is 4 instead of 2 because telemetry frame has extra 2 bytes CRC
            if len(raw_data) <= 4:
                print "Premature data, length = {0}, expecting minimum length = 5".format(len(raw_data))
                return frame
            frame.payload = raw_data[2:-2]
            frame.CRC = raw_data[-2:]
            return frame

        elif data_type_bytes == KoalaFrameDataType.telemetry_frame_type:
            self.frame_type = KoalaFrameType.telemetry_frame
            frame = TelemetryFrame()
            # The offset is 6 instead of 2 because telemetry frame has extra 4 bytes of unix timestamp
            if len(raw_data) <= 6:
                print "Premature data, length = {0}, expecting minimum length = 7".format(len(raw_data))
                return frame
            time_data = (raw_data[2] << 8) + raw_data[3]
            time_data = (time_data << 8) + raw_data[4]
            time_data = (time_data << 8) + raw_data[5]
            frame.set_time(time_data)
            frame.data = raw_data[6:]
            return frame

        elif data_type_bytes == KoalaFrameDataType.acknowledgement_frame:
            self.frame_type = KoalaFrameType.acknowledgement_frame
            frame = AcknowledgementFrame()
            if len(raw_data) < 2:
                print "Premature data, length = {0}, expecting minimum length = 2".format(len(raw_data))
                return frame
            return frame

        else:
            print "Unrecognized data type {0}".format(hex(data_type_bytes))
            print hex(raw_data[0])
            print hex(raw_data[1])
            return KoalaBaseFrame()

    def reset(self):
        """
        Reset the collector in a similar fashion to RFC1662Decoder

        :return: None
        """
        self.frame_type = KoalaFrameType.base_frame
        self.decoder.reset()


class KoalaFrameProducer:
    # TODO: Implementation!
    def __init__(self):
        raise NotImplementedError("Producer not implemented yet")
