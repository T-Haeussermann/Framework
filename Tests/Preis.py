import json
import math


Volumen = 1000
Preis = json.dumps({"priceFunction": "linear", "Steigung": 100, "Abschnitt": 100})
#Preis = json.dumps({"priceFunction": "exponentiell", "Exponent": 3, "Abschnitt": 100})
Preis = json.loads(Preis)

if Preis["priceFunction"] == "linear":
    P = Preis["Steigung"] * Volumen + 100

elif Preis["priceFunction"] == "exponentiell":
    P = math.exp(Preis["Exponent"]) * Volumen + 100
print(P)