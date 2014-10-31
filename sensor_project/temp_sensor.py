#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# DESC:
# Get data from the ds1820 external temperature sensor
#
# DATE:
# 10/3/2014
#

import os
import sys
from time import sleep
from ds18b20 import DS18B20

def get_temp_data_f():
    '''Get temperature data in Fahrenheit''' 
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    
    sensors = []
    temps = []

    sensor = DS18B20()
    for sensor_id in DS18B20.get_available_sensors():
        sensors.append(DS18B20(sensor_id))
    
    for sensor in sensors:
        temps.append(sensor.get_temperature(DS18B20.DEGREES_F))
    return temps