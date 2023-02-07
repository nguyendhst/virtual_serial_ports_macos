import serial

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


ser = startSerial("/dev/ttys008")
i = "hello\n"
ser.write(i.encode())
ser.close()
