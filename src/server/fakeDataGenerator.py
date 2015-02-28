__author__ = 'yilu'

from src.KSerialUtil.CANPacket import *
from random import *


class fakeDataGenerator:
    def __init__(self):
        self.cell_index = 0
        self.throttle = 100
        self.brake = 150

    def generate_throttle(self):
        self.throttle += randint(0, 50)
        if self.throttle > 900:
            self.throttle = 100 + randint(0, 500)
        throttle2 = self.throttle + randint(20, 50)
        data = self.throttle & 0xFFFF
        data <<= 16
        data |= throttle2 & 0xFFFF
        data <<= 32
        return CANTrottleBrakeSteering.CANThrottleSignalPacket(data)

    def generate_brake(self):
        self.brake += randint(0, 50)
        if self.brake > 900:
            self.brake = 100 + randint(0, 500)
        brake2 = self.brake + randint(20, 50)
        data = self.brake & 0xFFFF
        data <<= 16
        data |= brake2 & 0xFFFF
        data <<= 16
        data |= randint(0, 180)
        data <<= 16
        data |= randint(0, 0xFF) * randint(0, 1)
        return CANTrottleBrakeSteering.CANBrakeSteeringAndStatusPacket(data)

    def generate_voltage(self):
        self.cell_index += 1
        if self.cell_index == 64:
            self.cell_index = 0
        cell_voltage = randint(0, 10000)
        pack_voltage = randint(0, 1200000)
        insulation = randint(0, 500)
        data = self.cell_index & 0xFF
        data <<= 16
        data |= cell_voltage & 0xFFFF
        data <<= 32
        data |= pack_voltage & 0xFFFFFFFF
        data <<= 8
        data |= insulation & 0xFF
        return CANBMS.CANVoltageDataPacket(data)