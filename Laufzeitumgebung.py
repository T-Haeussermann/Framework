import time
import json
import threading
from Class_DT import Digital_Twin, Asset_Digital_Twin, Product_Demand_Digital_Twin
from MQTT import MQTT
import pandas
from collections import ChainMap

'''Variablen für MQTT-Broker 1'''
_username1 = "dbt"
_passwd1 = "dbt"
_host1 = "mq.jreichwald.de"
_port1 = 1883
_timeout1 = 60
_topic_sub1 = "Laufzeitumgebung/#"

'''Variablen für MQTT-Broker 2'''
_username2 = ""
_passwd2 = ""
_host2 = "127.0.0.1"
_port2 = 1883
_timeout2 = 60
_topic_sub2 = "Test"

'''Weitere Variablen'''
ListeDTs = []



def Nachricht_auswerten(TopicUndNachricht):
    Topic = TopicUndNachricht["Topic"]
    Nachricht = TopicUndNachricht["Nachricht"]
    Nachricht = json.loads(Nachricht)

    ListeThreads = []
    for thread in threading.enumerate():
        ListeThreads.append(thread.name)


    if "/Anforderung" in Topic:
            if Nachricht["Task"] == "Erstelle DT":
                if Nachricht["Name"] not in str(ListeThreads):
                    DT_nach_Typ_erstellen(Nachricht)

    elif "/Anforderung" in Topic and Nachricht["Task"] == "Erstelle DT" and Nachricht["Name"] in str(ListeThreads):
        print("Ich lege keinen neuen DT an")

    if "/Messwert" in Topic:
        Empfänger = getTwin(Nachricht["Name"])
        Empfänger.Q.put(Nachricht)



def DT_nach_Typ_erstellen(Nachricht):
    '''Prüft die eingehende Nachricht auf den Typ des DTs und instanziiert davon abhänig einen ADT, PDDT oder DT aus der Klasse DT'''
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
    '''Sucht den eingehenden Namen in der Liste der DTs'''
    for Digital_Twin in ListeDTs:
        if Digital_Twin.Name == Name:
            return Digital_Twin
    return None

def Laufzeitumgebung():
    ''' Hauptprogramm, übernimmt die Zuteilung und Auswertung von Nachrichten'''
    print("ich bin die Laufzeitumgebung")


    '''MQTT Broker instanziieren und Threads starten'''
    Broker_1 = MQTT(_username1, _passwd1, _host1, _port1, _topic_sub1)
    Broker_2 = MQTT(_username2, _passwd2, _host2, _port2, _topic_sub2)
    Broker_1.run()
    Broker_2.run()

    while True:

        if Broker_1.Q.empty() == False:
            TopicUndNachricht = Broker_1.Q.get()
            TopicUndNachricht = json.loads(TopicUndNachricht)
            Nachricht_auswerten(TopicUndNachricht)



        # Nachricht2 = Broker_2.Q.get()
        # print(Nachricht2)

        time.sleep(2)
    #mqtt_connection()



if __name__ == '__main__':
    Laufzeitumgebung()
