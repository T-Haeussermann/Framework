from SPARQLWrapper import SPARQLWrapper, JSON


'''https://rebeccabilbro.github.io/sparql-from-python/'''

# Specify the fuseki endpoint
sparql = SPARQLWrapper("http://twinserver.kve.hs-mannheim.de:38443/DMP#")

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
    DMP:Tester_ADT DMP:diameterHoleResource 0.015 .
    DMP:Tester_ADT DMP:maxThickness 0.06 .
    DMP:Tester_ADT DMP:minThickness 0.02 .
    DMP:Tester_ADT DMP:offersProductionService DMP:DrillingService .
    DMP:Tester_ADT DMP:processToM DMP:Metal .
}
""")

# Methode definieren
sparql.method = "POST"
sparql.query()
