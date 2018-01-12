import json
import pytz
from time import sleep
from datetime import date, datetime
from random import randint
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("123afhlss456")					#This is just an ID so that the MQTT broker can identify the client, using any random string will do.
myMQTTClient.configureEndpoint("a375a74rjdbru6.iot.us-west-2.amazonaws.com", 8883)			#this is the unique thing endpoint with the .503 certificate
# giovanni
myMQTTClient.configureCredentials("aws-iot-device-sdk-python/deviceSDK/certs/VeriSign-Class 3-Public-Primary-Certification-Authority-G5.pem.txt", "aws-iot-device-sdk-python/deviceSDK/certs/9e6528d5bc-private.pem.key", "aws-iot-device-sdk-python/deviceSDK/certs/9e6528d5bc-certificate.pem.crt")
# michael
myMQTTClient.configureCredentials(
    "aws-iot-device-sdk-python/deviceSDK/certs/VeriSign-Class3-Public-Primary-Certification-Authority-G5.pem.txt",
    "aws-iot-device-sdk-python/deviceSDK/certs/24535dbd29-private.pem.key",
    "aws-iot-device-sdk-python/deviceSDK/certs/24535dbd29-certificate.pem.crt")
#above has the path for the CA root cert, private key cert, and device cert
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

#connect and publish
myMQTTClient.connect()
myMQTTClient.publish("thing01/info", "connected", 0)

date = datetime.now(tz=pytz.utc)
# date = date.astimezone(timezone('US/Pacific'))
now_str = date.strftime('%m/%d/%Y %H:%M:%S %Z')

payload = {
    'plant_type': {"S": 'default'},
    'datetime': {"S": now_str},
    'location': {"S": 'default'},
    'temp': {"S": '0'},
    'humid': {"S": '0'},
    'light': {"S": '0'}
    }

def rand_sensor_data():
    print('randomizing sensor data')
    for each in payload:
        each = random.randint(1, 51)
        print('complete')

try:
    rand_sensor_data()
    print(payload)
    msg = json.dumps(payload)
    print(msg)
    myMQTTClient.publish("thing01/data", msg, 0)
    sleep(5)
except KeyboardInterrupt:
    GPIO.cleanup()
    print('exited')
