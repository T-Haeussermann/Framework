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
        self.Topic = "Laufzeitumgebung/" + self.Name + "/Handlung"

    def DT_Ablauf(self):
        while True:
            Nachricht = self.Q.get()
            print(Nachricht)



class Asset_Digital_Twin(Digital_Twin):
    def __init__(self, Name, Typ, Broker_1, Broker_2, DB_Client, KritWert, Operator, Handlung, Fähigkeit):
        super().__init__(Name, Typ, Broker_1, Broker_2)
        self.DB_Client = DB_Client
        self.KritWert = KritWert
        self.Operator = Operator
        self.Handlung = Handlung
        self.Fähigkeit = Fähigkeit

    def ADT_Ablauf(self):
        while True:
            print(type(self.Fähigkeit["Geometrie"]["Dimension X"]))
            Nachricht = self.Q.get()
            Messwert = Nachricht["Messwert"]
            Messwert_str = str(Nachricht["Messwert"])
            Einheit = Nachricht["Einheit"]
            print(Messwert_str + " " + Einheit + " von einem " + self.Typ + " gemessen")
            Punkt = Point("Messwert").tag("Name", self.Name).field("Gewicht",Messwert)
            self.DB_Client.Schreiben(Punkt)
            if self.Operator == ">":
                if Messwert > self.KritWert:
                    Payload = json.dumps({"Name": self.Name, "Ausführen": self.Handlung})
                    self.Broker_1.publish(self.Topic, Payload)
            elif self.Operator == "<":
                if Messwert < self.KritWert:
                    Payload = json.dumps({"Name": self.Name, "Ausführen": self.Handlung})
                    self.Broker_1.publish(self.Topic, Payload)


class Product_Demand_Digital_Twin(Digital_Twin):
    def __init__(self, Name, Typ, Broker_1, Broker_2, Bedarf):
        super().__init__(Name, Typ, Broker_1, Broker_2)
        self.Bedarf = Bedarf

    def PDDT_Ablauf(self):
        while True:
            Nachricht = self.Q.get()
            print(Nachricht)
            # Messwert = Nachricht["Messwert"]
            # Messwert_str = str(Nachricht["Messwert"])
            # Einheit = Nachricht["Einheit"]
            # print(Messwert_str + " " + Einheit + " von einem " + self.Typ + " gemessen")
            # Punkt = Point("Messwert").tag("Name", self.Name).field("Gewicht", Messwert)
            # self.DB_Client.Schreiben(Punkt)
            # if self.Operator == ">":
            #     if Messwert > self.KritWert:
            #         Payload = json.dumps({"Name": self.Name, "Ausführen": self.Handlung})
            #         self.Broker_1.publish(self.Topic, Payload)
            # elif self.Operator == "<":
            #     if Messwert < self.KritWert:
            #         Payload = json.dumps({"Name": self.Name, "Ausführen": self.Handlung})
            #         self.Broker_1.publish(self.Topic, Payload)
