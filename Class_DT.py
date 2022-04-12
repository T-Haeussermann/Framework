import time
from queue import Queue

class Digital_Twin:
    """Klasse normaler Twin ohne Fähigkeit Digital Twin"""
    def __init__(self, Name, Typ):
        self.Name = Name
        self.Typ = Typ
        self.Q = Queue()

    # def __repr__(self):
    #     rep = self.Name
    #     return rep

    def DT_Ablauf(self):
        while True:
            print(self.Name)
            print(self.Q)
            # Messwert = self.Name.get()
            # print(Messwert)
            # print("der Wert oben sollte aus der Q sein")
            # try:
            #     Messwert = self.Name.get()
            #     print(Messwert)
            #     print("der Wert oben sollte aus der Q sein")
            # except Exception:
            #     print("Läuft nicht")

            time.sleep(5)


class Asset_Digital_Twin(Digital_Twin):
    def __init__(self, Name, Typ, Fähigkeit):
        super().__init__(Name, Typ)
        self.Q = Queue()
        self.Fähigkeit = Fähigkeit

    # def __repr__(self):
    #     rep = self.Name
    #     return rep

    def ADT_Ablauf(self):
        while True:
            print(self.Name)
            time.sleep(5)


class Product_Demand_Digital_Twin(Digital_Twin):
    def __init__(self, Name, Typ, Bedarf):
        super().__init__(Name, Typ)
        self.Q = Queue()
        self.Bedarf = Bedarf

    # def __repr__(self):
    #     rep = self.Name
    #     return rep

    def PDDT_Ablauf(self):
        while True:
            print(self.Name)
            time.sleep(5)
