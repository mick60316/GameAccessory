# Inspired and modified from https://github.com/CloudMQTT/python-mqtt-example
import os
import configparser
from urllib.parse import urlparse
import paho.mqtt.client as mqtt
import socket
import sys
import getopt
import threading
import random

AppPort = 50052
LocalIp ='localhost'

updSocket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
common =[]
common.append("MUSIC")
common.append("NETFLIX")
common.append("YES")
common.append("MOD")






#LocalAddress
client = mqtt.Client()
# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))

def on_message(client, obj, msg):

    #print (type(LocalIp),type(AppPort))
    address = (LocalIp,AppPort)
    msgString =str(msg.payload,encoding='utf8')
    updSocket.sendto(msg.payload,address)
    print("Get Message "+msgString)
   
   

def on_publish(client, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, obj, level, string): 
    print(string)

def Mqtt_Setup() :
    # Assign event callbacks
    client.on_message = on_message
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe

    # Uncomment to enable debug messages
    #client.on_log = on_log

    # Get CLOUDMQTT settings from config.ini 
    CONFIG = configparser.ConfigParser()
    CONFIG.read('config.ini')
    CONFIG_MQTT = CONFIG['Cloudmqtt']
    TOPIC = CONFIG_MQTT['TOPIC']
    FIRST_MESSAGE = CONFIG_MQTT['MESSAGE']


    # Connect
    client.username_pw_set(CONFIG_MQTT['USER'], CONFIG_MQTT['PASSWORD'])
    client.connect(CONFIG_MQTT['CLOUDMQTT_URL'], int(CONFIG_MQTT['PORT']))

    # Start subscribe, with QoS level 0
    client.subscribe(TOPIC, 0)
    global timer
    timer.start()
    # Publish a message
    client.publish(TOPIC, FIRST_MESSAGE)

    # Continue the network loop, exit when an error occurs
    rc = 0
    while rc == 0:
        rc = client.loop()
    print("rc: " + str(rc))

def SystemArguments ():
    global LocalIp
    global AppPort
    argv =sys.argv[1:]
    try:
        opts,args =getopt.getopt(argv,"hi:p:",['help','ip=','port='])
    except getopt.GetoptError:
        return

    for opt,arg in opts:
        if opt in ("-h",'--help'):
            print('-----------------------------------------------------------------')
            print('Help: ')
        
            print('MqttService.py -i <LocalIp> -p <AppPort>')
            print('or: MqttService.py --ip=<LocalIp> --port=<AppPort>')
            print('-----------------------------------------------------------------')
            sys.exit()
        elif opt in ('-i','--ip'):
            LocalIp =arg
            print('Set IP = ',arg)
        elif opt in ('-p','--port'):
            AppPort =int(arg)
            print('Set Port = ',arg)
def MqttTestTimer():
    index =random.randint(0,3)
    print("Timer Click Message = ", common[index])
    client.publish("smartdisplay", common[index])
    global timer
    timer = threading.Timer(15, MqttTestTimer)
    timer.start()

timer =threading.Timer (15,MqttTestTimer)

    

if __name__=='__main__':
    #print(common[3])
    SystemArguments()
    Mqtt_Setup()
    
