import paho.mqtt.client as mqtt
import json
import os
import shutil
import subprocess
import sys
import fileinput

subprocess.Popen([sys.executable, "Maschine 17_DT.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT) # Startet Script im Hintergrund


_username = "dbt"
_passwd = "dbt"
_host = "mq.jreichwald.de"
_port = 1883
_timeout = 60


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("Laufumgebung/#") #("Laufumgebung/#")


def on_message(client, userdata, msg):
    TopicUndNachricht = msg.topic + " : " + str(msg.payload.decode("utf-8")) #string
    msg = json.loads(str(msg.payload.decode("utf-8")))
    #print(msg.topic + " : " + str(msg.payload.decode("utf-8")))
    #print(type(TopicUndNachricht))
    #print(msg)
    #name = msg['Name']
    if ("/Anforderung" in TopicUndNachricht and msg['Task'] == "Erstelle DT"):
         print("Ich stelle DT mit dem Namen " + msg['Name'] + " bereit!")
         Maschinenname = msg['Name']
         name = Maschinenname + "_DT" + ".py"
         path = "DTS/" + name
         shutil.copyfile("Dummy_DT.py", path)

         """Tatsächlichen Maschinenname in DT Script schreiben"""
         # input file
         fin = open("Dummy_DT.py", "rt")
         # output file to write the result to
         fout = open(path, "wt")
         # for each line in the input file
         for line in fin:
             # read replace the string and write to output file
             fout.write(line.replace("Maschinenname = Dummy_DT", "Maschinenname = " + Maschinenname))

         print(exec(open(path).read()))
         print("Ich habe DT mit dem Namen " + msg['Name'] + " bereit gestellt!")
         #subprocess.Popen(name, shell=True)
         # subprocess.Popen([sys.executable, name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #
    # else:
    #     print ("DT existiert bereits")


client = mqtt.Client()
client.username_pw_set(_username, _passwd)
client.on_connect = on_connect
client.on_message = on_message
client.connect(_host, _port, _timeout)

# Payload=json.dumps({"Maschine-17": "Erstelle DT"})
# topic = "Laufumgebung"
# client.publish(topic, Payload)


client.loop_forever()