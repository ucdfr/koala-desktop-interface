__author__ = 'yilu'

import unittest
# noinspection PyUnresolvedReferences
import env
from src.KSerialUtil.coder import RFC1662Encoder, RFC1662Decoder


class EncoderTestCase(unittest.TestCase):
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
        print decoded_result
        self.assertEqual(decoded_result, self.original_data)

    def test_redundant_group_data(self):
        decoder = RFC1662Decoder()
        decoder.read_bytes(self.set1_encoded_data)
        decoded_result = decoder.get_result()
        self.assertEqual(decoded_result, self.original_data)


if __name__ == '__main__':
    unittest.main()

