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
Maschinenname = "Tester_PDDT"
MaschinenTyp = "PDDT"
Bedarf = json.dumps({"Art": "Loch", "Geometrie": "Kreis",
                     "Dimensionen": {"Dimension X": 20, "Dimension Y": 20, "Dimension Z": 20, "Material": "ST 37"}})


"""Alle benötigten Topics werden hier definiert"""
topic = "Laufzeitumgebung/" + Maschinenname + "/#"
topicAnforderung = "Laufzeitumgebung/" + Maschinenname + "/Anforderung"
topicBedarf = "Laufzeitumgebung/" + Maschinenname + "/Bedarf"

def on_connect(client, userdata, flags, rc):
    """Verbindung mit dem MQTT-Broker 1 aufbauen"""
    print("Connected with result code " + str(rc))
    client.subscribe("Laufzeitumgebung/" + Maschinenname + "/Handlung")



def on_message(client, userdata, msg):
    """Hier werden Nachrichten zum Topic Handlungen empfangen, diese weisen den PT an was er auszukühlen hat
    z. B. Kühlmittelzuführ aktivieren"""
    #print(msg.topic + " : " + str(msg.payload.decode("utf-8")))
    msg = json.loads(str(msg.payload.decode("utf-8")))
    if msg["Ausführen"] == Handlung:
        print("Ich nehme zu")


client = mqtt.Client()
client.username_pw_set(_username, _passwd)
client.on_connect = on_connect
client.loop_start()
client.on_message = on_message
client.connect(_host, _port, _timeout)



Payload=json.dumps({"Name": Maschinenname, "Typ": MaschinenTyp, "Task": "Erstelle DT", "Bedarf": json.loads(Bedarf)})
while True:
    client.publish(topicAnforderung, Payload)
    time.sleep(2)

