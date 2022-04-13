from queue import Queue
import json
from MQTT import MQTT

class Digital_Twin:
    """Klasse normaler Twin ohne Fähigkeit Digital Twin"""
    def __init__(self, Name, Typ):
        self.Name = Name
        self.Typ = Typ
        self.Q = Queue()
        self.Topic = "Laufzeitumgebung/" + self.Name + "/Handlung"

    def DT_Ablauf(self):
        while True:
            # print(self.Name)
            # print(self.Q)
            Nachricht = self.Q.get()
            Messwert = Nachricht["Messwert"]
            Messwert_str = str(Nachricht["Messwert"])
            Einheit = Nachricht ["Einheit"]
            print(Messwert_str + " " + Einheit + " von Typ DT")
            # Broker_1.publish("Test", "Test")
            # if Messwert > 10:
            #     Payload = json.dumps({"Name": self.Name, "Ausführen": "Kühlmittel aktivieren"})
                #on_publish(client,Topic, Payload)



class Asset_Digital_Twin(Digital_Twin):
    def __init__(self, Name, Typ, Fähigkeit):
        super().__init__(Name, Typ)
        self.Q = Queue()
        self.Fähigkeit = Fähigkeit

    def ADT_Ablauf(self):
        while True:
            # print(self.Name)
            Nachricht = self.Q.get()
            Messwert = str(Nachricht["Messwert"])
            Einheit = Nachricht["Einheit"]
            print(Messwert + " " + Einheit + " von Typ ADT")


class Product_Demand_Digital_Twin(Digital_Twin):
    def __init__(self, Name, Typ, Bedarf):
        super().__init__(Name, Typ)
        self.Q = Queue()
        self.Bedarf = Bedarf

    def PDDT_Ablauf(self):
        while True:
            # print(self.Name)
            Nachricht = self.Q.get()
            Messwert = str(Nachricht["Messwert"])
            Einheit = Nachricht["Einheit"]
            print(Messwert + " " + Einheit  + " von Typ PDDT")
