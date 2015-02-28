__author__ = 'yilu'

from enum import Enum

from src.KSerialUtil.CANPacket.CANBase import *


class CANSystemStatePacketErrorFlag(Enum):
    CANSSPEF_system_ON_not_started =    0x0000,
    CANSSPEF_neutral =                  0x0001,
    CANSSPEF_drive =                    0x0002,
    CANSSPEF_fault_condition_present =  0x0004


class CANSystemStatePacket(CANBasePacket):
    def __init__(self, data):
        CANBasePacket.__init__(self, data)
        self.CAN_ID = CANID.CANID_system_state
        self.state_flags =                      (data & 0xFFFF000000000000) >> 48
        self.maximum_battery_current =          (data & 0x0000FFFF00000000) >> 32
        self.maximum_motor_current_forward =    (data & 0x00000000FFFF0000) >> 16
        self.maximum_motor_current_backward =   (data & 0x000000000000FFFF) >> 0
