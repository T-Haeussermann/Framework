import paho.mqtt.client as mqtt
import json
import time


_username = "dbt"
_passwd = "dbt"
_host = "mq.jreichwald.de"
_port = 1883
_timeout = 60
topic1 = "Laufumgebung/PT-17/Task"
topic2 = "Laufumgebung/PT-17/Messwert"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("Laufumgebung/Maschine/#")


# def on_message(client, userdata, msg):
#     #print(msg.topic + " : " + str(msg.payload.decode("utf-8")))
#     msg = json.loads(str(msg.payload.decode("utf-8")))
#     print(msg)
#     name = msg['Name']
#     if ((msg['Msg'] == "Erstelle DT") and (os.path.exists(name+'.py') == False)):
#         print("Ich erstelle jetzt einen DT")
#     else:
#         print ("DT existiert bereits")

client = mqtt.Client()
client.username_pw_set(_username, _passwd)
client.on_connect = on_connect
client.connect(_host, _port, _timeout)



Payload=json.dumps({"Name": "Maschine 17", "Task": "Erstelle DT"})
client.publish(topic1, Payload)

while True:
    # client.on_message = on_message


    Messwert=json.dumps({"Name": "Maschine 17", "Messwert": "20", "Einheit": "Celsius"})

    client.publish(topic2, Messwert)
    time.sleep(10)


