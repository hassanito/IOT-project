import paho.mqtt.client as mqtt
import json,schedule,datetime,pytz,time

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #previously #
    client.subscribe("gateway/7276ff000b03008c/event/number")

# The callback for when a PUBLISH message is received from the server.s
def on_message(client, userdata, msg):
    from .models import Professor,ApptRequests,Student
    from .views import send_presence_mail,send_absence_mail
    print(msg.topic+" "+str(msg.payload))
    messages.append(msg.payload)
    j = json.loads(msg.payload)
    #overhere I have to update this with the working topic and data content in json -test with the actual device

    professor_name = j['Professor']
    pr = Professor.objects.get(professor=professor_name)
    state = j['State']
    print("previous state is "+str(state))
    print("previous in office is "+str(pr.in_office))
    #when a message is received we check if the previous state saved in the database and the state from the bottom are different which means the
    #has left or came so we send an email in this CASCADE
    #state =1 implies professor.in_office = True
    #state =0 implies professor.in_office = False

    if(pr.in_office == False and state ==1):
        pr.in_office =True
        pr.save()
        print("SEND MAILS")
        #goes over all the subscribers of this professor and sends an email of his current stat that changed
        for i in ApptRequests.objects.filter(professor=pr):
            print("SENDING MAILS")
            current_student = i.student

            #print(current_student.student.email)
            send_presence_mail(i.get_time,current_student,pr)

    elif(pr.in_office == True and state ==0):
        pr.in_office =False
        pr.save()
        #goes over all the subscribers of this professor and sends an email of his current stat that changed
        for i in ApptRequests.objects.filter(professor=pr):
            print("SENDING MAILS OFF")
            current_student = i.student
            send_absence_mail(i.get_time,current_student,pr)
    print("current in office is "+str(pr.in_office))


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
