import json
import paho.mqtt.client as mqtt
from queue import Queue

class MQTT:
    def __init__(self, _username, _passwd, _host, _port, _topic_sub):
        self._username = _username
        self._passwd = _passwd
        self._host = _host
        self._port = _port
        self._topic_Sub = _topic_sub
        self.Q = Queue()
        self._timeout = 60
        self.client = mqtt.Client()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        self.client.subscribe(self._topic_Sub)

    def publish(self, Topic, Payload):
        self.client.publish(Topic, Payload)
        print("message published")

    def on_message(self, client, userdata, msg):
        Topic = msg.topic
        Nachricht = str(msg.payload.decode("utf-8"))
        TopicUndNachricht = json.dumps({"Topic": Topic, "Nachricht": Nachricht})
        self.Q.put(TopicUndNachricht)

    def run(self):
        self.client.username_pw_set(self._username, self._passwd)
        self.client.on_connect = self.on_connect
        self.client.loop_start()
        self.client.on_message = self.on_message
        self.client.connect(self._host, self._port, self._timeout)
        #self.client.loop_forever()
        #self.client.loop_stop()



