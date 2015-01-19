__author__ = 'yilu'

import unittest
# noinspection PyUnresolvedReferences
import env
from src.KSerialUtil.coder import RFC1662Encoder, RFC1662Decoder
from src.KSerialUtil.frame import *
from src.KSerialUtil.XBeeConnector import *


class EncoderDecoderTestCase(unittest.TestCase):
    def setUp(self):
        self.original_data = [0xAB, 0x7E]
        self.encoded_data = [0x7E, 0xAB, 0x7D, 0x5E]

        self.set1_original_data = [0xAB, 0x7E]
        self.set1_encoded_data = [0xAA, 0xBB, 0x7E, 0xAB, 0x7D, 0x5E, 0x7E, 0x25]

    def test_simple_encode(self):
        actual_result = RFC1662Encoder.encode_byte_array(self.original_data)
        self.assertEqual(len(actual_result), len(self.encoded_data))
        for i in range(len(self.encoded_data)):
            self.assertEqual(self.encoded_data[i], actual_result[i])

    def test_simple_decode(self):
        decoder = RFC1662Decoder()
        i = 0
        while (not decoder.decode_done()) and i < len(self.encoded_data):
            decoder.read_byte(self.encoded_data[i])
            i += 1
        decoded_result = decoder.get_result()
        self.assertEqual(decoded_result, self.original_data)

    def test_group_data(self):
        decoder = RFC1662Decoder()
        decoder.read_bytes(self.encoded_data)
        decoded_result = decoder.get_result()
        self.assertEqual(decoded_result, self.original_data)

    def test_redundant_data(self):
        decoder = RFC1662Decoder()
        i = 0
        while (not decoder.decode_done()) and i < len(self.set1_encoded_data):
            decoder.read_byte(self.set1_encoded_data[i])
            i += 1
        decoded_result = decoder.get_result()
        self.assertEqual(decoded_result, self.original_data)

    def test_redundant_group_data(self):
        decoder = RFC1662Decoder()
        decoder.read_bytes(self.set1_encoded_data)
        decoded_result = decoder.get_result()
        self.assertEqual(decoded_result, self.original_data)


class FrameTestCase(unittest.TestCase):
    def setUp(self):
        self.command_frame = CommandFrame()
        self.command_frame.payload = [0xAB, 0x7E, 0x53, 0xE5, 0xA0]
        self.command_frame.CRC = [0x00, 0x00]
        self.encoded_command_frame = [0x7E, 0xC0, 0xDF, 0xAB, 0x7D, 0x5E, 0x53, 0xE5, 0xA0, 0x00, 0x00]

        self.telemetry_frame = TelemetryFrame()
        self.telemetry_time_in_epoch = 1420768901
        self.telemetry_frame.set_time(self.telemetry_time_in_epoch)
        self.telemetry_frame.data = [0xAB, 0x7E, 0x53, 0xE5, 0xA0]
        self.encoded_telemetry_frame = [0x7E, 0x71, 0x7F, 0x54, 0xAF, 0x36, 0x85, 0xAB, 0x7D, 0x5E, 0x53, 0xE5, 0xA0]

        self.ack_frame = AcknowledgementFrame()
        self.encoded_ack_frame = [0x7E, 0xAC, 0x1F]

    def test_simple_command_frame_decode(self):
        test_collector = KoalaFrameCollector()
        for item in self.encoded_command_frame:
            test_collector.read_byte(item)
        result_decoded_frame = test_collector.generate_frame()
        self.assertTrue(isinstance(result_decoded_frame, CommandFrame))
        self.assertEqual(self.command_frame.payload, result_decoded_frame.payload)
        self.assertEqual(self.command_frame.CRC, result_decoded_frame.CRC)

    def test_simple_telemetry_frame_decode(self):
        test_collector = KoalaFrameCollector()
        for item in self.encoded_telemetry_frame:
            test_collector.read_byte(item)
        result_decoded_frame = test_collector.generate_frame()
        self.assertTrue(isinstance(result_decoded_frame, TelemetryFrame))
        self.assertEqual(self.telemetry_frame.time, result_decoded_frame.time)
        self.assertEqual(self.telemetry_frame.data, result_decoded_frame.data)

    def test_simple_ack_frame_decode(self):
        test_collector = KoalaFrameCollector()
        for item in self.encoded_ack_frame:
            test_collector.read_byte(item)
        result_decoded_frame = test_collector.generate_frame()
        self.assertTrue(isinstance(result_decoded_frame, AcknowledgementFrame))

    def test_simple_command_frame_encode(self):
        serialized_result = KoalaFrameProducer.serialize_frame(self.command_frame)
        self.assertEqual(serialized_result, self.encoded_command_frame)

    def test_simple_telemetry_frame_encode(self):
        serialized_result = KoalaFrameProducer.serialize_frame(self.telemetry_frame)
        self.assertEqual(serialized_result, self.encoded_telemetry_frame)

    def test_simple_ack_frame_encode(self):
        serialized_result = KoalaFrameProducer.serialize_frame(self.ack_frame)
        self.assertEqual(serialized_result, self.encoded_ack_frame)


class XBeeConnectorTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_connector(self):
        conn = XBeeConnector()
        conn.init()
        # conn.list_port()

if __name__ == '__main__':
    unittest.main()
