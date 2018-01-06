import RPi.GPIO as GPIO
import Adafruit_DHT
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from datetime import date, datetime
# pin definitions
dht_pin = 4      # BOARD 7
prc_pin = 11     # BCM 17
button_pin = 13  # BCM 27

# pin setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(prc_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("123afhlss456")					#This is just an ID so that the MQTT broker can identify the client, using any random string will do.
myMQTTClient.configureEndpoint("a375a74rjdbru6.iot.us-west-2.amazonaws.com", 8883)			#this is the unique thing endpoint with the .503 certificate
myMQTTClient.configureCredentials("aws-iot-device-sdk-python/deviceSDK/certs/VeriSign-Class 3-Public-Primary-Certification-Authority-G5.pem.txt", "aws-iot-device-sdk-python/deviceSDK/certs/9e6528d5bc-private.pem.key", "aws-iot-device-sdk-python/deviceSDK/certs/9e6528d5bc-certificate.pem.crt")
#above has the path for the CA root cert, private key cert, and device cert
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

#connect and publish
myMQTTClient.connect()
myMQTTClient.publish("thing01/info", "connected", 0)							#topic, message, time

#sensor data
def get_sensor_data():
	print('getting sensor data')
	humid, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, dht_pin)
	light = prc_time(prc_pin)
	print('complete')
	fahr = int(temp * (9.0 / 5.0) + 32)
	print('humid. = {}%, temp. = {}F, light = {}'.format(humid, fahr, light))

def prc_time(pin):
	light = 0
	GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
	sleep(0.1)

	GPIO.setup(pin, GPIO.IN)
	while (GPIO.input(pin) == GPIO.LOW):
		light += 1
	return light

try:
	while True:
		if GPIO.input(button_pin):
			date = datetime.now(tz=pytz.utc)
			date = date.astimezone(timezone('US/Pacific'))
			now_str = date.strftime('%m/%d/%Y %H:%M:%S %Z')
			result = get_sensor_data()
			payload = '{"timestamp": "' + now_str + '", "temperature": ' + str(result.fahr) + ', "humidity": ' + str(result.humid) + '}'
			print(payload)
			myMQTTClient.Publish("thing01/data", payload, 0)
			sleep(5)
		else:
			print(".")
			sleep(1)
except KeyboardInterrupt:
	GPIO.cleanup()
	print('exiting')
