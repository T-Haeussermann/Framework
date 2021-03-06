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
Maschinenname = "Tester_DT"
MaschinenTyp = "DT"
KritWert = 50
Operator = ">"
Handlung = "Kuehlmittel aktivieren"


"""Alle benötigten Topics werden hier definiert"""
topic = "Laufzeitumgebung/" + Maschinenname + "/#"
topicAnforderung = "Laufzeitumgebung/" + Maschinenname + "/Anforderung"
topicMesswerte = "Laufzeitumgebung/" + Maschinenname + "/Messwert"
topicHandlung = "Laufzeitumgebung/" + Maschinenname + "/Handlung"

def on_connect(client, userdata, flags, rc):
    """Verbindung mit dem MQTT-Broker 1 aufbauen"""
    print("Connected with result code " + str(rc))
    client.subscribe(topicHandlung)



def on_message(client, userdata, msg):
    """Hier werden Nachrichten zum Topic Handlungen empfangen, diese weisen den PT an was er auszukühlen hat
    z. B. Kühlmittelzuführ aktivieren"""
    print(msg.topic + " : " + str(msg.payload.decode("utf-8")))



client = mqtt.Client()
client.username_pw_set(_username, _passwd)
client.on_connect = on_connect
client.loop_start()
client.on_message = on_message
client.connect(_host, _port, _timeout)


Payload=json.dumps({"Name": Maschinenname, "Typ": MaschinenTyp, "Task": "Erstelle DT", "Kritischer Wert": KritWert,
                    "Operator": Operator, "Handlung": Handlung})
i = 0
while True:
    if i < 2:
        client.publish(topicAnforderung, Payload)
        i = i + 1
    #Messwert = json.dumps({"Name": Maschinenname, "Messwert": 17, "Einheit": "Celsius"})
    Messwert = json.dumps({"Name": Maschinenname, "Nachricht": "Ich bin halt auch dabei"})
    client.publish(topicMesswerte, Messwert)
    time.sleep(2)


