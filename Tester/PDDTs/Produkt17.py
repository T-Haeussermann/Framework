import paho.mqtt.client as mqtt
import json
from random import randrange
import time


_username = "Produkt17"
_passwd = ""
_host = "127.0.0.1"
_port = 1883
_timeout = 60


"""PT-Name wird der Variablen Maschinenname und Typ zugewiesen. Variable Typ bestimmt welche Art von DT angelegt wird.
Fähigkeit nur für ADTs ausfüllen und Bedarf nur für PDDTs ausfüllen."""
Maschinenname = "Produkt17"
MaschinenTyp = "PDDT"
#Bedarf = json.dumps({"ProductionService": "DrillingService", "processToM": "Metal", "Geometrie": "Kreis",
#                     "Dimensionen": {"DiameterHoleResource": 15.0, "Depth": 30.0, "Thickness": 55.0}})
Bedarf = json.dumps({"Schritt 1": {"ProductionService": "DrillingService", "TypeOfMaterial": "Metal",
                                   "Geometrie": "Kreis",
                                   "Dimensionen": {"DiameterHoleResource": 15.0, "Depth": 30.0, "Thickness": 55.0}},
                     "Schritt 2": {"ProductionService": "MillingService", "TypeOfMaterial": "Metal",
                                   "Geometrie": "Rechteck",
                                   "Dimensionen": {"LengthResource": 15.0, "WidthResource": 5.0,
                                                   "Depth": 30.0, "Thickness": 55.0}},
                     "Schritt 3": {"ProductionService": "StampingService", "TypeOfMaterial": "Metal",
                                   "Geometrie": "Rechteck",
                                   "Dimensionen": {"LengthResource": 15.0, "WidthResource": 5.0,
                                                   "Depth": 30.0, "Thickness": 55.0}},
                     "Schritt 4": {"ProductionService": "WeldingService", "TypeOfMaterial": "Metal",
                                   "Geometrie": "Rechteck",
                                   "Dimensionen": {"LengthResource": 15.0, "Thickness": 55.0}}})
Bedarf = json.loads(Bedarf)

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
    print(msg.topic + " : " + str(msg.payload.decode("utf-8")))
    # msg = json.loads(str(msg.payload.decode("utf-8")))
    # if msg["Ausführen"] == Handlung:
    #     print("Ich nehme zu")


client = mqtt.Client()
client.username_pw_set(_username, _passwd)
client.on_connect = on_connect
client.loop_start()
client.on_message = on_message
client.connect(_host, _port, _timeout)



Payload=json.dumps({"Name": Maschinenname, "Typ": MaschinenTyp, "Task": "Erstelle DT", "Bedarf": Bedarf})
client.publish(topicAnforderung, Payload, 2)
while True:

    time.sleep(2)

