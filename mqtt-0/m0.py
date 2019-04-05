import sys
import time
import paho.mqtt.client as paho

from __cf import C

#broker = "iot.eclipse.org"
broker = C.broker
client_id = 'mai-0'

if len(sys.argv) > 1:
  client_id = sys.argv[1]

def on_message(client, userdata, message):
  print('received message =', str(message.payload.decode('utf-8')))

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

client = paho.Client(client_id)
client.on_message = on_message
client.on_connect = on_connect

if ('app_id' in C):
  client.username_pw_set(username=C.app_id, password=C.secret)

print("connecting to broker:%s" % broker)
client.connect(broker)
client.loop_start()
client.subscribe("house/bulb1")
time.sleep(2)
print("sending...")
for i in range(200):
  client.publish("house/bulb1", "on-%d-from-%s" % (i, client_id))
print("out...")
time.sleep(100)
client.disconnect()
client.loop_stop()
