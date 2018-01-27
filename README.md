# Environmental Visual Examiner (EVE)
***College of the Canyons Association of Computing Machinery Research Project***

View our [**project abstraction**](https://docs.google.com/document/d/1yDm8ZhQO4J5V0nz4npQUcugwjEzfE0l4rJVBd1Fd8Nk/edit?usp=sharing) for a summary of how this system should work. To view more of the research completed so far, view our [**google drive**](https://drive.google.com/drive/folders/0B4uU1kLqkZiAc2NfbnluOFQxalk?usp=sharing)

## Design
This configuration is using AWS IoT, DynamoDB, and Lambda services from AWS. A pre-defined **eve_user** table in DynamoDB holds information about the user's garden plot for querying. An MQTT client is setup through AWS IoT to subscribe and publish from/to the raspberry pi at scheduled intervals using configuration details from [sensor_reader.py](https://github.com/cocacm/eve-pi/blob/master/sensor_reader.py) (certification must be created and linked to the pi using the topic **thing01/data**). A rule is then used to insert published sensor values into our DynamoDB **eve_data** table.

From DynamoDB, our [water_alg](https://github.com/cocacm/eve-aws/tree/master/water_alg) Lambda function is triggered, which requests eto from the CIMIS API, queries the plant factor from our **eve_pf** table, and calculates whether watering is required. The results are then written back to the same item in our **eve_data** table. Lasty, an MQTT message is published back to the pi with watering instructions, which are then executed.

## Configuration
[**help.txt**](https://github.com/cocacm/eve-pi/blob/master/help.txt) contains some useful linux commands for navigating the pi via ssh connection. All configuration is done using ssh. *DO NOT* push to this repository from the pi itself as this requires configuring user credentials for the pi, save out changes to your local computer and push from there. The pi will be setup to automatically pull from the repository once a day when deployed.

View the [**configs.txt**](https://github.com/cocacm/eve-pi/blob/master/configs/config.txt) from this repository to see configuration for pi hardware so far (any changes to hardware *MUST* be added to this file).

The [**wpa_supplicant.conf**](https://github.com/cocacm/eve-pi/blob/master/configs/wpa_supplicant.conf) contains the information for configuring wifi connection on the pi.

[**crontab.txt**](https://github.com/cocacm/eve-pi/blob/master/crontab.txt) is used for scheduling execution of the [**sensor_reader.py**](https://github.com/cocacm/eve-pi/blob/master/sensor_reader.py) script. To edit cron jobs, run `crontab -e` and select nano as your editor. Then insert the line from [**crontab.txt**](https://github.com/cocacm/eve-pi/blob/master/crontab.txt) and save.
