import requests
import json
import time
import os
import logging
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# Config AWSIoTMQTT
host = os.getenv('HOST')
rootCAPath = os.getenv('ROOT_CA_PATH')
certificatePath = os.getenv('CERTIFICATE_PATH')
privateKeyPath = os.getenv('PRIVATE_KEY_PATH')

def sendSlackMessage(value):
    url = os.getenv('SLACK_API')
    payload =  {"text": "The current level of CC is: %s cm left %s" % (value, getEmoticon(value))}
    return requests.post(url, data=json.dumps(payload))

def getEmoticon(level):
	level = int(level)
	if level > 50:
		return ":grinning:"
	elif level <= 50 and level > 15:
		return ":slightly_smiling_face:"
    elif level <= 15 and level > 5:
        return ":cold_sweat:"
	else:
		return ":scream:"

def ccSensorCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	print("from topic: %s")
	print(message.topic);
	print("--------------\n\n")
	sendSlackMessage(message.payload)

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
MQTTClient = AWSIoTMQTTClient("CC")
MQTTClient.configureEndpoint(host, 8883)
MQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
MQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
MQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
MQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
MQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
MQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
MQTTClient.connect();
MQTTClient.subscribe("ccSensor", 1, ccSensorCallback)
# MQTTClient.publish("ccSensor", 56, 0)
time.sleep(2)

# Run the programm
while True:
   time.sleep(1)
