from SPARQLWrapper import SPARQLWrapper, JSON
import datetime

'''https://www.youtube.com/watch?v=zdaL6unnv7Y'''

# Specify the DBPedia endpoint
sparql = SPARQLWrapper("http://dbpedia.org/sparql")

# Query for the description of "Capsaicin", filtered by language
sparql.setQuery("""
    SELECT ?object
    WHERE { dbr:Cat rdfs:label ?object.
         FILTER (LANG(?object)='nl')}
    # WHERE { dbr:Barack_Obama dbo:abstract ?object .
    #     FILTER (LANG(?object)='nl')}
""")

# Convert results to JSON format
sparql.setReturnFormat(JSON)
result = sparql.query().convert()

# The return data contains "bindings" (a list of dictionaries)
for hit in result["results"]["bindings"]:
    #print(hit["object"])
    lang, value = hit["object"]["xml:lang"], hit["object"]["value"]
    print(f"Lang: {lang} Value: {value}")
