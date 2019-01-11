#!/usr/bin/python

import time
import paho.mqtt.client as mqtt
import json
import time
import sys
import ssl
import RPi.GPIO as GPIO

feeder = 11


GPIO.setmode(GPIO.BOARD)

GPIO.setup(feeder, GPIO.OUT)

cert_path = "/home/pi/Desktop/certs/"
host = "xxxxxxxxxxxxxx-ats.iot.us-east-1.amazonaws.com"
topic = "$aws/things/aquarium/shadow/update"
root_cert = cert_path + "AmazonRootCA1.key"
cert_file = cert_path + "cert.pem.crt"
key_file = cert_path + "private.pem.key"

globalmessage = ""  # to send status back to MQTT
isConnected = False


def feedcommand(data):  # {"name":"FeedIntent","slots":{"Task":{"name":"Task","value":"feed the fish"}}}
    task = str(data["slots"]["Task"]["value"])
    global globalmessage

    if task in ["feed the fish", "feed my fish", "feed fish", "feed"]:
        globalmessage = "now fish is happy"
        print (globalmessage)
        toggle(feeder)


def toggle(gpio):

    p = GPIO.PWM(11, 50)
    p.start(12.5)
    count = 0
    try:
        while count <= 1:
            p.ChangeDutyCycle(12.5)
            time.sleep(1)
            p.ChangeDutyCycle(2.5)
            time.sleep(1)
            count += 1
    except KeyboardInterrupt:

        p.stop()
        GPIO.cleanup()
  #  GPIO.output(gpio, cmd)   call servo motor

# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
    isConnected = True
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    data = json.loads(str(msg.payload))
    # INTENT
    if "name" in data:
        if data["name"] == "FeedIntent":
            feedcommand(data)


client = mqtt.Client(client_id="aquarium.py")
client.on_connect = on_connect
client.on_message = on_message
#client.on_log = on_log
client.tls_set(root_cert,
               certfile=cert_file,
               keyfile=key_file,
               cert_reqs=ssl.CERT_REQUIRED,
               tls_version=ssl.PROTOCOL_TLSv1_2,
               ciphers=None)

client.connect(host, 8883, 60)

run = True

try:
    while run:
        client.loop()
        time.sleep(1)

        try:
            mypayload = '''{
                "StatusMessage": "%s"
            }''' % (globalmessage)

            if globalmessage != "":
                client.publish(topic, mypayload)
                globalmessage = ""

        except (TypeError):
            pass

except KeyboardInterrupt:
    print ("Thank you for using my program. Take Care Bye Bye!")
    GPIO.cleanup()
