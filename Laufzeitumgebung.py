import json
import signal
import threading
from Class_DT import Digital_Twin, Asset_Digital_Twin, Product_Demand_Digital_Twin
from MQTT import MQTT
from queue import Queue
import uvicorn
from fastapi import FastAPI
from API.Class_Server import Server
from Class_Influxdb import Influxdb



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
_topic_sub2 = "Laufzeitumgebung/#"

'''Variablen für Influxdb'''
url = "http://localhost:8086"
token = "-DnCnjPN_w0JbBzX6cPLMqdoSyJsne31lj4985R88bRj1pCp_Bi_434T5dwHgq1klKGLumx2joHU65P3l1M0cQ=="
org = "Laufzeitumgebung"
bucket = "Messwerte"

'''Weitere Variablen'''
ListeDTs = []


def Nachricht_auswerten_Broker_1(Topic, Nachricht):
    '''Wertet die eingehende Nachricht auf dem Broker 1 anhand des Topics aus
    und leitet die DT-Erstellung oder Messwertzuordnung ein'''

    ListeThreads = []
    for thread in threading.enumerate():
        ListeThreads.append(thread.name)

    if "/Anforderung" in Topic:
            if Nachricht["Task"] == "Erstelle DT":
                if Nachricht["Name"] not in str(ListeThreads):
                    DT_nach_Typ_erstellen(Nachricht)

    elif "/Anforderung" in Topic:
        if Nachricht["Task"] == "Erstelle DT":
            if Nachricht["Name"] in str(ListeThreads):
                print("Ich lege keinen neuen DT an")

    if "/Messwert" in Topic:
        Name = Nachricht["Name"]
        Empfaenger = getTwin(Name)
        if Empfaenger is not None:
            Empfaenger.Q.put(Nachricht)

def Nachricht_auswerten_Broker_2(Topic, Nachricht):
    '''Wertet die eingehende Nachricht auf dem Broker 2 anhand des Topics aus
    und leitet Anfragen auf dem Ontologie-Server ein'''
    if "/Bedarf" in Topic:
        print("Ich habe einen Bedarf erkannt und frage den Ontologie-Server wer das machen kann!")
        print("Das ist der Bedarf: " + str(Nachricht))
    else:
        print("Ich habe keinen Bedarf erkannt")



def DT_nach_Typ_erstellen(Nachricht):
    '''Prüft die eingehende Nachricht auf den Typ des DTs und instanziiert davon abhänig einen ADT, PDDT oder DT aus der Klasse DT'''
    if Nachricht["Typ"] == "ADT":
        print("Ich stelle DT mit dem Namen " + Nachricht["Name"] + " bereit!")
        Neuer_ADT = Asset_Digital_Twin(Nachricht["Name"], Nachricht["Typ"], Broker_1, Broker_2, DB_Client,
                                       Nachricht["Kritischer Wert"], Nachricht["Operator"], Nachricht["Handlung"],
                                       json.loads(Nachricht["Fähigkeit"]))
        ListeDTs.append(Neuer_ADT)
        print(Neuer_ADT.Name + " vom Typ " + Neuer_ADT.Typ + " Aus der Laufzeitumgebung gesendet")
        DT_Thread = threading.Thread(name=Neuer_ADT.Name, target=Neuer_ADT.ADT_Ablauf)
        DT_Thread.start()
        print(DT_Thread.name + " name of thread")

    elif Nachricht["Typ"] == "PDDT":
        print("Ich stelle DT mit dem Namen " + Nachricht["Name"] + " bereit!")
        Neuer_PDDT = Product_Demand_Digital_Twin(Nachricht["Name"], Nachricht["Typ"], Broker_1, Broker_2,
                                                 json.loads(Nachricht["Bedarf"]))
        ListeDTs.append(Neuer_PDDT)
        print(Neuer_PDDT.Name + " vom Typ " + Neuer_PDDT.Typ + " Aus der Laufzeitumgebung gesendet")
        DT_Thread = threading.Thread(name=Neuer_PDDT.Name, target=Neuer_PDDT.PDDT_Ablauf)
        DT_Thread.start()
        print(DT_Thread.name + " name of thread")

    elif Nachricht["Typ"] == "DT":
        print("Ich stelle DT mit dem Namen " + Nachricht["Name"] + " bereit!")
        Neuer_DT = Digital_Twin(Nachricht["Name"], Nachricht["Typ"], Broker_1, Broker_2)
        ListeDTs.append(Neuer_DT)
        print(Neuer_DT.Name + " vom Typ " + Neuer_DT.Typ + " Aus der Laufzeitumgebung gesendet")
        DT_Thread = threading.Thread(name=Neuer_DT.Name, target=Neuer_DT.DT_Ablauf)
        DT_Thread.start()
        print(DT_Thread.name + " name of thread")


def getTwin(Name):
    '''Sucht den eingehenden Namen in der Liste der DTs und gibt den Empfänger zurück'''
    for Digital_Twin in ListeDTs:
        if Digital_Twin.Name == Name:
            return Digital_Twin
    return None


''' Hauptprogramm, übernimmt die Zuteilung von Nachrichten und Auswertung des Nachrichtentyps'''
print("ich bin die Laufzeitumgebung")

'''MQTT Broker instanziieren und Threads starten'''
Broker_1 = MQTT(_username1, _passwd1, _host1, _port1, _topic_sub1)
Broker_2 = MQTT(_username2, _passwd2, _host2, _port2, _topic_sub2)
Broker_1.run()
Broker_2.run()

'''Lock für DB erzeugen und Verbindung zur Datenbank instanziieren'''
Lock_DB_Client = threading.Lock()
DB_Client = Influxdb(url, token, org, bucket, Lock_DB_Client)


'''App für Get-Request instanziieren'''
App = FastAPI()

'''API für den Zugriff auf die Laufzeitumgebung. Zugreifen über http://127.0.0.1:8000/docs#/'''
@App.get("/get-twin-names-api/")
async def Anzahl_Twins():
   return json.dumps({"Anzahl Twins": AnzahlTwins})

'''Server für API instanziieren
https://stackoverflow.com/questions/61577643/python-how-to-use-fastapi-and-uvicorn-run-without-blocking-the-thread'''
config = uvicorn.Config(App, host="127.0.0.1", port=8800, log_level="info")
server = Server(config=config)

with server.run_in_thread():
    # Server is started.
    while True:
        if Broker_1.Q.empty() == False or Broker_2.Q.empty() == False:
            '''Laufzeitumgebung wartet bis sich ein Objekt in der Queue des Broker 1 oder 2 befindet'''
            AnzahlTwins = len(ListeDTs)
            print(str(len(ListeDTs)) + " DTs laufen")

            if Broker_1.Q.empty() == False:
                '''Nachrichten von Broker 1 verarbeiten.
                Funktion blockt nicht und wird nur aufgerufen wenn etwas in der Queue ist'''
                TopicUndNachricht = Broker_1.Q.get()
                Topic = TopicUndNachricht[0]

                '''Wird benötigt um die Funktionsfähigkeit der Laufumgebung sicherzustellen, falls keine
                json kompatiblen Nachrichten versendet werden'''
                try:
                    Nachricht = json.loads(TopicUndNachricht[1])
                    Nachricht_auswerten_Broker_1(Topic, Nachricht)
                except:
                    print("Kein json kompatibler String in Broker 1")


            if Broker_2.Q.empty() == False:
                '''Nachrichten von Broker 2 verarbeiten'''
                TopicUndNachricht = Broker_2.Q.get()
                Topic = TopicUndNachricht[0]

                '''Wird benötigt um die Funktionsfähigkeit der Laufumgebung sicherzustellen, falls keine
                json kompatiblen Nachrichten versendet werden'''
                try:
                    Nachricht = json.loads(TopicUndNachricht[1])
                    Nachricht_auswerten_Broker_2(Topic, Nachricht)
                except:
                    print(TopicUndNachricht)
                    print("Kein json kompatibler String in Broker 2")

    # Server stopped.




