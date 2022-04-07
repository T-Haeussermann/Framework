import paho.mqtt.client as mqtt
import json
import os
import time


_username = "dbt"
_passwd = "dbt"
_host = "mq.jreichwald.de"
_port = 1883
_timeout = 60


"""PT-Name wird der Variablen Maschinenname zugewiesen"""
Maschinenname = "Prüfmaschine"


"""Alle benötigten Topics werden hier definiert"""
topic = "Laufumgebung/" + Maschinenname + "/#"
topicAnforderung = "Laufumgebung/" + Maschinenname + "/Anforderung"
topicMesswerte = "Laufumgebung/" + Maschinenname + "/Messwert"
topicHandlung = "Laufumgebung/" + Maschinenname + "/Handlung"

def on_connect(client, userdata, flags, rc):
    """Verbindung mit dem MQTT-Broker 1 aufbauen"""
    print("Connected with result code " + str(rc))
    client.subscribe("Laufumgebung/PT-17/Handlung")



def on_message(client, userdata, msg):
    """Hier werden Nachrichten zum Topic Handlungen empfangen, diese weisen den PT an was er auszukühlen hat
    z. B. Kühlmittelzuführ aktivieren"""
    #print(msg.topic + " : " + str(msg.payload.decode("utf-8")))
    msg = json.loads(str(msg.payload.decode("utf-8")))
    print(msg)
    if msg["Ausführen"] == "Kühlmittel aktivieren":
        print("Ich aktiviere das Kühlmittel")

client = mqtt.Client()
client.username_pw_set(_username, _passwd)
client.on_connect = on_connect
client.on_message = on_message
client.connect(_host, _port, _timeout)



Payload=json.dumps({"Name": Maschinenname, "Task": "Erstelle DT"})
client.publish(topicAnforderung, Payload)



while True:
    Messwert=json.dumps({"Name": Maschinenname, "Messwert": "20", "Einheit": "Celsius"})
    client.publish(topicMesswerte, Messwert)
    client.on_message = on_message
    time.sleep(2)
    client.loop_forever()
