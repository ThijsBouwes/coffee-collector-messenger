from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from Services import slack
import logging
import time

# Config AWSIoTMQTT
host = os.getenv('HOST')
rootCAPath = os.getenv('ROOT_CA_PATH')
certificatePath = os.getenv('CERTIFICATE_PATH')
privateKeyPath = os.getenv('PRIVATE_KEY_PATH')

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

# Callback
def ccSensorCallback(client, userdata, message):
    print"Received a new message: "
    print message.payload
    print "from topic: "
    print message.topic;
    print "--------------\n\n"
    slack.message(message.payload)

def publish(Reading):
    MQTTClient.publish("ccSensor", Reading, 1)

# Connect and subscribe to AWS IoT

MQTTClient.connect();
MQTTClient.subscribe("ccSensor", 1, ccSensorCallback)
