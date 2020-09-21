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
mbPort2 = None
try:
    mbPort2 = minimalmodbus.Instrument('COM20', 1)
except serial.serialutil.SerialException as e:
    print(e)
    quit()
mbPort2.serial.timeout = .2
mbPort2.serial.baudrate = 115200
mbPort2.serial.bytesize = 8
mbPort2.serial.parity = 'N'
mbPort2.serial.stopbits = 1

mbPort3 = None
try:
    mbPort3 = minimalmodbus.Instrument('COM21', 1)
except serial.serialutil.SerialException as e:
    print(e)
    quit()
mbPort3.serial.timeout = .2
mbPort3.serial.baudrate = 115200
mbPort3.serial.bytesize = 8
mbPort3.serial.parity = 'N'
mbPort3.serial.stopbits = 1

def writePort2():
    try:
        mbPort2.write_register(0, 2)
    except:
        pass

def writePort3():
    try:
        mbPort3.write_register(0, 3)
    except:
        pass

def readPort2():
    try:
        print(str(mbPort2.read_register(0)))
    except:
        pass

def runInParallel(*fns):
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()

while(True):
    runInParallel(writePort2, writePort3, readPort2)