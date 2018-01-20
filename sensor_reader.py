import RPi.GPIO as GPIO
import Adafruit_DHT
import json
import pytz
from time import sleep
from datetime import date, datetime
from random import randint
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# pin definitions
dht_pin = 4      # BOARD 7
prc_pin = 11     # BCM 17
button_pin = 13  # BCM 27

# pin setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(prc_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# AWS IoT certificate based connection
# MQQT client is an ID so that the MQTT broker can identify the client, using
# any random string will do.
myMQTTClient = AWSIoTMQTTClient("123afhlss456")
# this is the unique thing endpoint with the .503 certificate
myMQTTClient.configureEndpoint("a375a74rjdbru6.iot.us-west-2.amazonaws.com", 8883)
# giovanni
myMQTTClient.configureCredentials(
    "aws-iot-device-sdk-python/deviceSDK/certs/VeriSign-Class3-Public-Primary-Certification-Authority-G5.pem.txt",
    "aws-iot-device-sdk-python/deviceSDK/certs/9e6528d5bc-private.pem.key",
    "aws-iot-device-sdk-python/deviceSDK/certs/9e6528d5bc-certificate.pem.crt")
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

date = datetime.now(tz=pytz.utc)
date = date.astimezone(timezone('US/Pacific'))
now_str = date.strftime('%Y-%m-%d %H:%M:%S %Z')

# ping device for location
location = 'Valencia, Ca'
payload = {
    'plant_type': 'vegetable',
    'date_time': now_str,
    'location': location,
    'temp': 0.0,
    'humid': 0.0,
    'light': 0.0
    }

def get_sensor_data():
	print('getting sensor data')
	payload['humid'], payload['temp'] = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, dht_pin)
	payload['light'] = prc_time(prc_pin)
    # fahr = int(temp * (9.0 / 5.0) + 32)
	print('complete')

def prc_time(pin):
    # photoresistor cell sensor data
	light = 0
	GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
	sleep(0.1)  # 1 microsecond

	GPIO.setup(pin, GPIO.IN)
	while (GPIO.input(pin) == GPIO.LOW):
		light += 1
	return light

try:
    rand_sensor_data()
    print(payload)
    msg = payload.json()
    print(msg)
    myMQTTClient.Publish("thing01/data", payload, 0)
    sleep(5)
except KeyboardInterrupt:
	GPIO.cleanup()
	print('exiting')
