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



class Asset_Digital_Twin(Digital_Twin):
    def __init__(self, Name, Typ, Sensoren, Broker_1, Broker_2, DB_Client, KritWerte, Operatoren, Handlungen, Fähigkeit):
        super().__init__(Name, Typ, Broker_1, Broker_2)
        self.Sensoren = Sensoren
        self.DB_Client = DB_Client
        self.KritWerte = KritWerte
        self.Operatoren = Operatoren
        self.Handlungen = Handlungen
        self.Fähigkeit = Fähigkeit
        self.Topic = "Laufzeitumgebung/" + self.Name + "/Handlungen"

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
        Ich_bin = json.dumps({"Name": self.Name, "Typ": self.Typ, "Fähigkeit": self.Fähigkeit, "Sensoren": Sensorwerte})
        Ich_bin = json.loads(Ich_bin)
        return Ich_bin

    def ADT_Ablauf(self):
        self.DB_Client.New_Bucket(self.Name)
        while True:
            '''Warten bis sich eine Nachricht mit Messwerten in der Queue befindet.
            Datenpunkt erstellen und in der Datenbank ablegen'''
            Nachricht = self.Q.get()
            Sensorname = list(Nachricht["Messwert"].keys())[0]
            Sensoreinheit = Nachricht["Messwert"]["Einheit"]
            Sensorwert = Nachricht["Messwert"][Sensorname]
            Messpunkt = Point("Messwerte").tag("Sensor", Sensorname).field(Sensoreinheit, Sensorwert)
            self.DB_Client.Schreiben(self.Name, Messpunkt)

            '''Status prüfen und ggf. Handlung publishen'''
            try:
                Status = self.Ich_bin()
                for Sensor in Status["Sensoren"]:
                    if Status["Sensoren"][Sensor]["Operator"] == ">":
                        if Status["Sensoren"][Sensor]["Wert"] > Status["Sensoren"][Sensor]["Kritischer Wert"]:
                            Payload = json.dumps({"Name": self.Name, "Ausführen": Status["Sensoren"][Sensor]["Handlung"]})
                            self.Broker_1.publish(self.Topic + "/" + Sensor, Payload)
                    if Status["Sensoren"][Sensor]["Operator"] == "<":
                        if Status["Sensoren"][Sensor]["Wert"] < Status["Sensoren"][Sensor]["Kritischer Wert"]:
                            Payload = json.dumps({"Name": self.Name, "Ausführen": Status["Sensoren"][Sensor]["Handlung"]})
                            self.Broker_1.publish(self.Topic + "/" + Sensor, Payload)
            except:
                pass





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
            # Ermittel wer der Beste ist
            Name = Nachricht["DTs"]
            self.Broker_2.publish(self.Topic + "/Herstellen", json.dumps({"Name": self.Name,
                                                                           "Hersteller": Name,
                                                                           "Bedarf": self.Bedarf}))
