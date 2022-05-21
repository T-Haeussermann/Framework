from SPARQLWrapper import SPARQLWrapper, JSON

'''https://rebeccabilbro.github.io/sparql-from-python/'''

class Ontologie:

    def __init__(self):

        #self.sparql = SPARQLWrapper("http://twinserver.kve.hs-mannheim.de:38443/DMP")
        self.sparql = SPARQLWrapper("http://127.0.0.1:3030/DMP")
        self.Prefix = """PREFIX DMP: <http://www.semanticweb.org/lober/ontologies/2022/1/DMP#>
        PREFIX owl:  <http://www.w3.org/2002/07/owl#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>\n"""

    def Existiert(self, Name, Service, Material):
        Ask = """ASK {DMP:""" + Name + """ rdf:type owl:NamedIndividual ,
                 DMP:Resource .
                 DMP:""" + Name + """ DMP:offersProductionService DMP:""" + Service + """ .
                 DMP:""" + Name + """ DMP:processToM DMP:""" + Material + """ .
                 }"""
        self.sparql.setQuery(self.Prefix + Ask)

        # Convert results to JSON format
        self.sparql.setReturnFormat(JSON)
        Result = self.sparql.query().convert()
        return Result

    def Abfrage(self, Select, Where):
        self.sparql.setQuery(self.Prefix + " " + Select + " " + Where)
        # Convert results to JSON format
        self.sparql.setReturnFormat(JSON)
        Result = self.sparql.query().convert()
        ListeHersteller = []
        for hit in Result["results"]["bindings"]:
            for item in hit:
                Hersteller = hit[item]["value"].replace("http://www.semanticweb.org/lober/ontologies/2022/1/DMP#", "")
                ListeHersteller.append(Hersteller)
        return ListeHersteller

    def Anlegen(self, Insert):
        self.sparql.setQuery(self.Prefix + " " + Insert)

        # Methode definieren und ausführen
        self.sparql.method = "POST"
        self.sparql.query()


    def Löschen(self, Name):
        '''Löscht die semantische Repräsentation des DTs mit dem eingegebenen Namen'''

        Delete = """DELETE {?ProductionResource ?Service ?Material} 
        WHERE {?ProductionResource ?Service ?Material
        FILTER (?ProductionResource = DMP:""" + Name + """)
        }"""

        # Methode definieren und ausführen
        self.sparql.setQuery(self.Prefix + " " + Delete)
        self.sparql.method = "POST"
        self.sparql.query()

