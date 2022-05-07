import json


Preise = json.dumps({"5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
                    "11": 11, "12": 12, "13": 13, "14": 14, "15": 15,
                    "16": 16, "17": 17, "18": 18, "19": 19, "20": 20})
Preise = json.loads(Preise)

Zeiten = json.dumps({"5": 50, "6": 60, "7": 70, "8": 80, "9": 90, "10": 100,
                    "11": 110, "12": 120, "13": 130, "14": 140, "15": 150,
                   "16": 160, "17": 170, "18": 180, "19": 190, "20": 200})
Zeiten = json.loads(Zeiten)

Fehlerquote = 0.1
j = json.dumps({"Preise": Preise, "Zeiten": Zeiten, "Fehlerquote": Fehlerquote})
j = json.loads(j)

Bedarf = json.dumps({"Art": "Rechteck", "Material": "ST 37", "Geometrie": "Kreis",
                     "Dimensionen": {"Dimension X": 20, "Dimension Y": 20, "Dimension Z": 20}})
Bedarf = json.loads(Bedarf)

Liste_Fertig = {}
Liste_DTs = {"Tester_ADT", "Tester_PDDT", "Tester_DT"}

for item in Liste_DTs:
    if Bedarf["Art"] == "Loch":
        Liste = []
        for ET in j["Preise"]:
            if ET == str(Bedarf["Dimensionen"]["Dimension X"]):
                Liste.append(j["Preise"][ET])

        for ET in j["Zeiten"]:
            if ET == str(Bedarf["Dimensionen"]["Dimension X"]):
                Liste.append(j["Zeiten"][ET])

        Liste.append(j["Fehlerquote"])
        Liste_Fertig[item] = Liste

    if Bedarf["Art"] == "Kreis":
        Liste = []
        for ET in j["Preise"]:
            if ET == str(Bedarf["Dimensionen"]["Dimension X"]):
                Liste.append(j["Preise"][ET])

        for ET in j["Zeiten"]:
            if ET == str(Bedarf["Dimensionen"]["Dimension X"]):
                Liste.append(j["Zeiten"][ET])

        Liste.append(j["Fehlerquote"])
        Liste_Fertig[item] = Liste

    if Bedarf["Art"] == "Rechteck":
        Liste = []
        for ET in j["Preise"]:
            if ET == str(Bedarf["Dimensionen"]["Dimension X"]) + "x" + str(Bedarf["Dimensionen"]["Dimension Y"]):
                Liste.append(j["Preise"][ET])

        for ET in j["Zeiten"]:
            if ET == str(Bedarf["Dimensionen"]["Dimension X"]) + "x" + str(Bedarf["Dimensionen"]["Dimension Y"]):
                Liste.append(j["Zeiten"][ET])

        Liste.append(j["Fehlerquote"])
        Liste_Fertig[item] = Liste


def f(a, b, c):
    Güte = a + b + 2*c
    return Güte

Hersteller = {}

for DT in Liste_Fertig:
    Güte = Liste_Fertig[DT][0] + Liste_Fertig[DT][1] + 2*Liste_Fertig[DT][2]
    Hersteller[DT] = Güte
    print(Hersteller)

'''https://stackoverflow.com/questions/3282823/get-the-key-corresponding-to-the-minimum-value-within-a-dictionary'''

MinWert = min(Hersteller.values())
MinHersteller = [k for k, v in Hersteller.items() if v==MinWert]
'''Wenn mehrere DTs den gleichen Wert haben, nimm den ersten'''
final = {MinHersteller[0]: MinWert}
print(final)