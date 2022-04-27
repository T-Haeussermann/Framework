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
    def __init__(self, Name, Typ, Sensoren, Broker_1, Broker_2, DB_Client, KritWert, Operator, Handlung, Fähigkeit):
        super().__init__(Name, Typ, Broker_1, Broker_2)
        self.Sensoren = Sensoren
        self.DB_Client = DB_Client
        self.KritWert = KritWert
        self.Operator = Operator
        self.Handlung = Handlung
        self.Fähigkeit = Fähigkeit
        self.Topic = "Laufzeitumgebung/" + self.Name + "/Handlung"

    def Ich_bin(self):
        Sensorwerte = {}
        for Sensor in self.Sensoren:
            WertUndEinheit = {
                "Wert": self.DB_Client.Query(self.Name, Sensor)["Messwert"],
                "Einheit": self.DB_Client.Query(self.Name, Sensor)["Einheit"]
            }

            Sensorwerte[Sensor] = WertUndEinheit

        Ich_bin = json.dumps({"Name": self.Name, "Typ": self.Typ, "Fähigkeit": self.Fähigkeit, "Sensoren": Sensorwerte})
        Ich_bin = json.loads(Ich_bin)
        return Ich_bin

    def ADT_Ablauf(self):
        self.DB_Client.New_Bucket(self.Name)
        while True:
            Nachricht = self.Q.get()
            Sensorname = list(Nachricht["Messwert"].keys())[0]
            Sensoreinheit = Nachricht["Messwert"]["Einheit"]
            Sensorwert = Nachricht["Messwert"][Sensorname]
            Messpunkt = Point("Messwerte").tag("Sensor", Sensorname).field(Sensoreinheit, Sensorwert)
            self.DB_Client.Schreiben(self.Name, Messpunkt)
            # Messwert = Nachricht["Messwert"]
            # Messwert_str = str(Nachricht["Messwert"])
            # Einheit = Nachricht["Einheit"]
            # print(Messwert_str + " " + Einheit + " von einem " + self.Typ + " gemessen")
            # Punkt = Point("Messwert").tag("Name", self.Name).field("Gewicht",Messwert)
            # if self.Operator == ">":
            #     if Messwert > self.KritWert:
            #         Payload = json.dumps({"Name": self.Name, "Ausführen": self.Handlung})
            #         self.Broker_1.publish(self.Topic, Payload)
            # elif self.Operator == "<":
            #     if Messwert < self.KritWert:
            #         Payload = json.dumps({"Name": self.Name, "Ausführen": self.Handlung})
            #         self.Broker_1.publish(self.Topic, Payload)


class Product_Demand_Digital_Twin(Digital_Twin):
    def __init__(self, Name, Typ, Broker_1, Broker_2, Bedarf):
        super().__init__(Name, Typ, Broker_1, Broker_2)
        self.Bedarf = Bedarf
        self.Topic = "Laufzeitumgebung/" + self.Name + "/Bedarf"

    def Ich_bin(self):
        Ich_bin = json.dumps({"Name": self.Name, "Typ": self.Typ, "Bedarf": self.Bedarf})
        Ich_bin = json.loads(Ich_bin)
        return Ich_bin

    def PDDT_Ablauf(self):
        self.Broker_2.publish(self.Topic, json.dumps(self.Bedarf))
        while True:
            Nachricht = self.Q.get()
            print(Nachricht)
