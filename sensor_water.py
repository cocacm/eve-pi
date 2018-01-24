from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
# import boto3

# use MQTT sub to receive instructions from AWS
# use conditions statements to determine whether to water

def water_plot(water_amt):
    return '...plot watered {} gallons'.format(water_amt)

# query 'water_alg' from latest 'eve_main' item
# query 'data' attribute from 'eve_main'

# calculate conditons, determine if watering is required
# if watering is required invoke watering function
# if waterMoisture < 3 & waterReserveForPlot > 1:
#     print ("the plot will be watered")
#     willWater = True
# else:
#     print ("the plot will not be watered")
#     willWater = False

# call 'water_plot()' with the amount to water as a parameter

print(water_plot('0.5'))
