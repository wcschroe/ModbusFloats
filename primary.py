import minimalmodbus
import time
import serial
from ctypes import (Union, Array, c_uint16, c_float)

controller = None
try:
    controller = minimalmodbus.Instrument('COM21', 1)
except serial.serialutil.SerialException as e:
    print(e)
    quit()
controller.serial.timeout = .2
controller.serial.baudrate = 115200
controller.serial.bytesize = 8
controller.serial.parity = 'N'
controller.serial.stopbits = 1

class c_uint16_array(Array):
    _type_ = c_uint16
    _length_ = 2

class c_union(Union):
    _fields_ = ("i", c_uint16_array), ("f", c_float)

converter = c_union()

converter.f = 123.456789
controller.write_register(0, converter.i[0])
controller.write_register(1, converter.i[1])

converter.f = 987.654321
controller.write_register(2, converter.i[0])
controller.write_register(3, converter.i[1])