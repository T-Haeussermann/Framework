import paho.mqtt.client as mqtt
import json
import threading
from Class_DT import Digital_Twin, Asset_Digital_Twin, Product_Demand_Digital_Twin
from queue import Queue

'''Variablen für MQTT-Broker 1'''
_username = "dbt"
_passwd = "dbt"
_host = "mq.jreichwald.de"
_port = 1883
_timeout = 60

'''Variablen für MQTT-Broker 2'''
_username = ""
_passwd = ""
_host = "127.0.0.1"
_port = 1883
_timeout = 60

'''Variablen'''
ListeDTs = []



def mqtt_connection():
    client = mqtt.Client()
    client.username_pw_set(_username, _passwd)
    client.on_connect = on_connect
    client.on_message = on_message
    #client.on_publish = on_publish
    client.connect(_host, _port, _timeout)
    client.loop_forever()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("Laufzeitumgebung/#")

def on_message(client, userdata, msg):
    TopicUndNachricht = msg.topic + " : " + str(msg.payload.decode("utf-8")) #string
    Nachricht = json.loads(str(msg.payload.decode("utf-8")))

    ListeThreads = []
    for thread in threading.enumerate():
        ListeThreads.append(thread.name)


    if "/Anforderung" in TopicUndNachricht and Nachricht["Task"] == "Erstelle DT" and Nachricht["Name"] not in str(ListeThreads):
        DT_nach_Typ_erstellen(Nachricht)

    elif "/Anforderung" in TopicUndNachricht and Nachricht["Task"] == "Erstelle DT" and Nachricht["Name"] in str(ListeThreads):
        print("Ich lege keinen neuen DT an")

    if "/Messwert" in TopicUndNachricht:
        Empfänger = getTwin(Nachricht["Name"])
        Empfänger.Q.put(Nachricht)



def DT_nach_Typ_erstellen(Nachricht):
    if Nachricht["Typ"] == "ADT":
        print("Ich stelle DT mit dem Namen " + Nachricht["Name"] + " bereit!")
        Neuer_ADT = Asset_Digital_Twin(Nachricht["Name"], Nachricht["Typ"], Nachricht["Fähigkeit"])
        ListeDTs.append(Neuer_ADT)
        print(Neuer_ADT.Name + " vom Typ " + Neuer_ADT.Typ + " Aus der Laufzeitumgebung gesendet")
        DT_Thread = threading.Thread(name=Neuer_ADT.Name, target=Neuer_ADT.ADT_Ablauf)
        DT_Thread.start()
        print(DT_Thread.name + " name of thread")

    elif Nachricht["Typ"] == "PDDT":
        print("Ich stelle DT mit dem Namen " + Nachricht["Name"] + " bereit!")
        Neuer_PDDT = Product_Demand_Digital_Twin(Nachricht["Name"], Nachricht["Typ"], Nachricht["Bedarf"])
        ListeDTs.append(Neuer_PDDT)
        print(Neuer_PDDT.Name + " vom Typ " + Neuer_PDDT.Typ + " Aus der Laufzeitumgebung gesendet")
        DT_Thread = threading.Thread(name=Neuer_PDDT.Name, target=Neuer_PDDT.PDDT_Ablauf)
        DT_Thread.start()
        print(DT_Thread.name + " name of thread")

    elif Nachricht["Typ"] == "DT":
        print("Ich stelle DT mit dem Namen " + Nachricht["Name"] + " bereit!")
        Neuer_DT = Digital_Twin(Nachricht["Name"], Nachricht["Typ"])
        ListeDTs.append(Neuer_DT)
        print(Neuer_DT.Name + " vom Typ " + Neuer_DT.Typ + " Aus der Laufzeitumgebung gesendet")
        DT_Thread = threading.Thread(name=Neuer_DT.Name, target=Neuer_DT.DT_Ablauf)
        DT_Thread.start()
        print(DT_Thread.name + " name of thread")


def getTwin(Name):
    for Digital_Twin in ListeDTs:
        if Digital_Twin.Name == Name:
            return Digital_Twin
    return None

def Laufzeitumgebung():
    print("ich bin die Laufzeitumgebung")
    mqtt_connection()



if __name__ == '__main__':
    Laufzeitumgebung()
