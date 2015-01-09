__author__ = 'yilu'

from enum import Enum


class RFC1662DecoderStates(Enum):
    decode_not_started = 1
    decode_in_progress = 2
    decode_done = 3


class RFC1662Flags(Enum):
    begin_flag = 0x7E
    escape_flag = 0x7D
    escape_mask = 0x20


class RFC1662Encoder:
    def __init__(self):
        pass

    @staticmethod
    def encode_byte_array(data):
        """
        This method is static and doesn't require an instance of encoder, will encode the message in RFC1662 format.
        Will raise TypeError if illegal data is fed

        :param data: list of bytes to be encoded
        :return: list of encoded bytes
        """

        if not type(data) is list:
            raise TypeError("next_bytes need to be a list")

        result = [RFC1662Flags.begin_flag]
        for item in data:
            if item == RFC1662Flags.begin_flag or item == RFC1662Flags.escape_flag:
                result.append(RFC1662Flags.escape_flag)
                result.append(item ^ RFC1662Flags.escape_mask)
            else:
                result.append(item)
        return result


class RFC1662Decoder:
    def __init__(self):
        self.state = RFC1662DecoderStates.decode_not_started
        self.should_escape_flag = False
        self.result = []

    def read_byte(self, next_byte):
        """
        This method is the main decoding functions in this class, it read the next byte from the data, if the data is
        legal based on the current state of decoder it will decode the message and record it in buffer, if the data is
        not legal, it will simply ignore it without giving any warning. If the next starting byte is detected, the
        decoder will go into decode_done state and ignore all upcoming input, the user have to reset the decoder by
        either read out the buffer or call reset manually. In a similar manner, the decoder will ignore anything before
        a starting byte is read

        :param next_byte: next byte to be fed into the decoder
        :return: None
        """
        # If decoder is in idle state, try to get start byte and move to next state, if not
        if self.state == RFC1662DecoderStates.decode_not_started:
            # if the start flag is encountered, start decoding, if not, ignore
            if next_byte == RFC1662Flags.begin_flag:
                self.state = RFC1662DecoderStates.decode_in_progress

        elif self.state == RFC1662DecoderStates.decode_in_progress:
            if self.should_escape_flag:
                self.result.append(next_byte ^ RFC1662Flags.escape_mask)
                self.should_escape_flag = False
            else:
                if next_byte == RFC1662Flags.escape_flag:
                    self.should_escape_flag = True
                elif next_byte == RFC1662Flags.begin_flag:
                    self.state = RFC1662DecoderStates.decode_done
                else:
                    self.result.append(next_byte)

    def read_bytes(self, next_bytes):
        """
        Similar to read_byte, but read a list of bytes instead of a single byte. Will raise TypeError if anything
        else is given as input

        :param next_bytes: A list of bytes to be fed into decoder
        :return: None
        """
        if not type(next_bytes) is list:
            raise TypeError("next_bytes need to be a list")

        for next_byte in next_bytes:
            self.read_byte(next_byte)

    def finish(self):
        """
        Force decoder to finish

        :return: None
        """
        self.state = RFC1662DecoderStates.decode_done

    def decode_done(self):
        """
        Getter for querying the decoder to see if the decoding has concluded

        :return: True if decoding is done, vice versa
        """
        if self.state == RFC1662DecoderStates.decode_done:
            return True
        else:
            return False

    def get_result(self):
        """
        This function will terminate decoding, reset the decoder, and return the decoded values

        :return: decoding result in a list
        """
        self.finish()
        decoded = self.result
        self.reset()
        return decoded

    def reset(self):
        """
        Reset the decoder to initial state, useful after the previous decoding is finished and want to start decoding
        a new message

        :return: None
        """
        self.state = RFC1662DecoderStates.decode_not_started
        self.should_escape_flag = False
        self.result = []
