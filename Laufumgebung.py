import paho.mqtt.client as mqtt
import json
import os


_username = "dbt"
_passwd = "dbt"
_host = "mq.jreichwald.de"
_port = 1883
_timeout = 60


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("Laufumgebung/#")


def on_message(client, userdata, msg):
    #print(msg.topic + " : " + str(msg.payload.decode("utf-8")))
    msg = json.loads(str(msg.payload.decode("utf-8")))
    print(msg)
    name = msg['Name']
    if ((msg['Msg'] == "Erstelle DT") and (os.path.exists(name+'.py') == False)):
        print("Ich erstelle jetzt einen DT")
    else:
        print ("DT existiert bereits")


client = mqtt.Client()
client.username_pw_set(_username, _passwd)
client.on_connect = on_connect
client.on_message = on_message
client.connect(_host, _port, _timeout)

# Payload=json.dumps({"Maschine-17": "Erstelle DT"})
# topic = "Laufumgebung"
# client.publish(topic, Payload)


client.loop_forever()