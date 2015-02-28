__author__ = 'yilu'

from enum import Enum

from src.KSerialUtil.CANPacket.CANBase import *


class CANPackStatusPacketErrorFlag(Enum):
    CANPSPEF_no_error =                         0x0000,
    CANPSPEF_charge_mode =                      0x0001,
    CANPSPEF_pack_temperature_limit_exceeded =  0x0002,
    CANPSPEF_pack_temperature_limit_close =     0x0004,
    CANPSPEF_pack_temperature_low_limit =       0x0008,
    CANPSPEF_low_SOC =                          0x0010,
    CANPSPEF_critical_SOC =                     0x0020,
    CANPSPEF_imbalance =                        0x0040,
    CANPSPEF_6804_comm_failure =                0x0080,
    CANPSPEF_negative_contactor_closed =        0x0100,
    CANPSPEF_positive_contactor_closed =        0x0200,
    CANPSPEF_isolation_fault =                  0x0400,
    CANPSPEF_cell_too_high =                    0x0800,
    CANPSPEF_cell_too_low =                     0x1000,
    CANPSPEF_charge_hault =                     0x2000,
    CANPSPEF_full =                             0x4000,
    CANPSPEF_precharge_contactor_closed =       0x8000


class CANPackStatusPacket(CANBasePacket):
    def __init__(self, data):
        CANBasePacket.__init__(self, data)
        self.CAN_ID = CANID.CANID_pack_status
        self.SOC_percent =                  (data & 0xFF00000000000000) >> 56
        self.AH_used_since_full_charge =    (data & 0x00FF000000000000) >> 48
        self.BMS_status_bits =              (data & 0x0000FFFF00000000) >> 32
        self.number_of_charge_cycles =      (data & 0x00000000FFFF0000) >> 16
        self.pack_balance_delta_mV =        (data & 0x000000000000FFFF) >> 0


class CANVoltageDataPacket(CANBasePacket):
    def __init__(self, data):
        CANBasePacket.__init__(self, data)
        self.CAN_ID = CANID.CANID_voltage_data
        self.cell_index =                       (data & 0xFF00000000000000) >> 56
        self.cell_voltage_mV =                  (data & 0x00FFFF0000000000) >> 40
        self.pack_voltage_mV =                  (data & 0x000000FFFFFFFF00) >> 8
        self.insulation_condition_from_bender = (data & 0x00000000000000FF) >> 0


class CANTemperatureDataCurrentPacket(CANBasePacket):
    def __init__(self, data):
        CANBasePacket.__init__(self, data)
        self.CAN_ID = CANID.CANID_temp_data_current
        self.sensor_index =         (data & 0xFF00000000000000) >> 56
        self.temp_value_C =         (data & 0x00FF000000000000) >> 48
        self.highest_temp_value =   (data & 0x0000FF0000000000) >> 40
        self.lowest_temp_value =    (data & 0x000000FF00000000) >> 32
        self.discharge_current_mA = (data & 0x00000000FFFFFFFF) >> 0
