from queue import Queue
import json
from MQTT import MQTT

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
            Messwert = Nachricht["Messwert"]
            Messwert_str = str(Nachricht["Messwert"])
            Einheit = Nachricht ["Einheit"]
            print(Messwert_str + " " + Einheit + " von einem " + self.Typ + " gemessen")
            if Messwert > 50:
                Payload = json.dumps({"Name": self.Name, "Ausführen": "Kühlmittel aktivieren"})
                self.Broker_1.publish(self.Topic, Payload)



class Asset_Digital_Twin(Digital_Twin):
    def __init__(self, Name, Typ, Broker_1, Broker_2, Fähigkeit):
        super().__init__(Name, Typ, Broker_1, Broker_2)
        self.Q = Queue()
        self.Fähigkeit = Fähigkeit

    def ADT_Ablauf(self):
        while True:
            Nachricht = self.Q.get()
            Messwert = Nachricht["Messwert"]
            Messwert_str = str(Nachricht["Messwert"])
            Einheit = Nachricht["Einheit"]
            print(Messwert_str + " " + Einheit + " von einem " + self.Typ + " gemessen")
            if Messwert > 10:
                Payload = json.dumps({"Name": self.Name, "Ausführen": "Kraft erhöhen"})
                self.Broker_1.publish(self.Topic, Payload)


class Product_Demand_Digital_Twin(Digital_Twin):
    def __init__(self, Name, Typ, Broker_1, Broker_2, Bedarf):
        super().__init__(Name, Typ, Broker_1, Broker_2)
        self.Q = Queue()
        self.Bedarf = Bedarf

    def PDDT_Ablauf(self):
        while True:
            Nachricht = self.Q.get()
            Messwert = Nachricht["Messwert"]
            Messwert_str = str(Nachricht["Messwert"])
            Einheit = Nachricht["Einheit"]
            print(Messwert_str + " " + Einheit + " von einem " + self.Typ + " gemessen")
            if Messwert > 10:
                Payload = json.dumps({"Name": self.Name, "Ausführen": "Gewicht erhöhen"})
                self.Broker_1.publish(self.Topic, Payload)
