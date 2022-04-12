import paho.mqtt.client as mqtt
import json
import threading
from Class_DT import Digital_Twin, Asset_Digital_Twin, Product_Demand_Digital_Twin
from queue import Queue

'''Variablen für MQTT-Broker'''
_username = "dbt"
_passwd = "dbt"
_host = "mq.jreichwald.de"
_port = 1883
_timeout = 60



def mqtt_connection():
    client = mqtt.Client()
    client.username_pw_set(_username, _passwd)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(_host, _port, _timeout)
    client.loop_forever()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("Laufzeitumgebung/#")

def on_message(client, userdata, msg):
    TopicUndNachricht = msg.topic + " : " + str(msg.payload.decode("utf-8")) #string
    Nachricht = json.loads(str(msg.payload.decode("utf-8")))

    ListeDT = []
    for thread in threading.enumerate():
        ListeDT.append(thread.name)


    if "/Anforderung" in TopicUndNachricht and Nachricht["Task"] == "Erstelle DT" and Nachricht["Name"] not in str(ListeDT):
        DT_nach_Typ_erstellen(Nachricht)

    elif "/Anforderung" in TopicUndNachricht and Nachricht["Task"] == "Erstelle DT" and Nachricht["Name"] in str(ListeDT):
        print("Ich lege keinen neuen DT an")

    if "/Messwert" in TopicUndNachricht:
        Empfänger = Nachricht["Name"]
        # print(Nachricht["Messwert"])
        Messwert = Nachricht["Messwert"]
        globals()[Empfänger].Q.put(Messwert)



def DT_nach_Typ_erstellen(Nachricht):
    if Nachricht["Typ"] == "ADT":
        print("Ich stelle DT mit dem Namen " + Nachricht["Name"] + " bereit!")
        Neuer_ADT = Nachricht["Name"]
        globals()[Neuer_ADT] = Asset_Digital_Twin(Nachricht["Name"], Nachricht["Typ"], Nachricht["Fähigkeit"])
        print(globals()[Neuer_ADT].Name + " vom Typ " + globals()[Neuer_ADT].Typ + " Aus der Laufzeitumgebung gesendet")
        DT_Thread = threading.Thread(name=globals()[Neuer_ADT].Name, target=globals()[Neuer_ADT].ADT_Ablauf)
        DT_Thread.start()
        print(DT_Thread.name + " name of thread")

    elif Nachricht["Typ"] == "PDDT":
        print("Ich stelle DT mit dem Namen " + Nachricht["Name"] + " bereit!")
        Neuer_PDDT = Nachricht["Name"]
        globals()[Neuer_PDDT] = Product_Demand_Digital_Twin(Nachricht["Name"], Nachricht["Typ"], Nachricht["Bedarf"])
        print(globals()[Neuer_PDDT].Name + " vom Typ " + globals()[Neuer_PDDT].Typ + " Aus der Laufzeitumgebung gesendet")
        DT_Thread = threading.Thread(name=globals()[Neuer_PDDT].Name, target=globals()[Neuer_PDDT].PDDT_Ablauf)
        DT_Thread.start()
        print(DT_Thread.name + " name of thread")

    elif Nachricht["Typ"] == "DT":
        print("Ich stelle DT mit dem Namen " + Nachricht["Name"] + " bereit!")
        Neuer_DT = Nachricht["Name"]
        globals()[Neuer_DT] = Digital_Twin(Nachricht["Name"], Nachricht["Typ"])
        print(globals()[Neuer_DT].Name + " vom Typ " + globals()[Neuer_DT].Typ + " Aus der Laufzeitumgebung gesendet")
        DT_Thread = threading.Thread(name=globals()[Neuer_DT].Name, target=globals()[Neuer_DT].DT_Ablauf)
        DT_Thread.start()
        print(DT_Thread.name + " name of thread")


def Laufzeitumgebung():
    print("ich bin die Laufzeitumgebung")
    mqtt_connection()



if __name__ == '__main__':
    Laufzeitumgebung()