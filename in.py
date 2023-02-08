import serial

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
i = "hello\n"
ser.write(i.encode())
ser.close()
