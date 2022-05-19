import time
from queue import Queue
import json
from influxdb_client import Point

'''Achtung nur Json Versenden sonst kommt es zu Fehlern in der Laufumgebung'''

class Digital_Twin:
    """Klasse normaler Twin ohne Fähigkeit Digital Twin"""
    def __init__(self, Name, Typ, Broker_1, Broker_2):
        self.Name = Name
        self.Typ = Typ
        self.Q = Queue()
        self.Broker_1 = Broker_1
        self.Broker_2 = Broker_2
        self.Topic = "Laufzeitumgebung/" + self.Name

    def Ich_bin(self):
        Ich_bin = json.dumps({"Name": self.Name, "Typ": self.Typ})
        Ich_bin = json.loads(Ich_bin)
        return Ich_bin

    def DT_Ablauf(self):
        while True:
            Nachricht = self.Q.get()
            print(Nachricht)

            '''Stoppt den Thread wenn der Befehl Kill kommt'''
            if Nachricht == "Kill":
                break


class Asset_Digital_Twin(Digital_Twin):
    def __init__(self, Name, Typ, Sensoren, Broker_1, Broker_2, DB_Client, KritWerte, Operatoren, Handlungen, Fähigkeit,
                 Preise, Zeiten, Fehlerquote, Ontologie_Client):
        super().__init__(Name, Typ, Broker_1, Broker_2)
        self.Sensoren = Sensoren
        self.DB_Client = DB_Client
        self.KritWerte = KritWerte
        self.Operatoren = Operatoren
        self.Handlungen = Handlungen
        self.Fähigkeit = Fähigkeit
        self.Preise = Preise
        self.Zeiten = Zeiten
        self.Fehlerquote = Fehlerquote
        self.Ontologie_Client = Ontologie_Client
        self.Topic = "Laufzeitumgebung/" + self.Name

    def Ich_bin(self):
        Sensorwerte = {}
        for Sensor in self.Sensoren:

            WertUndEinheit = {
                "Wert": self.DB_Client.Query(self.Name, Sensor)["Messwert"],
                "Einheit": self.DB_Client.Query(self.Name, Sensor)["Einheit"],
                "Kritischer Wert": self.KritWerte[Sensor],
                "Operator": self.Operatoren[Sensor],
                "Handlung": self.Handlungen[Sensor]
            }
            Sensorwerte[Sensor] = WertUndEinheit
        '''Sensorwerte, Kritische Werte, Operatoren und Handlungen getrennt'''
        # Ich_bin = json.dumps({"Name": self.Name, "Typ": self.Typ, "Fähigkeit": self.Fähigkeit, "Sensoren": Sensorwerte,
        #                       "Kritische Werte": self.KritWerte, "Operatoren": self.Operatoren,
        #                       "Handlungen": self.Handlungen})
        '''Sensorwerte, Kritische Werte, Operatoren und Handlungen zusammen'''
        Ich_bin = json.dumps({"Name": self.Name, "Typ": self.Typ, "Fähigkeit": self.Fähigkeit, "Sensoren": Sensorwerte,
                              "Preise": self.Preise, "Zeiten": self.Zeiten, "Fehlerquote": self.Fehlerquote})
        Ich_bin = json.loads(Ich_bin)
        return Ich_bin

    def ADT_Ablauf(self):
        '''Bucket in der Datenbank mit dem Namen des ADT anlegen'''
        self.DB_Client.New_Bucket(self.Name)

        '''ADT auf dem Ontologie-Server anlegen'''
        Ich_bin = self.Ich_bin()
        offersProductionService = Ich_bin["Fähigkeit"]["offersProductionService"]
        processToM = Ich_bin["Fähigkeit"]["processToM"]
        Fehlerquote = Ich_bin["Fehlerquote"]

        Dimensionen = ""
        for item in Ich_bin["Fähigkeit"]["Dimensionen"]:
            Dimensionen = Dimensionen +\
                          "DMP:" +self.Name + " DMP:" + item + " " + "\"" +\
                          str(Ich_bin["Fähigkeit"]["Dimensionen"][item]) + "\"^^xsd:decimal .\n"

        Preise = ""
        for item in Ich_bin["Preise"]:
            if type(Ich_bin["Preise"][item]) != str:
                Preise = Preise + \
                              "DMP:" + self.Name + " DMP:" + item + " " + "\"" + \
                              str(Ich_bin["Preise"][item]) + "\"^^xsd:decimal .\n"
            else:
                Preise = Preise + \
                         "DMP:" + self.Name + " DMP:" + item + " " + "\"" + \
                         str(Ich_bin["Preise"][item]) + "\"^^xsd:string .\n"

        Zeiten = ""
        for item in Ich_bin["Zeiten"]:
            if type(Ich_bin["Zeiten"][item]) is not str:
                Zeiten = Zeiten + \
                         "DMP:" + self.Name + " DMP:" + item + " " + "\"" + \
                         str(Ich_bin["Zeiten"][item]) + "\"^^xsd:decimal .\n"
            else:
                Zeiten = Zeiten + \
                         "DMP:" + self.Name + " DMP:" + item + " " + "\"" + \
                         str(Ich_bin["Zeiten"][item]) + "\"^^xsd:string .\n"

        if self.Ontologie_Client.Existiert(self.Name, offersProductionService, processToM)["boolean"] == False:
            Insert = """INSERT DATA {
                DMP:""" + self.Name + """ rdf:type owl:NamedIndividual ,
                DMP:Resource .
                DMP:""" + self.Name + """ DMP:offersProductionService DMP:""" + offersProductionService + """ .\n
                DMP:""" + self.Name + """ DMP:processToM DMP:""" + processToM + """ .\n""" + Dimensionen +\
                Preise + Zeiten + """
                DMP:""" + self.Name + """ DMP:Fehlerquote DMP:""" + str(Fehlerquote) + """
            }"""
            self.Ontologie_Client.Anlegen(Insert)

        while True:
            '''Warten bis sich eine Nachricht in der Queue befindet.
                            Prüfen ob es sich um Messwerte oder Fertigungsauftrag handelt
                            Datenpunkt erstellen und in der Datenbank ablegen'''
            Nachricht = self.Q.get()
            if "Messwert" in Nachricht:
                Sensorname = list(Nachricht["Messwert"].keys())[0]
                Sensoreinheit = Nachricht["Messwert"]["Einheit"]
                Sensorwert = Nachricht["Messwert"][Sensorname]
                Messpunkt = Point("Messwerte").tag("Sensor", Sensorname).field(Sensoreinheit, Sensorwert)
                self.DB_Client.Schreiben(self.Name, Messpunkt)

                '''Status prüfen und ggf. Handlung publishen. Error Handling, da zu Beginn noch nicht für alle Sensoren
                Messwerte in der Datenbank vorliegen.'''
                try:
                    Status = self.Ich_bin()
                    for Sensor in Status["Sensoren"]:
                        if Status["Sensoren"][Sensor]["Operator"] == ">":
                            if Status["Sensoren"][Sensor]["Wert"] > Status["Sensoren"][Sensor]["Kritischer Wert"]:
                                Payload = json.dumps(
                                    {"Name": self.Name, "Ausführen": Status["Sensoren"][Sensor]["Handlung"]})
                                self.Broker_1.publish(self.Topic + "/Handlungen/" + Sensor, Payload)
                        if Status["Sensoren"][Sensor]["Operator"] == "<":
                            if Status["Sensoren"][Sensor]["Wert"] < Status["Sensoren"][Sensor]["Kritischer Wert"]:
                                Payload = json.dumps(
                                    {"Name": self.Name, "Ausführen": Status["Sensoren"][Sensor]["Handlung"]})
                                self.Broker_1.publish(self.Topic + "/Handlungen/" + Sensor, Payload)
                except:
                    pass

            elif "Hersteller" in Nachricht:
                Payload = json.dumps({"Auftraggeber": Nachricht["Auftraggeber"], "Bedarf": Nachricht["Bedarf"],
                                      "Auftragseingang": time.asctime()})
                self.Broker_1.publish(self.Topic + "/Fertigung/" + Nachricht["Auftraggeber"], Payload, 2)

            elif Nachricht == "Kill":
                break





class Product_Demand_Digital_Twin(Digital_Twin):
    def __init__(self, Name, Typ, Broker_1, Broker_2, Bedarf):
        super().__init__(Name, Typ, Broker_1, Broker_2)
        self.Bedarf = Bedarf
        self.Topic = "Laufzeitumgebung/" + self.Name

    def Ich_bin(self):
        Ich_bin = json.dumps({"Name": self.Name, "Typ": self.Typ, "Bedarf": self.Bedarf})
        Ich_bin = json.loads(Ich_bin)
        return Ich_bin

    def PDDT_Ablauf(self):
        self.Broker_2.publish(self.Topic + "/Bedarf", json.dumps({"Name": self.Name, "Bedarf": self.Bedarf}))
        while True:
            Nachricht = self.Q.get()
            '''Ermittelt, wer der Beste ist'''
            Liste_Hersteller = {}
            if Nachricht != "Kill":
                for DT in Nachricht:
                    Twin = DT.Ich_bin()
                    TwinName = Twin["Name"]
                    '''Error Handling, falls Twin mit falschem Skill übergeben wird'''
                    try:
                        if self.Bedarf["Art"] == "Tasche":
                            if self.Bedarf ["Geometrie"] == "Kreis":
                                Liste = []
                                for ET in Twin["Preise"]:
                                    if ET == str(self.Bedarf["Dimensionen"]["Dimension X"]):
                                        Liste.append(Twin["Preise"][ET])

                                for ET in Twin["Zeiten"]:
                                    if ET == str(self.Bedarf["Dimensionen"]["Dimension X"]):
                                        Liste.append(Twin["Zeiten"][ET])

                                Liste.append(Twin["Fehlerquote"])
                                Liste_Hersteller[TwinName] = Liste

                            elif self.Bedarf ["Geometrie"] == "Rechteck":
                                for ET in Twin["Preise"]:
                                    print(ET)
                                    print(type(ET))
                                    if ET == str(self.Bedarf["Dimensionen"]["Dimension X"]) + "x" + \
                                            str(self.Bedarf["Dimensionen"]["Dimension Y"]):
                                        Liste.append(Twin["Preise"][ET])

                                for ET in Twin["Zeiten"]:
                                    if ET == str(self.Bedarf["Dimensionen"]["Dimension X"]) + "x" + \
                                            str(self.Bedarf["Dimensionen"]["Dimension Y"]):
                                        Liste.append(Twin["Zeiten"][ET])

                                Liste.append(Twin["Fehlerquote"])
                                Liste_Hersteller[TwinName] = Liste

                        elif self.Bedarf["Art"] == "Aufsatz":
                            if self.Bedarf["Geometrie"] == "Kreis":
                                Liste = []
                                for ET in Twin["Preise"]:
                                    if ET == str(self.Bedarf["Dimensionen"]["Dimension X"]):
                                        Liste.append(Twin["Preise"][ET])

                                for ET in Twin["Zeiten"]:
                                    if ET == str(self.Bedarf["Dimensionen"]["Dimension X"]):
                                        Liste.append(Twin["Zeiten"][ET])

                                Liste.append(Twin["Fehlerquote"])
                                Liste_Hersteller[TwinName] = Liste

                            elif self.Bedarf["Geometrie"] == "Rechteck":
                                for ET in Twin["Preise"]:
                                    if ET == str(self.Bedarf["Dimensionen"]["Dimension X"]) + "x" + \
                                            str(self.Bedarf["Dimensionen"]["Dimension Y"]):
                                        Liste.append(Twin["Preise"][ET])

                                for ET in Twin["Zeiten"]:
                                    if ET == str(self.Bedarf["Dimensionen"]["Dimension X"]) + "x" + \
                                            str(self.Bedarf["Dimensionen"]["Dimension Y"]):
                                        Liste.append(Twin["Zeiten"][ET])

                                Liste.append(Twin["Fehlerquote"])
                                Liste_Hersteller[TwinName] = Liste
                    except:
                        continue

                for DT in Liste_Hersteller:
                    Güte = Liste_Hersteller[DT][0] + Liste_Hersteller[DT][1] + 2 * Liste_Hersteller[DT][2]
                    Liste_Hersteller[DT] = Güte

                '''https://stackoverflow.com/questions/3282823/get-the-key-corresponding-to-the-minimum-value-within-a-dictionary'''
                MinWert = min(Liste_Hersteller.values())
                MinHersteller = [k for k, v in Liste_Hersteller.items() if v == MinWert]

                '''Wenn mehrere DTs den gleichen Wert haben, nimm den ersten'''
                Hersteller = MinHersteller[0]
                self.Broker_2.publish(self.Topic + "/Herstellen", json.dumps({"Auftraggeber": self.Name,
                                                                               "Hersteller": Hersteller,
                                                                               "Bedarf": self.Bedarf}))

            if Nachricht == "Kill":
                break