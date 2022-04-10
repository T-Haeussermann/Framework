import paho.mqtt.client as mqtt
import json
import threading
import multiprocessing
import asyncio
from Class_DT import Digital_Twin


'''Variablen für MQTT-Broker'''
_username = "dbt"
_passwd = "dbt"
_host = "mq.jreichwald.de"
_port = 1883
_timeout = 60


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("Laufumgebung/#") #("Laufumgebung/#")


def on_message(client, userdata, msg):
    TopicUndNachricht = msg.topic + " : " + str(msg.payload.decode("utf-8")) #string
    Nachricht = json.loads(str(msg.payload.decode("utf-8")))

    if ("/Anforderung" in TopicUndNachricht and Nachricht["Task"] == "Erstelle DT" and Nachricht["Name"] not in threading.enumerate()):
        print("Ich stelle DT mit dem Namen " + Nachricht["Name"] + " bereit!")
        Neuer_DT = Digital_Twin(Nachricht["Name"], Nachricht["Typ"])
        print(Neuer_DT.Name + " vom Typ " + Neuer_DT.Typ + " Aus der Laufumgebung gesendet")
        DT_Thread = threading.Thread(name=Neuer_DT.Name, target=Neuer_DT.DT_Ablauf)
        DT_Thread.start()
        print(DT_Thread.name + " name of thread")

    elif (Nachricht["Name"] in threading.enumerate()):
        print("Ich lege keinen neuen DT an")



def Laufumgebung():
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

if __name__ == '__main__':
    Laufumgebung()