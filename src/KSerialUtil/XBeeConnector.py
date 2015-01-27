__author__ = 'yilu'
import sys
import glob
import threading
import time

import serial
# from serial.tools import list_ports

import AsyncCall


class XBeeConnector:
    # TODO: Handle connection lost scenario
    def __init__(self):
        self.data_arrive_callback = None
        self.device_name = None
        self.serial_connection = None
        self.data_polling_thread = None

    def init(self):
        """Lists serial ports

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of available serial ports
        """
        if sys.platform.startswith('win'):
            ports = ['COM' + str(i + 1) for i in range(256)]

        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this is to exclude your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')

        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')

        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass

        for item in result:
            self.__send_test_signal(self, item, self.__initial_response_received)

    @staticmethod
    def get_hex_representation(data_str):
        return ":".join("{:02x}".format(ord(c)) for c in data_str)

    def on_data_arrive(self, callback):
        self.data_arrive_callback = callback

    def __initial_response_received(self, data, device, serial_connection):
        if data:
            print "{0} returned data {1}".format(device, data)
        if "OK" in data:
            serial_connection.write("ATSH\r")
            line = serial_connection.readline()
            if "13A200" in line:
                print "XBee confirmed on device {0}".format(device)
                self.serial_connection = serial_connection
                self.device_name = device
                self.__bind_device(self)
            else:
                print "Device {0} did not has a legal response".format(device)
        else:
            serial_connection.close()

    @AsyncCall.Async
    def __bind_device(self):
        print "Starting XBee cooling count down from 10"
        for t in range(10):
            print "{0} mississippi...".format(10 - t)
            time.sleep(1)   # Wait for 10 seconds so the XBee will exit command mode
        print "Binding XBee for data reception"
        self.data_polling_thread = threading.Thread(target=self.__poll_loop)
        self.data_polling_thread.daemon = True
        self.data_polling_thread.start()
        print "XBee binded on device {0}".format(self.device_name)

    def __poll_loop(self):
        while True:
            data = self.serial_connection.readline()
            if data is not None:
                self.__data_received(data)

    def __data_received(self, data):
        if self.data_arrive_callback is not None:
            self.data_arrive_callback(data)

    @AsyncCall.Async
    def __send_test_signal(self, device, callback):
        ser = serial.Serial(device, 115200, timeout=1)
        ser.bytesize = serial.EIGHTBITS
        ser.parity = serial.PARITY_NONE
        ser.stopbits = serial.STOPBITS_ONE
        ser.write("+++")
        line = ser.readline()
        callback(line, device, ser)
