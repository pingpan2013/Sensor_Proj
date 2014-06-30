#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# DESC:
# Get data from the ds1820 temperature sensor, if exception happens
# it will return False
#
# DATE:
# 06/06/2014
#

import os
import sys
from time import sleep
from ds18b20 import DS18B20

def get_temp_data():
    '''Load the deviece'''
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    
    try:        
        sensor = DS18B20()
        while True:
            temperatures = sensor.get_temperatures([DS18B20.DEGREES_C, DS18B20.DEGREES_F, DS18B20.KELVIN])
            print "Kelvin: %f" % temperatures[2]
            print "Degrees Celsius: %f" % temperatures[0]
            print "Degrees Fahrenheit: %f" % temperatures[1]
            print "====================================="
            sleep(1)
    except:
        print "Exception Happened: ", sys.exc_info()[0]
        return False


def get_mult_temp_data():
    '''Load the deviece'''
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    
    sensors = []
    temps = []

    try:        
        sensor = DS18B20()
        while True:
            for sensor_id in DS18B20.get_available_sensors():
                sensors.append(DS18B20(sensor_id))
            
            i = 0;
            for sensor in sensors:
                temps[i] = sensor.get_temperature(DS18B20.DEGREES_F) 
                print "Sensor {0} : {1}".format(sensor.get_id(), temps[i])
                i++
                
            sleep(1)
    except:
        print "Exception Happened: ", sys.exc_info()[0]
        return False


if __name__ == "__main__":

    if get_temp_data() == False:
        print "Move On >>>>>"
