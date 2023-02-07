import serial
import sys

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

def decodeSerial(ser):
    i = ser.read_until(b"1")
    return i

ser = startSerial("/dev/ttys009")

sys.stdout.write(str(ser.read_until(b"\n"), encoding="utf-8"))
sys.stdout.flush()

ser.close()