import time

class Digital_Twin:
    """Klasse Digital Twin, Quelle: https://medium.com/swlh/classes-subclasses-in-python-12b6013d9f3"""
    def __init__(self, Name, Typ):
        self.Name = Name
        self.Typ = Typ

    def DT_Ablauf(self):
        while True:
            print(self.Name)
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
