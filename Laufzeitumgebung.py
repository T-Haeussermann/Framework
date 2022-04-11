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

    ListeDT = [n for DT in threading.enumerate().getName[]]
    print(ListeDT)

    if ("/Anforderung" in TopicUndNachricht and Nachricht["Task"] == "Erstelle DT" and Nachricht["Name"] not in ListeDT):
        DT_nach_Typ_erstellen(Nachricht)

    elif (Nachricht["Name"] in threading.enumerate()):
        print("Ich lege keinen neuen DT an")

    if "/Messwert" in TopicUndNachricht:
        print(Nachricht["Messwert"])
        Messwert = Nachricht
        q.put(Messwert)
        print(q)
        print("Test")



def DT_nach_Typ_erstellen(Nachricht):
    if Nachricht["Typ"] == "ADT":
        print("Ich stelle DT mit dem Namen " + Nachricht["Name"] + " bereit!")
        Neuer_ADT = Asset_Digital_Twin(Nachricht["Name"], Nachricht["Typ"], Nachricht["Fähigkeit"])
        print(Neuer_ADT.Name + " vom Typ " + Neuer_ADT.Typ + " Aus der Laufzeitumgebung gesendet")
        DT_Thread = threading.Thread(name=Neuer_ADT.Name, target=Neuer_ADT.ADT_Ablauf)
        DT_Thread.start()
        print(DT_Thread.name + " name of thread")

    elif Nachricht["Typ"] == "PDDT":
        print("Ich stelle DT mit dem Namen " + Nachricht["Name"] + " bereit!")
        Neuer_PDDT = Product_Demand_Digital_Twin(Nachricht["Name"], Nachricht["Typ"], Nachricht["Bedarf"])
        print(Neuer_PDDT.Name + " vom Typ " + Neuer_PDDT.Typ + " Aus der Laufzeitumgebung gesendet")
        DT_Thread = threading.Thread(name=Neuer_PDDT.Name, target=Neuer_PDDT.PDDT_Ablauf)
        DT_Thread.start()
        print(DT_Thread.name + " name of thread")

    elif Nachricht["Typ"] == "DT":
        print("Ich stelle DT mit dem Namen " + Nachricht["Name"] + " bereit!")
        Neuer_DT = Digital_Twin(Nachricht["Name"], Nachricht["Typ"], q)
        print(Neuer_DT.Name + " vom Typ " + Neuer_DT.Typ + " Aus der Laufzeitumgebung gesendet")
        DT_Thread = threading.Thread(name=Neuer_DT.Name, target=Neuer_DT.DT_Ablauf)
        DT_Thread.start()
        print(DT_Thread.name + " name of thread")
        test = threading.enumerate()
        test2 = threading.enumerate()[4]
        print(test)
        if "Tester DT" in test2:
            print("so gehts")
        print(test2)


def Laufzeitumgebung():
    print("ich bin die Laufzeitumgebung")
    mqtt_connection()



if __name__ == '__main__':
    q = Queue()
    Laufzeitumgebung()