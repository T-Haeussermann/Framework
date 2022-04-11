from Class_DT import Asset_Digital_Twin, Product_Demand_Digital_Twin
import time
import paho.mqtt.client as mqtt
import json
import os
import time

Maschinenname = Dummy_DT

testA = Asset_Digital_Twin("Name", "MeinPT", "ADT", "fräsen", "10h", "ausgelastet")
testB = Product_Demand_Digital_Twin("Name", "MeinPT", "PDDT", "20er Loch", "heute")
print(testA.capacity)
print(vars(testB))

_username = "dbt"
_passwd = "dbt"
_host = "mq.jreichwald.de"
_port = 1883
_timeout = 60


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("Laufumgebung/" + Maschinenname + "/Messwert")  # ("Laufumgebung/#")


def on_message(client, userdata, msg):
    # print(msg.topic + " : " + str(msg.payload.decode("utf-8")))
    msg = json.loads(str(msg.payload.decode("utf-8")))
    Messwert = msg["Messwert"]
    Einheit = msg["Einheit"]
    print("Der Messwert liegt bei " + Messwert + " und die Einheit ist " + Einheit)


client = mqtt.Client()
client.username_pw_set(_username, _passwd)
client.on_connect = on_connect
client.on_message = on_message
client.connect(_host, _port, _timeout)

Payload=json.dumps({"Maschine-17": "Erstelle DT"})
topic = "Laufumgebung"
client.publish(topic, Payload)

client.loop_forever()