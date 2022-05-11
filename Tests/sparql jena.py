import json

from SPARQLWrapper import SPARQLWrapper, JSON
import html


'''https://rebeccabilbro.github.io/sparql-from-python/'''

# Specify the DBPedia endpoint
sparql = SPARQLWrapper("http://twinserver.kve.hs-mannheim.de:38443/DMP")

# Query for the description of "Capsaicin", filtered by language
sparql.setQuery("""
PREFIX DMP: <http://www.semanticweb.org/lober/ontologies/2022/1/DMP#>

SELECT ?Product ?ProductionPlan
WHERE {?Product DMP:hasProductionPlan ?ProductionPlan.
}
""")

# Convert results to JSON format
sparql.setReturnFormat(JSON)
result = sparql.query().convert()

# for item in result["results"]["bindings"]:
#     print(item["o"]["value"])


#print(json.dumps(result,sort_keys=True, indent=4))
#print(type(result))

for hit in result["results"]["bindings"]:
    for item in hit:
        print(str(item) + ": " + str(hit[item]["value"].replace("http://www.semanticweb.org/lober/ontologies/2022/1/DMP#","")))
