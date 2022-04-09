#class Digital Twin(Asset Digital Twin,Product Demand Digital Twin):
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


# class Asset_Digital_Twin(Digital_Twin):
#     def __init__(self, name, namePT, typ, skill, processing_time, capacity):
#         #self.typ = "Asset Digital Twin"
#         self.skill = skill
#         self.processing_time = processing_time
#         self.capacity = capacity
#
#     def use_skill(self):
#         print("Skill eingesetzt")
#
#     def accept_demand(self):
#         print("Anfrage akzeptiert")
#
# class Product_Demand_Digital_Twin(Digital_Twin):
#     def __init__(self, name, namePT, typ, demand, date_of_delivery):
#         #self.typ = "Asset Digital Twin"
#         self.demand = demand
#         self.date_of_delivery = date_of_delivery
#
#     def submit_demand(self):
#         print("Anfragegestellt")


#
#

#
#
# Digital_Twin.on_msg(DT)
# Digital_Twin.send_msg(DT)
# Digital_Twin.evaluete_data(DT)