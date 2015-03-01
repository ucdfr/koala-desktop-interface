__author__ = 'yilu'

from src.KSerialUtil.CANPacket.CANBase import *


class CANThrottleSignalPacket(CANBasePacket):
    def __init__(self, data):
        CANBasePacket.__init__(self, data)
        self.CAN_ID = CANID.CANID_throttle_sig
        self.throttle_signal_1 =    (data & 0xFFFF000000000000) >> 48
        self.throttle_signal_2 =    (data & 0x0000FFFF00000000) >> 32
        padding =                   (data & 0x00000000FFFFFFFF) >> 0

        if padding != 0:
            #if padding is not zero reset everything
            print "Invalid throttle signal packet"
            self.CAN_ID = CANID.CANID_INVALID
            self.throttle_signal_1 = 0
            self.throttle_signal_2 = 0


class CANBrakeSteeringAndStatusErrorFlag(object):
    CANBSASEF_no_error =                            0x0000,
    CANBSASEF_throttle_1_out_of_range =             0x0001,
    CANBSASEF_throttle_2_out_of_range =             0x0002,
    CANBSASEF_brake_1_out_of_range =                0x0004,
    CANBSASEF_brake_2_out_of_range =                0x0008,
    CANBSASEF_steering_out_of_range =               0x0010,
    CANBSASEF_throttle_curve_match =                0x0020,
    CANBSASEF_soft_throttle_brake_plausibility =    0x0040


class CANBrakeSteeringAndStatusPacket(CANBasePacket):
    def __init__(self, data):
        CANBasePacket.__init__(self, data)
        self.CAN_ID = CANID.CANID_brake_steering_status
        self.brake_pressure_1 =     (data & 0xFFFF000000000000) >> 48
        self.brake_pressure_2 =     (data & 0x0000FFFF00000000) >> 32
        self.steering_position =    (data & 0x00000000FFFF0000) >> 16
        self.error_flags =          (data & 0x000000000000FFFF) >> 0
