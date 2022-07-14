from SPARQLWrapper import SPARQLWrapper, JSON
import json

Preise = json.dumps({"P5": 5.0, "P6": 6.0, "P7": 7.0, "P8": 8.0, "P9": 9.0, "P10": 10.0, "P11": 11.0, "P12": 12.0,
                     "P13": 13.0, "P14": 14.0, "P15": 15.0, "P16": 16.0, "P17": 17.0, "P18": 18.0, "P19": 19.0,
                     "P20": 20.0})
Preise = json.loads(Preise)

'''https://rebeccabilbro.github.io/sparql-from-python/'''

# Specify the fuseki endpoint
sparql = SPARQLWrapper("http://twinserver.kve.hs-mannheim.de:38443/DMP#")

P = ""

for item in Preise:
    P = P + "DMP:Tester_ADT DMP:" + item + " " + "\"" + str(Preise[item]) + "\"^^xsd:decimal .\n"

# Query
sparql.setQuery("""
PREFIX DMP: <http://www.semanticweb.org/lober/ontologies/2022/1/DMP#>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>

INSERT DATA {
    DMP:PTM2 rdf:type owl:NamedIndividual ,
    DMP:Resource .
    DMP:PTM2 DMP:offersProductionService DMP:DrillingService .
    DMP:PTM2 DMP:processToM DMP:Metal .
    DMP:PTM2 DMP:minDepth "1.0"^^xsd:decimal .
    DMP:PTM2 DMP:maxDepth "10.0"^^xsd:decimal .
    DMP:PTM2 DMP:minDiameterHoleResource "1.0"^^xsd:decimal .
    DMP:PTM2 DMP:maxDiameterHoleResource "10.0"^^xsd:decimal .
    DMP:PTM2 DMP:minThickness "1.0"^^xsd:decimal .
    DMP:PTM2 DMP:maxThickness "10.0"^^xsd:decimal .
}

""")


# Methode definieren und ausführen
sparql.method = "POST"
results = sparql.query().info()# .convert()


print(sparql)
