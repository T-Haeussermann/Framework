import json
import threading
from Class_DT import Digital_Twin, Asset_Digital_Twin, Product_Demand_Digital_Twin
from MQTT import MQTT
import uvicorn
from fastapi import FastAPI
from Class_Server import Server
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
_host2 = "192.168.178.70"
_port2 = 1884
_timeout2 = 60
_topic_sub2 = "Laufzeitumgebung/#"

'''Variablen für beide Broker'''
Event = threading.Event()

'''Variablen für Influxdb'''
url = "192.168.178.70" + ":8086"
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

    if "/Messwerte" in Topic:
        Name = Nachricht["Name"]
        Empfaenger = getTwin(Name)
        if Empfaenger is not None:
            Empfaenger.Q.put(Nachricht)

def Nachricht_auswerten_Broker_2(Topic, Nachricht):
    '''Wertet die eingehende Nachricht auf dem Broker 2 anhand des Topics aus
    und leitet Anfragen auf dem Ontologie-Server ein'''
    if "/Bedarf" in Topic:
        Abfrage_Ontologie_Server(Topic, Nachricht)

    if "/Herstellen" in Topic:
        Name = Nachricht["Hersteller"]
        Empfaenger = getTwin(Name)
        if Empfaenger is not None:
            Empfaenger.Q.put(Nachricht)



def Abfrage_Ontologie_Server(Topic, Nachricht):
    '''Führt eine Abfrage auf dem Ontologie-Server durch und gibt die DTs zurück, weleche diese bearbeiten können.'''
    print("Ich habe einen Bedarf erkannt und frage den Ontologie-Server wer das machen kann!")
    '''Liste der möglichen DTs erstellen mit den Werten, die bewertet werden'''
    ListeHersteller = ["Tester_ADT", "Tester_ADT1", "Tester_ADT2"]
    Hersteller = []
    for Twin in ListeHersteller:
        DT = getTwin(Twin)
        if DT is not None:
            Hersteller.append(DT)

    Anfrager = getTwin(Nachricht["Name"])
    if Anfrager is not None:
        Anfrager.Q.put(Hersteller)


def DT_nach_Typ_erstellen(Nachricht):
    '''Prüft die eingehende Nachricht auf den Typ des DTs und instanziiert davon abhänig einen ADT, PDDT oder DT aus der Klasse DT'''
    if Nachricht["Typ"] == "ADT":
        print("Ich stelle DT mit dem Namen " + Nachricht["Name"] + " bereit!")
        Neuer_ADT = Asset_Digital_Twin(Nachricht["Name"], Nachricht["Typ"], Nachricht["Sensoren"],
                                       Broker_1, Broker_2, DB_Client, Nachricht["Kritische Werte"],
                                       Nachricht["Operatoren"], Nachricht["Handlungen"], Nachricht["Skill"],
                                       Nachricht["Preise"], Nachricht["Zeiten"], Nachricht["Fehlerquote"])
        ListeDTs.append(Neuer_ADT)
        print(Neuer_ADT.Name + " vom Typ " + Neuer_ADT.Typ + " Aus der Laufzeitumgebung gesendet")
        DT_Thread = threading.Thread(name=Neuer_ADT.Name, target=Neuer_ADT.ADT_Ablauf)
        DT_Thread.start()
        print(DT_Thread.name + " name of thread")

    elif Nachricht["Typ"] == "PDDT":
        print("Ich stelle DT mit dem Namen " + Nachricht["Name"] + " bereit!")
        Neuer_PDDT = Product_Demand_Digital_Twin(Nachricht["Name"], Nachricht["Typ"], Broker_1, Broker_2,
                                                 Nachricht["Bedarf"])
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
print("Hallo ich bin die Laufzeitumgebung :)")

'''MQTT Broker instanziieren und Threads starten'''
Broker_1 = MQTT(_username1, _passwd1, _host1, _port1, _topic_sub1, Event)
Broker_2 = MQTT(_username2, _passwd2, _host2, _port2, _topic_sub2, Event)
Broker_1.run()
Broker_2.run()

'''Lock für DB erzeugen und Verbindung zur Datenbank instanziieren'''
Lock_DB_Client = threading.Lock()
DB_Client = Influxdb(url, token, org, Lock_DB_Client)


'''App für Get-Request instanziieren'''
App = FastAPI()

'''API für den Zugriff auf die Laufzeitumgebung. Zugreifen über http://127.0.0.1:7000/docs#/'''
'''Gibt Anzahl der aktiven DTs zurück'''
@App.get("/get-twin-number/")
async def Anzahl_Twins():
    return json.loads(json.dumps({"Anzahl Twins": AnzahlTwins}))

'''Gibt den letzten Messwert des angegebenen DTs und Sensors zurück. Wird der Name des Sensors auf all gestellt,
werden die letzten Werte aller Sensoren des DTs als Liste zurückgegeben'''
@App.get("/get/{Name}/{Sensor}")
async def Sensorwerte_Twin(Name, Sensor):
    return DB_Client.Query(Name, Sensor)


'''Gibt den angegebenen DTs oder die ausgewählten Inhalte zurück. Attribute sind optional Query-Parameter.
In Url: http://127.0.0.1:7000/{Name}?Attribut1=Attribut&Attribut2=Attribut...'''
@App.get("/{Name}")
async def Twins(Name, Attribut1=None, Attribut2 =None, Attribut3=None, Attribut4=None, Attribut5= None):
    Twin = getTwin(Name)
    '''Error Handling, fall der gesuchte Twin noch nicht instanziiert wurde.'''
    if Twin == None:
        return "Gesuchter Twin nicht vorhanden"
    else:
        if Attribut1 == None:
            Twin = Twin.Ich_bin()
            return Twin
        else:
            if Attribut1 == None:
                Twin = Twin.Ich_bin()
                return Twin
            elif Attribut1 != None:
                if Attribut2 == None:
                    Twin = Twin.Ich_bin()[Attribut1]
                    return Twin
                elif Attribut2 != None:
                    if Attribut3 == None:
                        Twin = Twin.Ich_bin()[Attribut1][Attribut2]
                        return Twin
                    elif Attribut3 != None:
                        if Attribut4 == None:
                            Twin = Twin.Ich_bin()[Attribut1][Attribut2][Attribut3]
                            return Twin
                        elif Attribut4 != None:
                            if Attribut5 == None:
                                Twin = Twin.Ich_bin()[Attribut1][Attribut2][Attribut3][Attribut4]
                                return Twin
                            elif Attribut5 != None:
                                Twin = Twin.Ich_bin()[Attribut1][Attribut2][Attribut3][Attribut4][Attribut5]
                                return Twin

'''Server für API instanziieren
https://stackoverflow.com/questions/61577643/python-how-to-use-fastapi-and-uvicorn-run-without-blocking-the-thread
host="0.0.0.0" für globales hosten https://www.uvicorn.org/settings/#socket-binding
https://stackoverflow.com/questions/62898917/running-fastapi-app-using-uvicorn-on-ubuntu-server'''
config = uvicorn.Config(App, host="127.0.0.1", port=7000, log_level="info")
server = Server(config=config)

with server.run_in_thread():
    # Server is started.
    '''Anzahl Twins muss einmal vor der Schleife definiert werden um jeder Zeit über die API zugreifen zu können.'''
    AnzahlTwins = len(ListeDTs)
    while True:
        Event.wait()
        Event.clear()
        '''Laufzeitumgebung wartet bis sich ein Objekt in der Queue des Broker 1 oder 2 befindet.
        Dann wird das Event wieder auf False gestellt und die Laufzeitumgebung wartet
        nach dem Durchlaufen der Schleife wieder.'''
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
                print(TopicUndNachricht[1])
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
                print(TopicUndNachricht[1])
                print("Kein json kompatibler String in Broker 2")



    # Server stopped.




