import serial
import sys
import os

def startSerial(tty_id):
    ser = serial.Serial(port = tty_id, timeout = None)
    ser.close()
    ser.open()
    if ser.isOpen():
        print(ser.name, ":connection successful.")
        return ser
    else:
        print(ser.name, ":connection failed.")
        return False


# read from argument
tty_id = os.sys.argv[1]

ser = startSerial("/dev/"+tty_id)

sys.stdout.write(str(ser.read_until(b"\n"), encoding="utf-8"))
sys.stdout.flush()

ser.close()
