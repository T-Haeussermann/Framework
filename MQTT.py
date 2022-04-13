import time
import paho.mqtt.client
import paho.mqtt.client as mqtt
from queue import Queue

class MQTT:
    def __init__(self, _username, _passwd, _host, _port, Topic_Sub):
        self._username = _username
        self._passwd = _passwd
        self._host = _host
        self._port = _port
        self.Topic_Sub = Topic_Sub
        self._timeout = 60
        self.client = mqtt.Client()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        self.client.subscribe(self.Topic_Sub)

    def publish(self, Topic, Payload):
        self.client.publish(Topic, Payload)
        print("message published")

    def on_message(self, client, userdata, msg):
        TopicUndNachricht = msg.topic + " : " + str(msg.payload.decode("utf-8"))  # string
        Nachricht = str(msg.payload.decode("utf-8")) # übergibt nur reinen String. Muss in json gewanderlt werden json.loads()
        Q_in.put(Nachricht)
        print(TopicUndNachricht)
        return TopicUndNachricht

    def run(self):
        self.client.username_pw_set(self._username, self._passwd)
        self.client.on_connect = self.on_connect
        self.client.loop_start()
        self.client.on_message = self.on_message
        self.client.connect(self._host, self._port, self._timeout)
        #self.client.loop_forever()
        #self.client.loop_stop()



if __name__ == '__main__':
    Q_in = Queue ()
    test = MQTT("dbt", "dbt", "mq.jreichwald.de", 1883, "Laufzeitumgebung/#")
    test.run()


while True:
    time.sleep(2)
    test.publish("Hallo", "lol")



