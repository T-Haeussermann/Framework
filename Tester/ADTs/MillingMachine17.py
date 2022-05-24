import paho.mqtt.client as mqtt
import json
from random import randrange
import time
import datetime


_username = "MillingMachine17"
_passwd = ""
_host = "127.0.0.1"
_port = 1883
_timeout = 60


"""PT-Name wird der Variablen Maschinenname und Typ zugewiesen. Variable Typ bestimmt welche Art von DT angelegt wird.
Fähigkeit nur für ADTs ausfüllen und Bedarf nur für PDDTs ausfüllen."""
Maschinenname = "MillingMachine17"
MaschinenTyp = "ADT"
Sensoren = ["S1", "S2", "S3", "S4"]
KritWerte = {"S1": 30, "S2": 50, "S3": 25, "S4":17}
Operatoren = {"S1": ">", "S2": "<", "S3": "<", "S4":">"}
Handlungen = {"S1": "Kraft erhoehen", "S2": "Kühlmittel aktivieren", "S3": "Gewicht erhöhen", "S4": "Backrate steigern"}
Skill = json.dumps({"offersProductionService": "MillingService", "TypeOfMaterial": "Metal",
                    "Geometrie": "Rechteck",
                    "Dimensionen": {"minLengthResource": 5.0, "maxLengthResource": 500.0,
                                    "minWidthResource": 5.0, "maxWidthResource": 200.0,
                                    "minDepth": 5.0, "maxDepth": 100.0, "minThickness": 5.0, "maxThickness": 200.0}})
Skill = json.loads(Skill)


'''Entscheidungsvariablen für die Vergabe von Aufträgen'''
Preise = json.dumps({"priceFunction": "exponentiell", "Exponent": 1.0, "Abschnitt": 50.0})
Preise = json.loads(Preise)

Zeiten = json.dumps({"timeFunction": "exponentiell", "Exponent": 0.5, "Abschnitt": 20.0})
Zeiten = json.loads(Zeiten)

Fehlerquote = 0.1


"""Alle benötigten Topics werden hier definiert"""
topic = "Laufzeitumgebung/" + Maschinenname + "/#"
topicAnforderung = "Laufzeitumgebung/" + Maschinenname + "/Anforderung"
topicMesswerte = "Laufzeitumgebung/" + Maschinenname + "/Messwerte"
topicHandlung = "Laufzeitumgebung/" + Maschinenname + "/Handlungen"

def on_connect(client, userdata, flags, rc):
    """Verbindung mit dem MQTT-Broker 1 aufbauen"""
    print("Connected with result code " + str(rc))
    client.subscribe("Laufzeitumgebung/" + Maschinenname + "/#")



def on_message(client, userdata, msg):
    """Hier werden Nachrichten zum Topic Handlungen empfangen, diese weisen den PT an was er auszuführen hat
    z. B. Kühlmittelzuführ aktivieren"""
    # print(msg.topic + " : " + str(msg.payload.decode("utf-8")))
    Nachricht = json.loads(str(msg.payload.decode("utf-8")))
    Topic = msg.topic
    if "Handlungen" in Topic:
        for Sensor in Handlungen:
            if Nachricht["Ausführen"] == Handlungen[Sensor]:
                print("Handlung : " + Handlungen[Sensor] + " eingeleitet")

    elif "Fertigung" in Topic:
        print("Ich stelle jetzt " + str(Nachricht["Bedarf"]) + " für " + str(Nachricht["Auftraggeber"]) + " her!")

    elif "Broker_Change" in Topic:
        _username = Nachricht["Username"]
        _passwd = Nachricht["Passwort"]
        _host = Nachricht["Host"]
        _port = int(Nachricht["Port"])
        client.username_pw_set(_username, _passwd)
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(_host, _port, _timeout)
        print("Broker gewechselt!")


client = mqtt.Client()
client.username_pw_set(_username, _passwd)
client.on_connect = on_connect
client.loop_start()
client.on_message = on_message
client.connect(_host, _port, _timeout)




Payload=json.dumps({"Name": Maschinenname, "Task": "Erstelle DT", "Typ": MaschinenTyp, "Sensoren": Sensoren,
                    "Kritische Werte": KritWerte, "Operatoren": Operatoren, "Handlungen": Handlungen,
                    "Skill": Skill, "Preise": Preise, "Zeiten": Zeiten, "Fehlerquote": Fehlerquote})
client.publish(topicAnforderung, Payload, 2)

while True:
    Messwert = json.dumps({"Name": Maschinenname, "Messwert": {"S1": randrange(100), "Einheit": "Newton"}})
    client.publish(topicMesswerte + "/S1", Messwert)
    Messwert = json.dumps({"Name": Maschinenname, "Messwert": {"S2": randrange(100), "Einheit": "Celsius"}})
    client.publish(topicMesswerte + "/S2", Messwert)
    Messwert = json.dumps({"Name": Maschinenname, "Messwert": {"S3": randrange(100), "Einheit": "Kilogramm"}})
    client.publish(topicMesswerte + "/S3", Messwert)
    Messwert = json.dumps({"Name": Maschinenname, "Messwert": {"S4": randrange(100), "Einheit": "Käsekuchen"}})
    client.publish(topicMesswerte + "/S4", Messwert)
    time.sleep(2)

