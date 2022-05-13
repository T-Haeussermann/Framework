from Laufzeitumgebung.Class_Ontologie import Ontologie
import threading


LockAb_Ontologie = threading.Lock()
LockAn_Ontologie = threading.Lock()
Test = Ontologie(LockAb_Ontologie, LockAn_Ontologie)

Select = "SELECT ?ProductionResource ?Service ?diameterHoleResource ?maxThickness ?minThickness"
Where = """WHERE {?ProductionResource DMP:offersProductionService ?Service .
       ?ProductionResource DMP:processToM ?Metal .
       ?ProductionResource DMP:diameterHoleResource ?diameterHoleResource .
       ?ProductionResource DMP:maxThickness ?maxThickness . 
       ?ProductionResource DMP:minThickness ?minThickness .
       FILTER (?ProductionResource = DMP:Tester_ADT)
        }"""

# erg = Test.Abfrage(Select, Where)
# print(erg)

erg = Test.Existiert("Tester_ADT", "DrillingService", "Metal")
print(type(erg["boolean"]))

Prefix = """PREFIX DMP: <http://www.semanticweb.org/lober/ontologies/2022/1/DMP#>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>"""
Insert = """INSERT DATA {
    DMP:Tester_ADT rdf:type owl:NamedIndividual ,
    DMP:Resource .
    DMP:Tester_ADT DMP:diameterHoleResource "0.015"^^xsd:decimal .
    DMP:Tester_ADT DMP:maxThickness "0.06"^^xsd:decimal .
    DMP:Tester_ADT DMP:minThickness "0.02"^^xsd:decimal .
    DMP:Tester_ADT DMP:offersProductionService DMP:DrillingService .
    DMP:Tester_ADT DMP:processToM DMP:Metal .
}"""

# Test.Anlegen(Prefix, Insert)
