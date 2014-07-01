#!/usr/bin/python

#
# File Name: utilities.py
#
# Desc:
# Control the sensor to get humidity and moisture infomation
# If internet is down, store the result into local files
# else send the data to the database
#
# Date: May 22nd, 2014
#

import os
import time      
import datetime
import glob
import sys
import subprocess

import RPi.GPIO as GPIO
import conf
import server_conn
import mois_sensor
import humi_sensor
import curr_sensor
import temp_sensor

GPIO.setwarnings(False)

def main():
    '''
    The main process of this project:
    1. Get the necessary data from sensors, including humidity/moisture/temperature 
    2. Store the data locally 
    3. Check if Internet is available. If available, send the data to the server
    4. Restart PI and then eepeat from 1
    '''
    # Some preparation work:
    # 1)Check temperature to decide if we need open bulbs
    # 2)Get current time as the new file name
    conf.control_LED(25, True)
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y_%m_%d_%H_%M_%S')
    filename  = str(timestamp) + '.jpg'     
    
    # SETP 1: Get all data from sensors
    humidity, temp_f = humi_sensor.get_humidity_and_temp()          # Get humidity and temperature
    moistureA, moistureB, moistureC = mois_sensor.get_moisture()    # Get moisture

    ### The following parts are used to debug  ###
    print 'Took picture ' + timestamp		
    print "Humidity:    %.1f %%" % humidity
    print "Internal Temperature: %.1f F" % temp_f
    print "Moisture A = " + str(moistureA)
    print "Moisture B = " + str(moistureB)
    print "Moisture C = " + str(moistureC)

    # STEP 2: Store data locally
    #os.system('raspistill -o ' + conf.pi_folder_1 + filename)
    subprocess.call(['raspistill', '-o', '{0}{1}'.format(conf.pi_folder_1,filename)])
    text_file = open("/home/pi/Desktop/parjana_data.txt", "a")
    text_file.write("PI_id: %s"%conf.PI_id 
                + ", Internal Temp: %s"%temp_f 
                + ", Internal Humidity: %s"%humidity 
                + ", Moisture A: %s"%moistureA 
                + ", Moisture B: %s"%moistureB 
                + ", Moisture C: %s"%moistureC
    
    print 'Waiting for internet reconfiguration .... '
    time.sleep(conf.period/2)
    
    # STEP 3: Send data to the server and database if Internet is available
    if server_conn.internet_on() == True:
        conf.control_LED(23, True)
        server_conn.store_data_to_ftp(filename)  # store pictures to FTP server
        server_conn.store_data_to_db(temp_f, humidity, moistureA, moistureB, moistureC)
        os.system("rm -f " + conf.pi_folder_1 + '*')
    else:
        print 'Internet is off'
    
    # STEP 4: Turn off the light and then restart PI
    print 'Rebooting ...'
    time.sleep(conf.period/2)
    conf.control_LED(23, False)
    conf.control_LED(25, False)
    subprocess.call(['sudo', 'reboot'])

if __name__ == '__main__':

    server_conn.check_folder("./")
