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

t = json.dumps({"Bedarf": {"Schritt 1": {"ProductionService": "DrillingService", "TypeOfMaterial": "Metal", "Geometrie": "Kreis", "Dimensionen": {"DiameterHoleResource": 15.0, "Depth": 30.0, "Thickness": 55.0}}}})
t = json.loads(t)
print(t)