import json
import threading
import time
from Class_DT import Digital_Twin, Asset_Digital_Twin, Product_Demand_Digital_Twin
from MQTT import MQTT
import uvicorn
from fastapi import FastAPI, Query
from Class_Server import Server
from Class_Influxdb import Influxdb
from Class_Ontologie import Ontologie
import os.path
import os



'''Variablen für MQTT-Broker 1'''
_username1 = "Framework_Broker1"
_passwd1 = ""
_host1 = "host.docker.internal" #zum Container Erstellen
#_host1 = "127.0.0.1" # Betrieb über die IDE
_port1 = 1883
_timeout1 = 60
_topic_sub1 = "Laufzeitumgebung/#"

'''Variablen für MQTT-Broker 2'''
_username2 = "Framework_Broker2"
_passwd2 = ""
_host2 = "host.docker.internal" #zum Container Erstellen
#_host2 = "127.0.0.1" # Betrieb über die IDE
_port2 = 1884
_timeout2 = 60
_topic_sub2 = "Laufzeitumgebung/#"

'''Variablen für beide Broker'''
Event = threading.Event()

'''Variablen für Influxdb'''
url = "host.docker.internal:" + "8086" #zum Container Erstellen
#url = "127.0.0.1:" + "8086" #Betrieb über die IDE
token = "uO8aNM5-r4unhLY-bfu7q21_lbo4epMzGZjDY_EGo-a5A5taErG9nQA7jxovh2cSh4_NUyixSVJiM-jDEAPfWQ==" #Docker Compose
#token = "-DnCnjPN_w0JbBzX6cPLMqdoSyJsne31lj4985R88bRj1pCp_Bi_434T5dwHgq1klKGLumx2joHU65P3l1M0cQ==" #Betrieb über die IDE
org = "Laufzeitumgebung"

'''Weitere Variablen'''
ListeDTs = []
startZeit = time.time()

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
    '''Liste der möglichen DTs erstellen'''
    Hersteller_Listen = {}
    Select = """SELECT ?ProductionResource"""
    for item in Nachricht["Bedarf"]:
        Schritt = Nachricht["Bedarf"][item]
        if Schritt["ProductionService"] == "DrillingService":
            TypeOfMaterial = Schritt["TypeOfMaterial"]
            DiameterHoleResource = Schritt["Dimensionen"]["DiameterHoleResource"]
            Depth = Schritt["Dimensionen"]["Depth"]
            Thickness = Schritt["Dimensionen"]["Thickness"]
            Where = """WHERE {
                       ?ProductionResource DMP:offersProductionService ?Service .
                       ?ProductionResource DMP:processToM ?TypeOfMaterial .
                       ?ProductionResource DMP:minDiameterHoleResource ?minDiameterHoleResource .
                       ?ProductionResource DMP:maxDiameterHoleResource ?maxDiameterHoleResource .
                       ?ProductionResource DMP:minDepth ?minDepth .
                       ?ProductionResource DMP:maxDepth ?maxDepth .
                       ?ProductionResource DMP:minThickness ?minThickness .
                       ?ProductionResource DMP:maxThickness ?maxThickness .
                       FILTER (?Service = DMP:DrillingService && ?TypeOfMaterial = DMP:""" + TypeOfMaterial + """ &&
                               ?minDiameterHoleResource <= """ + str(DiameterHoleResource) + """ &&
                               ?maxDiameterHoleResource >= """ + str(DiameterHoleResource) + """ &&
                               ?minDepth <= """ + str(Depth) + """ &&
                               ?maxDepth >= """ + str(Depth) + """ &&
                               ?minThickness <= """ + str(Thickness) + """ &&
                               ?maxThickness >= """ + str(Thickness) + """)
                       }"""

        elif Schritt["ProductionService"] == "MillingService":
            TypeOfMaterial = Schritt["TypeOfMaterial"]
            Lenght = Schritt["Dimensionen"]["LengthResource"]
            Width = Schritt["Dimensionen"]["WidthResource"]
            Depth = Schritt["Dimensionen"]["Depth"]
            Thickness = Schritt["Dimensionen"]["Thickness"]
            Where = """WHERE {
                       ?ProductionResource DMP:offersProductionService ?Service .
                       ?ProductionResource DMP:processToM ?TypeOfMaterial .
                       ?ProductionResource DMP:minLengthResource ?minLengthResource .
                       ?ProductionResource DMP:maxLengthResource ?maxLengthResource .
                       ?ProductionResource DMP:minLengthResource ?minWidthResource .
                       ?ProductionResource DMP:maxWidthResource ?maxWidthResource .
                       ?ProductionResource DMP:minDepth ?minDepth .
                       ?ProductionResource DMP:maxDepth ?maxDepth .
                       ?ProductionResource DMP:minThickness ?minThickness .
                       ?ProductionResource DMP:maxThickness ?maxThickness .
                       FILTER (?Service = DMP:MillingService && ?TypeOfMaterial = DMP:""" + TypeOfMaterial + """ &&
                               ?minLengthResource <= """ + str(Lenght) + """ &&
                               ?maxLengthResource >= """ + str(Lenght) + """ &&
                               ?minWidthResource <= """ + str(Width) + """ &&
                               ?maxWidthResource >= """ + str(Width) + """ &&
                               ?minDepth <= """ + str(Depth) + """ &&
                               ?maxDepth >= """ + str(Depth) + """ &&
                               ?minThickness <= """ + str(Thickness) + """ &&
                               ?maxThickness >= """ + str(Thickness) + """)
                       }"""

        elif Schritt["ProductionService"] == "StampingService":
            TypeOfMaterial = Schritt["TypeOfMaterial"]
            Lenght = Schritt["Dimensionen"]["LengthResource"]
            Width = Schritt["Dimensionen"]["WidthResource"]
            Depth = Schritt["Dimensionen"]["Depth"]
            Thickness = Schritt["Dimensionen"]["Thickness"]
            Where = """WHERE {
                       ?ProductionResource DMP:offersProductionService ?Service .
                       ?ProductionResource DMP:processToM ?TypeOfMaterial .
                       ?ProductionResource DMP:minLengthResource ?minLengthResource .
                       ?ProductionResource DMP:maxLengthResource ?maxLengthResource .
                       ?ProductionResource DMP:minLengthResource ?minWidthResource .
                       ?ProductionResource DMP:maxWidthResource ?maxWidthResource .
                       ?ProductionResource DMP:minDepth ?minDepth .
                       ?ProductionResource DMP:maxDepth ?maxDepth .
                       ?ProductionResource DMP:minThickness ?minThickness .
                       ?ProductionResource DMP:maxThickness ?maxThickness .
                       FILTER (?Service = DMP:StampingService && ?TypeOfMaterial = DMP:""" + TypeOfMaterial + """ &&
                               ?minLengthResource <= """ + str(Lenght) + """ &&
                               ?maxLengthResource >= """ + str(Lenght) + """ &&
                               ?minWidthResource <= """ + str(Width) + """ &&
                               ?maxWidthResource >= """ + str(Width) + """ &&
                               ?minDepth <= """ + str(Depth) + """ &&
                               ?maxDepth >= """ + str(Depth) + """ &&
                               ?minThickness <= """ + str(Thickness) + """ &&
                               ?maxThickness >= """ + str(Thickness) + """)
                       }"""

        elif Schritt["ProductionService"] == "WeldingService":
            TypeOfMaterial = Schritt["TypeOfMaterial"]
            Lenght = Schritt["Dimensionen"]["LengthResource"]
            Thickness = Schritt["Dimensionen"]["Thickness"]
            Where = """WHERE {
                           ?ProductionResource DMP:offersProductionService ?Service .
                           ?ProductionResource DMP:processToM ?TypeOfMaterial .
                           ?ProductionResource DMP:minLengthResource ?minLengthResource .
                           ?ProductionResource DMP:maxLengthResource ?maxLengthResource .
                           ?ProductionResource DMP:minThickness ?minThickness .
                           ?ProductionResource DMP:maxThickness ?maxThickness .
                           FILTER (?Service = DMP:WeldingService && ?TypeOfMaterial = DMP:""" + TypeOfMaterial + """ &&
                                   ?minLengthResource <= """ + str(Lenght) + """ &&
                                   ?maxLengthResource >= """ + str(Lenght) + """ &&
                                   ?minThickness <= """ + str(Thickness) + """ &&
                                   ?maxThickness >= """ + str(Thickness) + """)}"""


        ListeHersteller = Ontologie_Client.Abfrage(Select, Where)
        Hersteller = []
        for DT in ListeHersteller:
            Twin = getTwin(DT)
            if DT != None:
                Hersteller.append(Twin)

        Hersteller_Listen[item] = Hersteller

    Anfrager = getTwin(Nachricht["Name"])
    if Anfrager is not None:
        Anfrager.Q.put(Hersteller_Listen)


def DT_nach_Typ_erstellen(Nachricht):
    '''Prüft die eingehende Nachricht auf den Typ des DTs und instanziiert davon abhänig einen ADT, PDDT oder DT aus der Klasse DT'''
    if Nachricht["Typ"] == "ADT":
        print("Ich stelle DT mit dem Namen " + Nachricht["Name"] + " bereit!")
        Neuer_ADT = Asset_Digital_Twin(Nachricht["Name"], Nachricht["Typ"], Nachricht["Sensoren"],
                                       Broker_1, Broker_2, DB_Client, Nachricht["Kritische Werte"],
                                       Nachricht["Operatoren"], Nachricht["Handlungen"], Nachricht["Skill"],
                                       Nachricht["Preise"], Nachricht["Zeiten"], Nachricht["Fehlerquote"],
                                       Ontologie_Client)
        ListeDTs.append(Neuer_ADT)
        print(Neuer_ADT.Name + " vom Typ " + Neuer_ADT.Typ + " Aus der Laufzeitumgebung gesendet")
        DT_Thread = threading.Thread(name=Neuer_ADT.Name, target=Neuer_ADT.ADT_Ablauf)
        DT_Thread.start()
        Pfad = "DT Files/" + Nachricht["Name"] + ".json"

        if os.path.isfile(Pfad) == False:
            with open(Pfad, "w", encoding='utf8') as outfile:
                json.dump(Nachricht, outfile, indent=4, ensure_ascii=False)

        print(DT_Thread.name + " name of thread")

    elif Nachricht["Typ"] == "PDDT":
        print("Ich stelle DT mit dem Namen " + Nachricht["Name"] + " bereit!")
        Neuer_PDDT = Product_Demand_Digital_Twin(Nachricht["Name"], Nachricht["Typ"], Broker_1, Broker_2,
                                                 Nachricht["Bedarf"])
        ListeDTs.append(Neuer_PDDT)
        print(Neuer_PDDT.Name + " vom Typ " + Neuer_PDDT.Typ + " Aus der Laufzeitumgebung gesendet")
        DT_Thread = threading.Thread(name=Neuer_PDDT.Name, target=Neuer_PDDT.PDDT_Ablauf)
        DT_Thread.start()

        Pfad = "DT Files/" + Nachricht["Name"] + ".json"
        if os.path.isfile(Pfad) == False:
            with open(Pfad, "w", encoding='utf8') as outfile:
                json.dump(Nachricht, outfile, indent=4, ensure_ascii=False)

        print(DT_Thread.name + " name of thread")

    elif Nachricht["Typ"] == "DT":
        print("Ich stelle DT mit dem Namen " + Nachricht["Name"] + " bereit!")
        Neuer_DT = Digital_Twin(Nachricht["Name"], Nachricht["Typ"], Broker_1, Broker_2)
        ListeDTs.append(Neuer_DT)
        print(Neuer_DT.Name + " vom Typ " + Neuer_DT.Typ + " Aus der Laufzeitumgebung gesendet")
        DT_Thread = threading.Thread(name=Neuer_DT.Name, target=Neuer_DT.DT_Ablauf)
        DT_Thread.start()

        Pfad = "DT Files/" + Nachricht["Name"] + ".json"
        if os.path.isfile(Pfad) == False:
            with open(Pfad, "w", encoding='utf8') as outfile:
                json.dump(Nachricht, outfile, indent=4, ensure_ascii=False)

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

'''Locks für Ontologie erzeugen und Verbindung zum Server instanziieren'''
Ontologie_Client = Ontologie()


'''App für Get-Request instanziieren'''
App = FastAPI()

'''API für den Zugriff auf die Laufzeitumgebung. Zugreifen über http://127.0.0.1:7000/docs#/'''
'''Gibt Anzahl der aktiven DTs zurück'''
@App.get("/get-twin-number/")
async def Anzahl_Twins():
    AnzahlTwins = len(ListeDTs)
    return json.loads(json.dumps({"Anzahl Twins": AnzahlTwins}))

'''Gibt den letzten Messwert des angegebenen DTs und Sensors zurück. Wird der Name des Sensors auf all gestellt,
werden die letzten Werte aller Sensoren des DTs als Liste zurückgegeben'''
@App.get("/get/{Name}/{Sensor}")
async def Sensorwerte_Twin(Name, Sensor):
    return DB_Client.Query(Name, Sensor)


'''Gibt den angegebenen DTs oder die ausgewählten Inhalte zurück. Attribute sind optional Query-Parameter.
In Url: http://127.0.0.1:7000/{Name}?Attribut1=Attribut&Attribut2=Attribut...'''
@App.get("/{Name}")
async def Twins(Name, Attribute: list[str] = Query(None)):
    Twin = getTwin(Name)

    '''Error Handling, fall der gesuchte Twin noch nicht instanziiert wurde.'''
    if Twin == None:
        return "Gesuchter Twin nicht vorhanden"

    else:
        if Attribute == None:
            Twin = Twin.Ich_bin()
            return Twin

        else:
            Twin = Twin.Ich_bin()
            for item in Attribute:
                Twin = Twin[item]
            return Twin

'''Erstellt einen DT vom Typ PDDT Test URL: http://127.0.0.1:7000/PDDT/Test/%7B%22Schritt%201%22%3A%20%7B%22Production
Service%22%3A%20%22DrillingService%22%2C%20%22TypeOfMaterial%22%3A%20%22Metal%22%2C%20%22Geometrie%22%3A%20%22Kreis%22
%2C%20%22Dimensionen%22%3A%20%7B%22DiameterHoleResource%22%3A%2015.0%2C%20%22Depth%22%3A%2030.0%2C%20%22Thickness%22%3
A%2055.0%7D%7D%7D'''
@App.put("/PDDT/{Name}/{Bedarf}")
async def PDDT_Erstellen(Name, Bedarf):
    if Name in ListeDTs:
        return "DT mit diesem Namen existiert bereits. Bitte einen anderen Namen wählen."

    Bedarf = json.loads(Bedarf)
    Nachricht = json.dumps({"Name": Name, "Typ": "PDDT", "Task": "Erstelle DT"})
    Nachricht = json.loads(Nachricht)
    Nachricht["Bedarf"] = Bedarf
    DT_nach_Typ_erstellen(Nachricht)
    return "PDDT wurde erstellt"

'''Stoppt die Instanz des angegebenen Broker, ändert den Broker und startet die Instanz neu'''
@App.put("/change/{Broker}/{Host}/{Port}")
async def change_Broker(Broker, Host, Port,Username="", Passwort=""):
    if Broker == "Broker_1":
        Broker_1.publish("Laufzeitumgebung/Broker_Change", json.dumps({"Broker": Broker, "Username": Username,
        "Passwort": Passwort, "Host": Host, "Port": Port}), Qos=2)
        Broker_1.client.loop_stop()
        Broker_1._username = Username
        Broker_1._passwd = Passwort
        Broker_1._host = Host
        Broker_1._port = int(Port)
        Broker_1.run()
        return "Broker wurde geändert"

    elif Broker == "Broker_2":
        Broker_2.client.loop_stop()
        Broker_2._username = Username
        Broker_2._passwd = Passwort
        Broker_2._host = Host
        Broker_2._port = int(Port)
        Broker_2._topic_Sub = Topic
        Broker_2.run()
        return "Broker wurde geändert"
    else:
        return "Angegebener Broker existiert nicht"

'''Ändert die Datenbank Test URL:http://127.0.0.1:7000/change/DB/host.docker.internal%3A9999/oaDobTgt6NufUHzJYmvI67U6oW
neMdUP2bW1jjtl6bwZBSMAGekZUyETix5XGe0YCI-rufhSGrNSBWb-G7JG_w%3D%3D/Laufzeitumgebung'''
@App.put("/change/DB/{URL}/{Token}/{Org}")
async def change_DB(URL, Token, Org):
    DB_Client.url = URL
    DB_Client.token = Token
    DB_Client.org = Org

    '''Error Handling, Falls die Datenbank geändert wird und noch kein Bucket angelegt wurde'''
    for Twin in ListeDTs:
        if Twin.Typ == "ADT":
            DB_Client.New_Bucket(Twin.Name)
            print("Neues Bucket für " + Twin.Name + " in der neuen DB angelegt")

    return "Datenbank wurde geändert"

'''Beendet die Ausführung eines DTs und entfernt sein json file, um einen Neustart zu verhindern'''
@App.delete("/kill/{Name}")
async def kill(Name):
    threadtokill = getTwin(Name)
    if threadtokill is not None:
        os.remove("DT Files/" + Name + ".json")
        ListeDTs.remove(threadtokill)
        threadtokill.Q.put("Kill")
        if threadtokill.Typ == "ADT":
            Ontologie_Client.Löschen(Name)
        print(str(len(ListeDTs)) + " DTs laufen")
        return "Digital Twin wurde gelöscht"

    else:
        return "Digital Twin existiert nicht"

'''Server für API instanziieren
https://stackoverflow.com/questions/61577643/python-how-to-use-fastapi-and-uvicorn-run-without-blocking-the-thread
host="0.0.0.0" für globales hosten https://www.uvicorn.org/settings/#socket-binding
https://stackoverflow.com/questions/62898917/running-fastapi-app-using-uvicorn-on-ubuntu-server'''
config = uvicorn.Config(App, host="0.0.0.0", port=7000, log_level="info")
server = Server(config=config)


with server.run_in_thread():
    # Server is started.
    '''Anzahl Twins muss einmal vor der Schleife definiert werden um jeder Zeit über die API zugreifen zu können.'''
    AnzahlTwins = len(ListeDTs)



    '''https://stackoverflow.com/questions/30539679/python-read-several-json-files-from-a-folder
    Läd alle json.files aus dem Ordner DT Files und startet diese DTs. Wartet bis beide Broker verbunden sind,
    dass bei einem Neustart die Laufzeitumgebung die Nachrichten mit den Bedarfen erhält'''
    while True:
        if Broker_1.client.is_connected() == True:
            if Broker_2.client.is_connected() == True:
                for file_name in [file for file in os.listdir("DT Files/")]:
                    with open("DT Files/" + file_name, "r") as json_file:
                        data = json.load(json_file)
                        DT_nach_Typ_erstellen(data)
                break
        else:
            pass
    print(str(len(ListeDTs)) + " DTs laufen")

    while True:
        '''Laufzeitumgebung wartet bis sich ein Objekt in der Queue des Broker 1 oder 2 befindet.
        Dann wird das Event wieder auf False gestellt und die Laufzeitumgebung wartet
        nach dem Durchlaufen der Schleife wieder.'''
        Event.wait()
        Event.clear()

        '''Gibt alle 5 Seconden die Anzahl der in der Lafuzeitumgebung aktiven DTs aus. Dadurch wird die Ausgabe nicht
        mit Nachrichten überflutet. https://stackoverflow.com/questions/70544320/how-to-print-every-x-seconds-while-rest
        -of-code-runs-without-being-stopped'''
        aktuelleZeit = time.time()
        AnzahlTwins = len(ListeDTs)
        if aktuelleZeit - startZeit >= 5:
            print(str(len(ListeDTs)) + " DTs laufen")
            startZeit = aktuelleZeit

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




