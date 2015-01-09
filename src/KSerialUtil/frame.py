__author__ = 'yilu'

from coder import RFC1662Encoder, RFC1662Decoder
from enum import Enum
import datetime
import time


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


class UnixTimestampTo4BytesConvertor:
    def __init__(self):
        pass

    @staticmethod
    def unix_timestamp_to_four_bytes(timestamp):
        four_bytes = [0x00] * 4
        four_bytes[3] = timestamp & 0xFF
        timestamp >>= 8
        four_bytes[2] = timestamp & 0xFF
        timestamp >>= 8
        four_bytes[1] = timestamp & 0xFF
        timestamp >>= 8
        four_bytes[0] = timestamp & 0xFF
        return four_bytes

    @staticmethod
    def four_bytes_to_unix_timestamp(four_bytes):
        if not isinstance(four_bytes, list):
            raise TypeError("four_bytes need to be a list")
        if len(four_bytes) != 4:
            raise Exception("four_bytes is not actually list of four")

        time_data = (four_bytes[0] << 8) + four_bytes[1]
        time_data = (time_data << 8) + four_bytes[2]
        time_data = (time_data << 8) + four_bytes[3]
        return time_data


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
        if len(raw_data) < 2:
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
            time_data = UnixTimestampTo4BytesConvertor.four_bytes_to_unix_timestamp(raw_data[2:6])
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
    def __init__(self):
        pass

    @staticmethod
    def serialize_frame(frame):
        if isinstance(frame, CommandFrame):
            data_type = KoalaFrameDataType.command_frame_type
            data_to_be_encoded = [0x00] * 2
            data_to_be_encoded[1] = data_type & 0xFF
            data_type >>= 8
            data_to_be_encoded[0] = data_type & 0xFF
            data_to_be_encoded += frame.payload
            data_to_be_encoded += frame.CRC
            return RFC1662Encoder.encode_byte_array(data_to_be_encoded)

        elif isinstance(frame, TelemetryFrame):
            data_type = KoalaFrameDataType.telemetry_frame_type
            data_to_be_encoded = [0x00] * 2
            data_to_be_encoded[1] = data_type & 0xFF
            data_type >>= 8
            data_to_be_encoded[0] = data_type & 0xFF
            int_repre_of_time = int(time.mktime(frame.time.timetuple()))
            timestamp = UnixTimestampTo4BytesConvertor.unix_timestamp_to_four_bytes(int_repre_of_time)
            data_to_be_encoded += timestamp
            data_to_be_encoded += frame.data
            return RFC1662Encoder.encode_byte_array(data_to_be_encoded)

        elif isinstance(frame, AcknowledgementFrame):
            data_type = KoalaFrameDataType.acknowledgement_frame
            data_to_be_encoded = [0x00] * 2
            data_to_be_encoded[1] = data_type & 0xFF
            data_type >>= 8
            data_to_be_encoded[0] = data_type & 0xFF
            return RFC1662Encoder.encode_byte_array(data_to_be_encoded)

        else:
            raise TypeError("Unrecognized frame type")
