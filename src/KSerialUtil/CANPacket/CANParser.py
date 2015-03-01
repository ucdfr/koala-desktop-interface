__author__ = 'yilu'

from CANBase import *
from CANBMS import *
from CANDashboard import *
from CANTrottleBrakeSteering import *
from CANSevconGen4 import *


class CANParser:
    def __init__(self):
        pass

    @staticmethod
    def parse(data):
        CAN_ID = (int(data["type"]),)
        raw_data = int(data["data"])
        if CAN_ID == CANID.CANID_throttle_sig:
            return CANThrottleSignalPacket(raw_data)

        elif CAN_ID == CANID.CANID_brake_steering_status:
            return CANBrakeSteeringAndStatusPacket(raw_data)

        elif CAN_ID == CANID.CANID_pack_status:
            return CANPackStatusPacket(raw_data)

        elif CAN_ID == CANID.CANID_voltage_data:
            return CANVoltageDataPacket(raw_data)

        elif CAN_ID == CANID.CANID_temp_data_current:
            return CANTemperatureDataCurrentPacket(raw_data)

        elif CAN_ID == CANID.CANID_system_state:
            return CANSystemStatePacket(raw_data)

        elif CAN_ID == CANID.CANID_TPDO1_current_control:
            return CANTPDO1CurrentControlPacket(raw_data)

        elif CAN_ID == CANID.CANID_TPDO2_controls:
            return CANTPDO2ControlsPacket(raw_data)

        elif CAN_ID == CANID.CANID_TPDO3_operation_params:
            return CANTPDO3OperationParamsPacket(raw_data)

        elif CAN_ID == CANID.CANID_TPDO4_sensors:
            return CANTPDO4SensorsPacket(raw_data)

        elif CAN_ID == CANID.CANID_TPDO5_motor_throttle:
            return CANTPDO5MotorAndThrottlePacket(raw_data)

        #fallback if type is not recognized
        print "CANParser: type %s not recognized, returning CANBasePacket" % CAN_ID
        return CANBasePacket(data)