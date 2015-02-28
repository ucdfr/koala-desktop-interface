__author__ = 'yilu'

from enum import Enum


class CANID(Enum):
    CANID_INVALID = 0xFFF,
    CANID_throttle_sig = 0x205,
    CANID_brake_steering_status = 0x305, # TODO: Fake
    CANID_pack_status = 0x188,
    CANID_voltage_data = 0x388,
    CANID_temp_data_current = 0x488,
    CANID_system_state = 0x588, #TODO: Fake
    CANID_TPDO1_current_control = 0x181,
    CANID_TPDO2_controls = 0x481,
    CANID_TPDO3_operation_params = 0x501,
    CANID_TPDO4_sensors = 0x381,
    CANID_TPDO5_motor_throttle = 0x281


class CANBasePacket:
    def __init__(self):
        self.CAN_ID = CANID.CANID_INVALID
