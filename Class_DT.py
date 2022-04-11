import time
from queue import Queue

class Digital_Twin:
    """Klasse normaler Twin ohne Fähigkeit Digital Twin"""
    def __init__(self, Name, Typ, q):
        self.Name = Name
        self.Typ = Typ
        self.q = q

    def DT_Ablauf(self):
        while True:
            print(self.Name)
            # Messwert = self.q.get()
            # print(Messwert)
            # print("der Wert oben sollte aus der Q sein")
            # try:
            #     Messwert = self.q.get()
            #     print(Messwert)
            #     print("der Wert oben sollte aus der Q sein")
            # except Exception:
            #     print("Läuft nicht")

            time.sleep(5)


class Asset_Digital_Twin(Digital_Twin):
    def __init__(self, Name, Typ, Fähigkeit):
        super().__init__(Name, Typ)
        self.Fähigkeit = Fähigkeit

    def ADT_Ablauf(self):
        while True:
            print(self.Name)
            time.sleep(5)


class Product_Demand_Digital_Twin(Digital_Twin):
    def __init__(self, Name, Typ, Bedarf):
        super().__init__(Name, Typ)
        self.Bedarf = Bedarf

    def PDDT_Ablauf(self):
        while True:
            print(self.Name)
            time.sleep(5)
