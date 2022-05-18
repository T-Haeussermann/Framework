from SPARQLWrapper import SPARQLWrapper, JSON
import json

Preise = json.dumps({"P5": 5, "P6": 6, "P7": 7, "P8": 8, "P9": 9, "P10": 10, "P11": 11, "P12": 12, "P13": 13, "P14": 14,
                     "P15": 15, "P16": 16, "P17": 17, "P18": 18, "P19": 19, "P20": 20})
Preise = json.loads(Preise)

'''https://rebeccabilbro.github.io/sparql-from-python/'''

# Specify the fuseki endpoint
sparql = SPARQLWrapper("http://twinserver.kve.hs-mannheim.de:38443/DMP#")

P = ""

for item in Preise:
    P = P + "DMP:Tester_ADT DMP:" + item + " " + "\"" + str(Preise[item]) + "\"^^xsd:decimal .\n"
print(P)
# Query
sparql.setQuery("""
PREFIX DMP: <http://www.semanticweb.org/lober/ontologies/2022/1/DMP#>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>

INSERT DATA {
    DMP:Tester_ADT rdf:type owl:NamedIndividual ,
    DMP:Resource .
    DMP:Tester_ADT DMP:diameterHoleResource "0.015"^^xsd:decimal .
    DMP:Tester_ADT DMP:maxThickness "0.06"^^xsd:decimal .
    DMP:Tester_ADT DMP:minThickness  "0.02"^^xsd:decimal .\n"""
    + P + """
    DMP:Tester_ADT DMP:offersProductionService DMP:DrillingService .
    DMP:Tester_ADT DMP:processToM DMP:Metal .
}

""")


# Methode definieren und ausführen
sparql.method = "POST"
sparql.query()
