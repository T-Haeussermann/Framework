import json
from random import randrange

Sensoren = ["S1", "S2", "S3"]
jsondata = {}

for Sensor in Sensoren:
    test = {
        "Wert": randrange(10),
        "Einheit": "Newton"
        }

    jsondata[Sensor] = test


print(json.dumps(jsondata, indent=4))