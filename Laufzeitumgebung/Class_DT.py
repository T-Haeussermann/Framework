import time
from queue import Queue
import json
from influxdb_client import Point
import math

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
            Abfrage = self.DB_Client.Query(self.Name, Sensor)
            '''Error Handling, falls noch keine Messwerte existieren'''
            if Abfrage != None:
                WertUndEinheit = {
                    "Wert": Abfrage["Messwert"],
                    "Einheit": Abfrage["Einheit"],
                    "Kritischer Wert": self.KritWerte[Sensor],
                    "Operator": self.Operatoren[Sensor],
                    "Handlung": self.Handlungen[Sensor]
                }
                Sensorwerte[Sensor] = WertUndEinheit
            else:
                WertUndEinheit = {
                    "Wert": "?",
                    "Einheit": "?",
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
        TypeOfMaterial = Ich_bin["Fähigkeit"]["TypeOfMaterial"]
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

        if self.Ontologie_Client.Existiert(self.Name, offersProductionService, TypeOfMaterial)["boolean"] == False:
            Insert = """INSERT DATA {
                DMP:""" + self.Name + """ rdf:type owl:NamedIndividual ,
                DMP:Resource .
                DMP:""" + self.Name + """ DMP:offersProductionService DMP:""" + offersProductionService + """ .\n
                DMP:""" + self.Name + """ DMP:processToM DMP:""" + TypeOfMaterial + """ .\n""" + Dimensionen +\
                Preise + Zeiten + """
                DMP:""" + self.Name + """ DMP:Fehlerquote \"^^""" + str(Fehlerquote) + """\"^^xsd:decimal
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
                Payload = json.dumps({"Auftraggeber": Nachricht["Auftraggeber"], "Schritt": Nachricht["Schritt"],
                                      "Bedarf": Nachricht["Bedarf"], "Auftragseingang": time.asctime()})
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
        self.Broker_2.publish(self.Topic + "/Bedarf", json.dumps({"Name": self.Name, "Bedarf": self.Bedarf}), Qos=2)
        while True:
            Nachricht = self.Q.get()
            '''Ermittelt, wer der Beste ist'''
            Liste_Hersteller = {}
            Güte_Hersteller = {}
            if Nachricht != "Kill":
                for item in Nachricht:
                    Kriterien_Liste = {}
                    Liste = Nachricht[item]
                    if Liste == []:
                        time.sleep(10)
                        self.Broker_2.publish(self.Topic + "/Bedarf",
                                              json.dumps({"Name": self.Name, "Bedarf": self.Bedarf}), Qos=2)
                        continue

                    for DT in Liste:
                        '''Error Handling, Falls nicht instanziierte DT vom Ontologie-Server kommen leer ist'''
                        if DT == None:
                            continue

                        Twin = DT.Ich_bin()
                        TwinName = Twin["Name"]
                        for Schritt in self.Bedarf:
                            Bedarf = self.Bedarf[Schritt]
                            if Bedarf["ProductionService"] == "DrillingService":
                                Zerspanungvolumen = (Bedarf["Dimensionen"]["DiameterHoleResource"] *\
                                                     Bedarf["Dimensionen"]["DiameterHoleResource"] *\
                                                     Bedarf["Dimensionen"]["Depth"])
                                Bezugsgroeße = Zerspanungvolumen
                            elif Bedarf["ProductionService"] == "MillingService":
                                Zerspanungvolumen = (Bedarf["Dimensionen"]["LengthResource"] *\
                                                     Bedarf["Dimensionen"]["WidthResource"] *\
                                                     Bedarf["Dimensionen"]["Depth"])
                                Bezugsgroeße = Zerspanungvolumen

                            elif Bedarf["ProductionService"] == "StampingService":
                                Flaeche = (Bedarf["Dimensionen"]["LengthResource"] * Bedarf["Dimensionen"]["WidthResource"])
                                Bezugsgroeße = Flaeche

                            elif Bedarf["ProductionService"] == "WeldingService":
                                Laenge = (Bedarf["Dimensionen"]["LengthResource"] * Bedarf["Dimensionen"]["WidthResource"])
                                Bezugsgroeße = Laenge

                        '''Preis für das oben berechnete Zerspanungsvolumen berechnen'''
                        if Twin["Preise"]["priceFunction"] == "linear":
                            Preis = Twin["Preise"]["Steigung"] * Bezugsgroeße + Twin["Preise"]["Abschnitt"]

                        elif Twin["Preise"]["priceFunction"] == "exponentiell":
                            Preis = math.exp(Twin["Preise"]["Exponent"]) * Bezugsgroeße + Twin["Preise"]["Abschnitt"]

                        '''Zeit für das oben berechnete Zerspanungsvolumen berechnen'''
                        if Twin["Zeiten"]["timeFunction"] == "linear":
                            Zeiten = Twin["Zeiten"]["Steigung"] * Bezugsgroeße + Twin["Zeiten"]["Abschnitt"]

                        elif Twin["Zeiten"]["timeFunction"] == "exponentiell":
                            Zeiten = math.exp(Twin["Zeiten"]["Exponent"]) * Bezugsgroeße + Twin["Zeiten"]["Abschnitt"]

                        Fehlerquote = Twin["Fehlerquote"]

                        Kriterien = json.dumps({"Preis": Preis, "Zeit": Zeiten, "Fehlerquote": Fehlerquote})
                        '''JSON der Hersteller Erstellen, mit den Werten für Preis, Zeit und Fehlerquote'''
                        Kriterien_Liste[TwinName] = json.loads(Kriterien)
                    Liste_Hersteller[item] = Kriterien_Liste

                for Schritt in Liste_Hersteller:
                    Güte_Liste = {}
                    for DT in Liste_Hersteller[Schritt]:
                        Güte = Liste_Hersteller[Schritt][DT]["Preis"] + Liste_Hersteller[Schritt][DT]["Zeit"] *\
                               (1 + Liste_Hersteller[Schritt][DT]["Fehlerquote"])
                        Güte_Liste[DT] = Güte
                        Güte_Hersteller[Schritt] = Güte_Liste


                '''Hersteller mit für jeden Schritt mit minimalen Kriterien auswählen'''
                Hersteller = {}
                for Schritt in Güte_Hersteller:
                    MinWert = min(Güte_Hersteller[Schritt], key=Güte_Hersteller[Schritt].get)
                    Hersteller[Schritt] = MinWert
                print("Für "+ self.Name + " " + str(Hersteller))

                '''Auftrag für jeden Hersteller versenden'''
                for DT in Hersteller:
                    HK = Hersteller[DT]
                    self.Broker_2.publish(self.Topic + "/Herstellen/" + DT,
                                          json.dumps({"Auftraggeber": self.Name, "Hersteller": HK, "Schritt": DT,
                                                      "Bedarf": self.Bedarf[DT]}))

            if Nachricht == "Kill":
                break