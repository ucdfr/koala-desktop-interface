__author__ = 'yilu'
import sys
import glob
import serial
from serial.tools import list_ports

# def serial_ports():
#     """Lists serial ports
#
#     :raises EnvironmentError:
#         On unsupported or unknown platforms
#     :returns:
#         A list of available serial ports
#     """
#     if sys.platform.startswith('win'):
#         ports = ['COM' + str(i + 1) for i in range(256)]
#
#     elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
#         # this is to exclude your current terminal "/dev/tty"
#         ports = glob.glob('/dev/tty[A-Za-z]*')
#
#     elif sys.platform.startswith('darwin'):
#         ports = glob.glob('/dev/tty.*')
#
#     else:
#         raise EnvironmentError('Unsupported platform')
#
#     result = []
#     for port in ports:
#         try:
#             s = serial.Serial(port)
#             s.close()
#             result.append(port)
#         except (OSError, serial.SerialException):
#             pass
#     return result
#
# for port_name, port_desc, hw_id in list_ports.comports():
#     print "{0} is present as {1}, {2}".format(port_name, port_desc, hw_id)
#         # with serial.Serial(port=port_name, **device_serial_settings) as ser:
#         #     ser.write(status_request_string)
#         #     if ser.readline().startswith(expected_response):
#         #         device_port = port_name
#         #         break
#
#
# if __name__ == '__main__':
#     print(serial_ports())