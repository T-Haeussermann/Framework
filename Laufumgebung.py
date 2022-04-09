import time

import paho.mqtt.client as mqtt
import json
import threading


'''Variablen für MQTT-Broker'''
_username = "dbt"
_passwd = "dbt"
_host = "mq.jreichwald.de"
_port = 1883
_timeout = 60


class Digital_Twin:
    """Klasse Digital Twin, Quelle: https://medium.com/swlh/classes-subclasses-in-python-12b6013d9f3"""
    def __init__(self, name, typ):
        self.name = name
        self.typ = typ

    def DT_Ablauf(self):
        while True:
            print(self.name)
            time.sleep(5)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("Laufumgebung/#") #("Laufumgebung/#")


def on_message(client, userdata, msg):
    TopicUndNachricht = msg.topic + " : " + str(msg.payload.decode("utf-8")) #string
    Nachricht = json.loads(str(msg.payload.decode("utf-8")))
    if ("/Anforderung" in TopicUndNachricht and Nachricht['Task'] == "Erstelle DT"):
        print("Ich stelle DT mit dem Namen " + Nachricht['Name'] + " bereit!")
        Neuer_DT = Digital_Twin(Nachricht['Name'], Nachricht['Typ'])
        DT_Thread = threading.Thread(target=Digital_Twin.DT_Ablauf(Neuer_DT))
        DT_Thread.start()
        DT_Thread.join()
    # else:
    #      print ("DT existiert bereits")

client = mqtt.Client()
client.username_pw_set(_username, _passwd)
client.on_connect = on_connect
client.on_message = on_message
client.connect(_host, _port, _timeout)

# Payload=json.dumps({"Maschine-17": "Erstelle DT"})
# topic = "Laufumgebung"
# client.publish(topic, Payload)
print("ich bin die Laufumgebung")

client.loop_forever()