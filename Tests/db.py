from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from random import randrange

# You can generate an API token from the "API Tokens Tab" in the UI
url = "http://localhost:8086"
token = "-DnCnjPN_w0JbBzX6cPLMqdoSyJsne31lj4985R88bRj1pCp_Bi_434T5dwHgq1klKGLumx2joHU65P3l1M0cQ=="
org = "Laufzeitumgebung"
bucket = "Messwerte"

#establish a connection
client = InfluxDBClient(url=url, token=token, org=org)

#instantiate the WriteAPI
write_api = client.write_api(write_options=SYNCHRONOUS)

#instantiate the QueryAPI
query_api = client.query_api()

#create and write the point
while True:
    p = Point("h2o_level").tag("location", "coyote_creek").field("water_level", randrange(100))
    write_api.write(bucket=bucket, org=org, record=p)


#write_api.close()

#return the table and print the result
# result = client.query_api().query(org=org, query=query)
# results = []
# for table in result:
#     for record in table.records:
#         results.append((record.get_value(), record.get_field()))
# print(results)
