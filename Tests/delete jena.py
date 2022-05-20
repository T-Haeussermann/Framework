from SPARQLWrapper import SPARQLWrapper, JSON


'''https://rebeccabilbro.github.io/sparql-from-python/'''

# Specify the fuseki endpoint
#sparql = SPARQLWrapper("http://twinserver.kve.hs-mannheim.de:38443/DMP#")
sparql = SPARQLWrapper("http://127.0.0.1:3030/DMP")

# Query
sparql.setQuery("""
PREFIX DMP: <http://www.semanticweb.org/lober/ontologies/2022/1/DMP#>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>


DELETE {?ProductionResource ?Service ?Material} 
WHERE {?ProductionResource ?Service ?Material
FILTER (?ProductionResource = DMP:Tester_ADT)
}

""")

# Methode definieren und ausführen
sparql.method = "POST"
sparql.query()
