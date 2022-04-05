#class Digital Twin(Asset Digital Twin,Product Demand Digital Twin):

class Digital_Twin:
    """Klasse Digital Twin, Quelle: https://medium.com/swlh/classes-subclasses-in-python-12b6013d9f3"""
    def __init__(self, name, namePT, typ):
        self.name = name
        self.namePT = namePT
        self.typ = typ

    def on_msg(self):
        print("Nachricht empfangen")

    def send_msg(self):
        print("Nachricht gesendet")

    def evaluete_data(self):
        print("Daten ausgewertet")


class Asset_Digital_Twin(Digital_Twin):
    def __init__(self, name, namePT, typ, skill, processing_time, capacity):
        #self.typ = "Asset Digital Twin"
        self.skill = skill
        self.processing_time = processing_time
        self.capacity = capacity

    def use_skill(self):
        print("Skill eingesetzt")

    def accept_demand(self):
        print("Anfrage akzeptiert")

class Product_Demand_Digital_Twin(Digital_Twin):
    def __init__(self, name, namePT, typ, demand, date_of_delivery):
        #self.typ = "Asset Digital Twin"
        self.demand = demand
        self.date_of_delivery = date_of_delivery

    def submit_demand(self):
        print("Anfragegestellt")

