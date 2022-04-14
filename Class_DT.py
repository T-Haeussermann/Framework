from queue import Queue
import json
from MQTT import MQTT

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
            print(Messwert_str + " " + Einheit + " von Typ DT")
            self.Broker_1.publish(self.Topic, "Das läuft von Instanz zu Instanz")
            if Messwert > 10:
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
            Messwert = str(Nachricht["Messwert"])
            Einheit = Nachricht["Einheit"]
            print(Messwert + " " + Einheit + " von Typ ADT")
            self.Broker_1.publish(self.Topic, "ADT")


class Product_Demand_Digital_Twin(Digital_Twin):
    def __init__(self, Name, Typ, Broker_1, Broker_2, Bedarf):
        super().__init__(Name, Typ, Broker_1, Broker_2)
        self.Q = Queue()
        self.Bedarf = Bedarf

    def PDDT_Ablauf(self):
        while True:
            Nachricht = self.Q.get()
            Messwert = str(Nachricht["Messwert"])
            Einheit = Nachricht["Einheit"]
            print(Messwert + " " + Einheit  + " von Typ PDDT")
            self.Broker_1.publish(self.Topic, "PDDT")
