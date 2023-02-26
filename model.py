# pip3 install pyserial
import serial
import logging

from influxdb_client import InfluxDBClient, Point, WritePrecision


class Model:
    pass


class VirtualSerial(Model):
    def __init__(self, tty):
        self.tty = tty
        self.ser = None
        if not self.startSerial(tty):
            raise Exception("Can't open virtual serial port")

    def startSerial(self, tty_id):
        ser = serial.Serial(port=tty_id, timeout=None)
        # ser.close()
        # ser.open()
        if ser.isOpen():
            print(ser.name, ":connection successful.")
            self.ser = ser
            return True
        else:
            print(ser.name, ":connection failed.")
            return False

    def readSerial(self):
        if self.ser.in_waiting > 0:
            data = self.ser.read_until(b"\n")
            print(data.decode())
            return data.decode()
        else:
            return False

    def writeData(self, data):
        self.ser.write(data.encode())
        return True

    def closeSerial(self):
        self.ser.close()
        return True

    def openSerial(self):
        self.ser.open()
        return True


class Topic:
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def publish(self, data):
        self.data = data
        for subscriber in self.subscribers:
            subscriber.update(self)

    def getData(self):
        return self.data


class InfluxDataPoint:
    #      "point1": {
    #     "sensor": "sensor1",
    #     "id": "111",
    #     "value": 23,
    #   },
    def __init__(self, raw):
        pass