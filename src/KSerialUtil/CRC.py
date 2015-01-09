__author__ = 'yilu'

'''
Ported from Jonathan's Hamming function, not sure if it works..yet
Source: https://github.com/ucdfr/Node-Beaver/blob/usb/Node-Beaver/Node-Beaver.cydsn/hamfunc.c
'''
# TODO: Get an idea on how this thing works

from enum import Enum


class HAM(Enum):
    INTACT = 1
    SINGLE = 2
    DOUBLE = 3


class Hamming84:
    hams = [
        0x00, 0x87, 0x99, 0x1E,
        0xAA, 0x2D, 0x33, 0xB4,
        0x4B, 0xCC, 0xD2, 0x55,
        0xE1, 0x66, 0x78, 0xFF
    ]

    def __init__(self):
        pass

    @staticmethod
    def ham_byte(byte):
        """
        LOL

        :param byte:
        :return:
        """
        upper = Hamming84.hams[byte >> 4]
        lower = Hamming84.hams[byte & 0x0F]
        return upper, lower
    # ham_byte()

    @staticmethod
    def unham_nibble(byte):
        """
        I have no idea what this function is doing...

        :param byte:
        :return:
        """

        pos = 0
        code = [0x00] * 8
        signal = HAM.INTACT

        code[0] = byte & 0x01
        byte >>= 1
        code[1] = byte & 0x01
        byte >>= 1
        code[2] = byte & 0x01
        byte >>= 1
        code[3] = byte & 0x01
        byte >>= 1
        code[4] = byte & 0x01
        byte >>= 1
        code[5] = byte & 0x01
        byte >>= 1
        code[6] = byte & 0x01
        byte >>= 1
        code[7] = byte & 0x01

        if (code[2] ^ code[4] ^ code[6]) != code[0]:
            pos += 1

        if (code[2] ^ code[5] ^ code[6]) != code[1]:
            pos += 2

        if (code[4] ^ code[5] ^ code[6]) != code[3]:
            pos += 4

        if pos:
            code[pos-1] ^= 1  # correct error
            signal = HAM.SINGLE
        # if single error occurred

        if (code[0] ^ code[1] ^ code[2] ^ code[3] ^ code[4] ^ code[5] ^ code[6]) != code[7]:
            if pos != 0:  # if double error detected
                signal = HAM.DOUBLE
            else:
                code[7] ^= 1
                signal = HAM.SINGLE
                # else only last parity had error
        # if last parity doesn't match

        nibble = code[6]
        nibble = (nibble << 1) | code[5]
        nibble = (nibble << 1) | code[4]
        nibble = (nibble << 1) | code[2]
        return nibble, signal
    # ham_chk_nib()

    @staticmethod
    def unham_byte(upper, lower):
        """
        I have no idea what I'm doing...

        :param upper:
        :param lower:
        :return:
        """

        nibble, signal_upper = Hamming84.unham_nibble(upper)
        output = nibble << 4
        nibble, signal_lower = Hamming84.unham_nibble(lower)

        if signal_upper == HAM.DOUBLE or signal_lower == HAM.DOUBLE:
            return output, signal_lower, signal_upper, 0

        output |= nibble
        return output, signal_upper, signal_lower, 1  # returns 1 if no double error
    # ham_chk_byt()
