from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate an API token from the "API Tokens Tab" in the UI
url = "http://localhost:8086"
token = "-DnCnjPN_w0JbBzX6cPLMqdoSyJsne31lj4985R88bRj1pCp_Bi_434T5dwHgq1klKGLumx2joHU65P3l1M0cQ=="
org = "Laufzeitumgebung"
bucket = "Messwerte"

class Influxdb:
    def __init__(self, url, token, org, bucket, lock):
        self.url = url
        self.token = token
        self. org = org
        self.bucket = bucket
        self.lock = lock
        self.dbclient = InfluxDBClient(url=url, token=token, org=org)
        self.write_api = self.dbclient.write_api(write_options=SYNCHRONOUS)


    def Schreiben(self, Punkt):
        self.lock.acquire()
        self.write_api.write(bucket=self.bucket, org=self.org, record=Punkt)
        self.lock.release()
