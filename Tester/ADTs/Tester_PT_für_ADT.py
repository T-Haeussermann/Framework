import paho.mqtt.client as mqtt
import json
from random import randrange
import time
import datetime


_username = "dbt"
_passwd = "dbt"
_host = "mq.jreichwald.de"
_port = 1883
_timeout = 60


"""PT-Name wird der Variablen Maschinenname und Typ zugewiesen. Variable Typ bestimmt welche Art von DT angelegt wird.
Fähigkeit nur für ADTs ausfüllen und Bedarf nur für PDDTs ausfüllen."""
Maschinenname = "Tester_ADT"
MaschinenTyp = "ADT"
Sensoren = ["S1", "S2", "S3", "S4"]
KritWerte = {"S1": 30, "S2": 50, "S3": 25, "S4":17}
Operatoren = {"S1": ">", "S2": "<", "S3": "<", "S4":">"}
Handlungen = {"S1": "Kraft erhoehen", "S2": "Kühlmittel aktivieren", "S3": "Gewicht erhöhen", "S4": "Backrate steigern"}
Skill = json.dumps({"Art": "Bohren", "Material": "ST 37", "Geometrie": "Kreis",
                        "Dimensionen": {"Dimension X": [5, 20], "Dimension Y": [5, 20], "Dimension Z": 20}})
Skill = json.loads(Skill)


'''Entscheidungsvariablen für die Vergabe von Aufträgen'''
Preise = json.dumps({"Kreis D5": 5, "Kreis D6": 6, "Kreis D7": 7, "Kreis D8": 8, "Kreis D9": 9, "Kreis D10": 10,
                    "Kreis D11": 11, "Kreis D12": 12, "Kreis D13": 13, "Kreis D14": 14, "Kreis D15": 15,
                    "Kreis D16": 16, "Kreis D17": 17, "Kreis D18": 18, "Kreis D19": 19, "Kreis D20": 20})
Preise = json.loads(Preise)

Zeiten = json.dumps({"Kreis D5": 50, "Kreis D6": 60, "Kreis D7": 70, "Kreis D8": 80, "Kreis D9": 90, "Kreis D10": 100,
                    "Kreis D11": 110, "Kreis D12": 120, "Kreis D13": 130, "Kreis D14": 140, "Kreis D15": 150,
                   "Kreis D16": 160, "Kreis D17": 170, "Kreis D18": 180, "Kreis D19": 190, "Kreis D20": 200})
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

    if "Fertigung" in Topic:
        print("Ich stelle jetzt " + str(Nachricht["Bedarf"]) + " für " + str(Nachricht["Auftraggeber"]) + " her!")


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

