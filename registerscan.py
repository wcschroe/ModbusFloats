import minimalmodbus
import time
import serial
import numpy
from multiprocessing import Process

not_in_op = 0
left_in_op = 1
right_in_op = 2

doWeld = 0             #Triggers the weld cycle
stopWeld = 1
safe = 2           #Read only, is set when all doors / latches are closed / latched
# Safety inputs (0 or 1):
leftDoorLatched = 3
rightDoorLatched = 4
stationInOperation = 5 # 1 for left, 2 for right, 0 for neither
# Determines the size of the modbus registers array associated with this enum:
TOTAL_REGS_SIZE = 6
controller = None
try:
    controller = minimalmodbus.Instrument('COM20', 1)
except serial.serialutil.SerialException as e:
    print(e)
    quit()
controller.serial.timeout = .2
controller.serial.baudrate = 115200
controller.serial.bytesize = 8
controller.serial.parity = 'N'
controller.serial.stopbits = 1

controller.write_register(102, 0)
controller.write_register(103, 0)



while True:
    value = controller.read_register(77, number_of_decimals = 0)
    print(str(value))
