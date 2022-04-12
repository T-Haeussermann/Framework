import paho.mqtt.client as mqtt
import json
from random import randrange
import time


_username = "dbt"
_passwd = "dbt"
_host = "mq.jreichwald.de"
_port = 1883
_timeout = 60


"""PT-Name wird der Variablen Maschinenname und Typ zugewiesen. Variable Typ bestimmt welche Art von DT angelegt wird.
Fähigkeit nur für ADTs ausfüllen und Bedarf nur für PDDTs ausfüllen."""
Maschinenname = "Tester_ADT"
MaschinenTyp = "ADT"
Fähigkeit = "Ich kann"


"""Alle benötigten Topics werden hier definiert"""
topic = "Laufzeitumgebung/" + Maschinenname + "/#"
topicAnforderung = "Laufzeitumgebung/" + Maschinenname + "/Anforderung"
topicMesswerte = "Laufzeitumgebung/" + Maschinenname + "/Messwert"
topicHandlung = "Laufzeitumgebung/" + Maschinenname + "/Handlung"

def on_connect(client, userdata, flags, rc):
    """Verbindung mit dem MQTT-Broker 1 aufbauen"""
    print("Connected with result code " + str(rc))
    client.subscribe("Laufzeitumgebung/PT-17/Handlung")



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



Payload=json.dumps({"Name": Maschinenname, "Typ": MaschinenTyp, "Task": "Erstelle DT", "Fähigkeit": Fähigkeit})
client.publish(topicAnforderung, Payload)



while True:
    Messwert=json.dumps({"Name": Maschinenname, "Messwert": randrange(100), "Einheit": "Celsius"})
    client.publish(topicMesswerte, Messwert)
    time.sleep(2)
    client.loop()
