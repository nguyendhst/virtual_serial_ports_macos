import sys
from Adafruit_IO import MQTTClient

import configparser

import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


# import logging
# logging.basicConfig(level=logging.INFO)

# from simpleAi import *
# from uart import *
from model import *


class AdafruitIO:
    def __init__(self) -> None:
        self.client = None
        self.username = None
        self.key = None
        self.feeds = None
        self.setProfile()

    def setProfile(self):
        # read config file
        try:
            conf = configparser.ConfigParser()
            conf.read("conf.ini")
            print("Config file found")

            self.username = conf["DEFAULT"]["Username"]
            self.key = conf["DEFAULT"]["Key"]
            self.feeds = conf["DEFAULT"]["Feeds"].split(",")
            print("Username: ", str(self.username))
            print("Key: ", str(self.key))
            print("Feeds: ", str(self.feeds))
        except:
            raise Exception("Problem reading config file")

    def connected(self, client):
        print("Connected to server")
        print("Subscribing to feed: ", self.feeds)
        for topic in self.feeds:
            self.subscribe(topic)

    def subscribed(self, client, userdata, mid, granted_qos):
        print("Subscribe success")

    def disconnected(self, client):
        print("Disconnected from server")
        sys.exit(1)

    def message(self, feed_id, payload):
        print("Received message: " + payload + ", feed_id: " + feed_id)

    def connect(self):
        self.client = MQTTClient(self.username, self.key)
        self.client.on_connect = lambda client: self.connected(client)

        self.client.on_subscribe = (
            lambda client, userdata, mid, granted_qos: self.subscribed(
                client, userdata, mid, granted_qos
            )
        )
        self.client.on_disconnect = lambda client: self.disconnected(client)

        self.client.on_message = lambda feed_id, payload: self.message(feed_id, payload)

        try:
            self.client.connect()
            self.client.loop_background()
        except:
            raise Exception("Connect to Adafruit IO failed")

    def publish(self, feed_id, data):
        self.client.publish(feed_id, data)

    def subscribe(self, feed_id):
        self.client.subscribe(feed_id)

    def disconnect(self):
        self.client.disconnect()

    def loop(self):
        self.client.loop()


class InfluxDB:
    def __init__(self) -> None:
        self.url = None
        self.token = None
        self.org = None
        self.bucket = None
        self.client = None
        self.setProfile()

    def setProfile(self):
        # read config file
        try:
            conf = configparser.ConfigParser()
            conf.read("conf.ini")
            print("Config file found")

            self.url = conf["INFLUXDB"]["URL"]
            self.token = conf["INFLUXDB"]["TOKEN"]
            self.org = conf["INFLUXDB"]["ORG"]
            self.bucket = conf["INFLUXDB"]["BUCKET"]
            print("Url: ", str(self.url))
            print("Token: ", str(self.token))
            print("Org: ", str(self.org))
            print("Bucket: ", str(self.bucket))
        except:
            raise Exception("Problem reading config file")

    def connect(self):
        print("Connecting to InfluxDB...")
        try:
            self.client = influxdb_client.InfluxDBClient(
                url=self.url, token=self.token, org=self.org
            )
            self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
            print("Connected to InfluxDB")
        except:
            raise Exception("Connect to InfluxDB failed")

    def write(self, data):
        self.write_api.write(self.bucket, self.org, data)

    def disconnect(self):
        self.client.close()

    def formatInput(self, raw):
        self.raw = raw
        # format: sensor,id=123 value=123
        data = self.raw.split(",")
        if len(data) != 2:
            return

        self.sensor = data[0]
        data = data[1].split(" ")
        if len(data) != 2:
            return

        self.id = data[0].split("=")[1]
        self.value = data[1].split("=")[1]

        return (
            Point("Celcius")
            .tag("sensor", self.sensor)
            .tag("id", self.id)
            .field("value", int(self.value))
        )


# class Profile:
#     def __init__(self) -> None:
#         self.client = None
#         self.username = None
#         self.key = None
#         self.feeds = None
#         self.setProfile()

#     def setProfile(self):
#         # read config file
#         try:
#             conf = configparser.ConfigParser()
#             conf.read("conf.ini")
#             print("Config file found")

#             self.username = conf["DEFAULT"]["Username"]
#             self.key = conf["DEFAULT"]["Key"]
#             self.feeds = conf["DEFAULT"]["Feeds"].split(",")
#             print("Username: ", str(self.username))
#             print("Key: ", str(self.key))
#             print("Feeds: ", str(self.feeds))
#         except:
#             raise Exception("Problem reading config file")

#     def connected(self, client):
#         print("Connected to server")
#         print("Subscribing to feed: ", self.feeds)
#         for topic in self.feeds:
#             self.subscribe(topic)

#     def subscribed(self, client, userdata, mid, granted_qos):
#         print("Subscribe success")

#     def disconnected(self, client):
#         print("Disconnected from server")
#         sys.exit(1)

#     def message(self, feed_id, payload):
#         print("Received message: " + payload + ", feed_id: " + feed_id)

#     def connect(self):
#         self.client = MQTTClient(self.username, self.key)
#         self.client.on_connect = lambda client: self.connected(client)

#         self.client.on_subscribe = (
#             lambda client, userdata, mid, granted_qos: self.subscribed(
#                 client, userdata, mid, granted_qos
#             )
#         )
#         self.client.on_disconnect = lambda client: self.disconnected(client)

#         self.client.on_message = lambda feed_id, payload: self.message(feed_id, payload)

#         try:
#             self.client.connect()
#             self.client.loop_background()
#         except:
#             raise Exception("Connect to Adafruit IO failed")

#     def publish(self, feed_id, data):
#         self.client.publish(feed_id, data)

#     def subscribe(self, feed_id):
#         self.client.subscribe(feed_id)

#     def disconnect(self):
#         self.client.disconnect()

#     def loop(self):
#         self.client.loop()


class Controller:
    def __init__(self, mode) -> None:
        # change data profile here
        self.profile = AdafruitIO()
        # self.profile = InfluxDB()

        self.profile.connect()
        if mode == "virtual":
            self.serial = VirtualSerial("/dev/ttys012")
        else:
            # TODO
            self.serial = Serial("/dev/ttyUSB0")

    def writeData(self, data):
        self.serial.writeData(data)

    def readSerial(self):
        return self.serial.readSerial()

    def processData(self, data):
        if len(data) == 0:
            return

        # format: feed:data
        # data = data.split(":")
        # if len(data) != 2:
        #     return

        # feed = data[0]
        # data = data[1]
        # self.profile.publish(feed, data)
        self.profile.write(self.profile.formatInput(data))


# counter = 10
# counter_ai = 4

# while True:
# counter = counter - 1
# if counter <=0:
#     counter = 10
# TODO
# print("Random data publish")
# temp = random.randint(20,40)
# client.publish("cambien1", temp)
# humidity = random.randint(20,40)
# client.publish("cambien3", humidity)
# light = random.randint(20,40)
# client.publish("cambien2", light)

# counter_ai =  counter_ai - 1
# if counter_ai <= 0:
#     counter_ai = 4
#     ai_result = image_detector()
#     print("Output: ", ai_result)
#     client.publish("ai", ai_result)

# readSerial(client)
# time.sleep(1)
# pass
# tty_id = os.sys.argv[1]

# ser = startSerial("/dev/"+tty_id)

# sys.stdout.write(str(ser.read_until(b"\n"), encoding="utf-8"))
# sys.stdout.flush()


# def processData(client, data):
#     print("processData:", data)
#     if (len(data) == 0):
#         print("len(data) == 0")
#         return
#     data = data.replace("!", "")
#     data = data.replace("#", "")
#     splitData = data.split(":")
#     print(splitData)
#     if splitData[1] == "T":
#         print("pub", splitData[2])
#         client.publish("sensor1", splitData[2])


# mess = ""
# def readSerial(client):
#     bytesToRead = ser.in_waiting
#     # print(ser)
#     if (bytesToRead > 0):
#         print("bytesToRead:", bytesToRead)
#         global mess
#         mess = mess + ser.read(bytesToRead).decode("UTF-8")
#         # print(mess)
#         while ("#" in mess) and ("!" in mess):
#             mess = mess.replace("\n", "")

#             start = mess.find("!")
#             end = mess.find("#")
#             print("mess:", mess[start:end + 1])
#             processData(client, mess[start:end + 1])
#             if (end == len(mess)):
#                 mess = ""
#             else:
#                 mess = mess[end+1:]

# def writeData(data):
#     ser.write(str(data).encode())
