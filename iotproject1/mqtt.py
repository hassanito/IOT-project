import paho.mqtt.client as mqtt
import json
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #previously #
    client.subscribe("gateway/7276ff000b03008c/event/number")

# The callback for when a PUBLISH message is received from the server.s
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    messages.append(msg.payload)
    j = json.loads(msg.payload)
    print(j)
    if(j==1):
        print("BON")
    else:
        print("BATATA")
    if(j['applicationID']=='19'):
        if(j["deviceName"]=="IoT-G3"):
            state = j['object']['payload']
            print('STATE = '+state)



def on_publish(mqttc, userdata, mid):
    print("Published")

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

messages = []

client.username_pw_set("user","bonjour")

client.connect("212.98.137.194", 1883)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
