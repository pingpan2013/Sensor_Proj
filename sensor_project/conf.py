#!/usr/bin/python

#
# File Name: conf.py
# 
# Desc:
# The configuration information about the database and some other stuff
#

import logging

#===================================================
#     SensorBox software version information 
#===================================================
sensorbox_version = "v1.1.2"

#===================================================
#     Sensor configuration information 
#===================================================
PI_id = 7 # ID of computer
using_camera = False
num_moisture_sensors = 3
num_temp_sensors = 0
using_humidity_sensor = False
using_water_level_sensor = False
water_level_slope = -0.0232162397183
water_level_yintercept = 62.5863911235
water_level_interval = 1
# Real-world location for storage in database
location = "Test Site"
# Upload information
table_name = 'Test_' + str(PI_id)
ftp_name = '/Test/' + str(PI_id) + '/'
# Units information
temperature_units = "Fahrenheit"
precision = 2

#==================================================
#     Local directories for storing the results 
#==================================================
home = '/home/pi/'
desktop = home + 'Desktop/'
csv_filename = "sensorbox" + str(PI_id) + "_data.csv"
# The directory for storing the results if the internet is on
online_pictures_folder = desktop + 'pictures_online/'
# The directory for storing the results if the internet is down
offline_pictures_folder = desktop + 'pictures_offline/'
# USB saving directory
usb_folder = '/media/PARJANA03_/'

#===================================================
#     The hardware interface information 
#===================================================
sc_port = '/dev/ttyACM0'
sc_baud = 115200

#===================================================
#    The time (in seconds) between two collections 
#===================================================
period = 600

#===================================================
#     Database and FTP Server Information 
#===================================================

DB = {
    'host' : '198.57.219.221', 
    'user' : 'theparja_georgeg',
    'password' : 'ggrzywacz2190',
    'database' : 'theparja_NADF',
    'table' : table_name
}

FTP_Server = { 
    'host' : '198.57.219.221',
    'user' : 'data@theparjanadistribution.com',
    'password' : 'Parjana1247',
    'ftp_folder' : ftp_name
}

#==================================================
#     Log configuration for debugging
#==================================================
# log_level controls which log messages will be recorded
# See https://docs.python.org/2/howto/logging.html for more information
log_level = logging.WARNING
log_name = 'sensorbox.log'
previous_log_name = 'sensorbox_previous.log'
log_path = desktop + log_name
previous_log_path = desktop + previous_log_name
