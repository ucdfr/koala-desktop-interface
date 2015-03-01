__author__ = 'yilu'

from src.KSerialUtil.CANPacket.CANBase import *


class CANTPDO1CurrentControlPacket(CANBasePacket):
    def __init__(self, data):
        CANBasePacket.__init__(self, data)
        self.CAN_ID = CANID.CANID_TPDO1_current_control
        self.target_ld =    (data & 0xFFFF000000000000) >> 48
        self.target_lp =    (data & 0x0000FFFF00000000) >> 32
        self.ld =           (data & 0x00000000FFFF0000) >> 16
        self.lp =           (data & 0x000000000000FFFF) >> 0


class CANTPDO2ControlsPacket(CANBasePacket):
    def __init__(self, data):
        CANBasePacket.__init__(self, data)
        self.CAN_ID = CANID.CANID_TPDO2_controls
        self.voltage_modulation =   (data & 0xFFFF000000000000) >> 48
        self.ud =                   (data & 0x0000FFFF00000000) >> 32
        self.uq =                   (data & 0x00000000FFFF0000) >> 16
        self.economy_value =        (data & 0x000000000000FFFF) >> 0


class CANTPDO3OperationParamsPacket(CANBasePacket):
    def __init__(self, data):
        CANBasePacket.__init__(self, data)
        self.CAN_ID = CANID.CANID_TPDO3_operation_params
        self.target_velocity_lef_motor =            (data & 0xFFFFFFFF00000000) >> 32
        self.maximum_battery_discharge_current =    (data & 0x00000000FFFF0000) >> 16
        self.line_contractor =                      (data & 0x000000000000FFFF) >> 0


class CANTPDO4SensorsPacket(CANBasePacket):
    def __init__(self, data):
        CANBasePacket.__init__(self, data)
        self.CAN_ID = CANID.CANID_TPDO4_sensors
        self.battery_voltage =      (data & 0xFFFF000000000000) >> 48
        self.heatsink_temperature = (data & 0x0000FF0000000000) >> 40
        self.battery_current =      (data & 0x000000FFFF000000) >> 24
        self.capacitor_voltage =    (data & 0x0000000000FFFF00) >> 8
        self.digital_inputs =       (data & 0x00000000000000FF) >> 0


class CANTPDO5MotorAndThrottlePacket(CANBasePacket):
    def __init__(self, data):
        CANBasePacket.__init__(self, data)
        self.CAN_ID = CANID.CANID_TPDO5_motor_throttle
        self.velocity =                 (data & 0xFFFFFFFF00000000) >> 32
        self.throttle_input_voltage =   (data & 0x00000000FFFF0000) >> 16
        self.temperature_PTC =          (data & 0x000000000000FFFF) >> 0
