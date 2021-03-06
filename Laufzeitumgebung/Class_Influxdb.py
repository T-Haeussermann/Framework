import json
from influxdb_client import InfluxDBClient, BucketRetentionRules
from influxdb_client.client.write_api import SYNCHRONOUS



# You can generate an API token from the "API Tokens Tab" in the UI
url = "http://localhost:8086"
token = "-DnCnjPN_w0JbBzX6cPLMqdoSyJsne31lj4985R88bRj1pCp_Bi_434T5dwHgq1klKGLumx2joHU65P3l1M0cQ=="
org = "Laufzeitumgebung"

class Influxdb:
    def __init__(self, url, token, org, lock):
        self.url = url
        self.token = token
        self. org = org
        self.lock = lock
        #self.dbclient = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        #self.buckets_api = self.dbclient.buckets_api()
        # self.retention_rules = BucketRetentionRules(type="expire", every_seconds=86400) #Bei Bedarf ausfüllen
        #self.write_api = self.dbclient.write_api(write_options=SYNCHRONOUS)

    @property
    def dbclient(self):
        return InfluxDBClient(url=self.url, token=self.token, org=self.org)

    @property
    def buckets_api(self):
        return self.dbclient.buckets_api()

    @property
    def write_api(self):
        return self.dbclient.write_api(write_options=SYNCHRONOUS)

    def Schreiben(self, Bucket, Punkt):
        self.lock.acquire()
        self.write_api.write(bucket=Bucket, org=self.org, record=Punkt)
        self.lock.release()

    def New_Bucket(self, Name):
        if self.buckets_api.find_bucket_by_name(bucket_name=Name) == None:
            self.buckets_api.create_bucket(bucket_name=Name, retention_rules=None, org=self.org)
        else:
            pass

    def Query(self, Name, Sensor):

        if Sensor == "all":
            '''Sucht die letzten Werte aller Sensoren eines DTs heraus'''
            ListeSensoren = []
            query = '''from(bucket: "''' + Name + '''")
                |> range(start: -1h)
                |> filter(fn: (r) => r["_measurement"] == "Messwerte")
                |> last()'''
            tables = self.dbclient.query_api().query(query, org=org)

            for table in tables:
                for record in table.records:
                    Sensor = record["Sensor"]
                    Messwert = record["_value"]
                    Einheit = record["_field"]
                    Antwort = json.dumps({"Sensor": Sensor, "Messwert": Messwert, "Einheit": Einheit})
                    Antwort = json.loads(Antwort)
                    ListeSensoren.append(Antwort)
            return ListeSensoren

        else:
            query = '''from(bucket: "''' + Name + '''")
                |> range(start: -1h)
                |> filter(fn: (r) => r["_measurement"] == "Messwerte")
                |> filter(fn: (r) => r["Sensor"] == "''' + Sensor + '''")
                |> last()'''

            tables = self.dbclient.query_api().query(query, org=org)
            if tables !=0:
                for table in tables:
                    for record in table.records:
                        Sensor = record["Sensor"]
                        Messwert = record["_value"]
                        Einheit = record["_field"]
                        if Messwert != None:
                            Antwort = json.dumps({"Sensor": Sensor, "Messwert": Messwert, "Einheit": Einheit})
                        else:
                            Antwort = json.dumps({"Sensor": Sensor, "Messwert": "-", "Einheit": Einheit})
                        Antwort = json.loads(Antwort)
                    return Antwort
            else:
                return None
