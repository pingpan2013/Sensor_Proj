#!/usr/bin/python

#
# File Name: humi_sensor.py
# Desc: The humidity sensor module which is responsible for getting the 
#       humidity and temperature data from the sensor
#

import subprocess
import re
import time

def get_humidity_and_temp(): 
    '''
    Get humidity and temperature data from sensors
    '''
    output = subprocess.check_output(["./adafruit_dht.py", "2302", "17"]);
    
    matches = re.search("Temp =\s+([0-9.]+)", output)
    if (not matches):
        time.sleep(3)
    
    temp = float(matches.group(1))
    temp_f = temp * 9.0 / 5.0 + 32.0 # converts temp to F
    
    # search for humidity printout
    matches = re.search("Hum =\s+([0-9.]+)", output)
    if (not matches):
        time.sleep(3)
    
    humidity = float(matches.group(1))
   
    return (humidity, temp_f)
