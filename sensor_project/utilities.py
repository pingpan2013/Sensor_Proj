#!/usr/bin/python

#
# File Name: utilities.py
#
# Desc:
# Control the sensor to get humidity and moisture infomation
# If internet is down, store the result into local files
# else send the data to the database
#

import ftplib
import os
import time      
import datetime
import glob
import sys
import urllib2    # Used to test if internet is available
import urllib
import tempfile
import re
import glob

import subprocess
from subprocess import call
import conf.py

##### Connection interface with MySQL ######
import MySQLdb

##### Sensor lib ######
import spidev 
import RPi.GPIO as GPIO

# Open temperature sensors
spi = spidev.SpiDev()
spi.open(0, 0)


#########################################
####### Utility functions ###############
#########################################
def check_moisture(adcnum):
    '''
    Read moisture from pins
    '''
    if((adcnum > 7) or (adcnum < 0)):
        print 'Wrong pin number'
        return -1
    
    r = spi.xfer2([1, (8 + adcnum)<<4, 0])
    adcout = ((r[1]&3) << 8) + r[2]
    return adcout
    

def researt():
    '''
    Restart the PC after certain perriod
    '''
    ###### TODO

def internet_on():
    '''
    Test if internet access is available
    Return true if available, otherwise return false
    '''
    try:
        response = urllib2.urlopen('http://74.125.228.100', timeout=1)
        return True
    except urlib2.URLError as err: pass
    return False



def process_and_store_online():
    '''
    Process and store data if internet is available
    '''
    while(True):
                



def process_and_store_locally():
    '''
    Process and store data locally if internet is not available
    '''
    while(True):
        # Use the current time as the file name
        now = datetime.datetime.now()
        timestamp = now.strftime('%Y_%m_%d_%H_%M_%S')
        filename  = str(timestamp) + '.jpg'
        
        # Read data from humidity sensor
        # For more details about the APIs of the sensor, refer to:
        # learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/overview
        P = subprocess.Popen('./Adafruit_DHT')
        output = subprocess.check_output(['./Adafruit_DHT', '2302', str(humidity_pinA),]
        # TODO 
        
        humidity = 1;
        temp_f = 1;

        # The following parts are used to debug
        if(__debug__):
            print 'took picture ' + timestamp		
	    print "Humidity:    %.1f %%" % humidity
	    print "Internal Temperature: %.1f F" % temp_f
	    print "Moisture A = " + str(check_moisture(moisture_pinA))
	    print "Moisture B = " + str(check_moisture(moisture_pinB))
	    print "Moisture C = " + str(check_moisture(moisture_pinC))
	    print 'uploaded picture ' + timestamp

        # Create text file to store data locally
        text_file = open("/home/pi/Desktop/parjana_data.txt", "a")
        text_file.write("PI_id: %s"%PI_id + ",  Internal Temp: %s"%temp_f + ", Internal Humidity: %s"%humidity 
                        + ", Moisture A: %s"%check_moisture(moisture_pinA) + ", Moisture B: %s"%check_moisture(moisture_pinB) 
                        + ", Moisture C: %s"%check_moisture(moisture_pinC) + ", Time: %s"%timestamp + ", Test Site 2" + '\n')
        text_file.close()
        
        # Wait for some time to begin the next collection
        time.sleep(timedelay_2)
        

def get_data():
    '''
    Get the necessary data, the way to store it depends on whether the Internet access is available:
    if available, send the data to the server
    if not, store the data locally
    '''
    if(internet_on()):
        process_and_store_online()
    else:
        process_and_store_locally()




















