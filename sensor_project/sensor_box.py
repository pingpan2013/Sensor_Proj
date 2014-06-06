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
import urllib2    # Used to test if internet is available
import RPi.GPIO as GPIO
import conf

def control_light(ifEnd):
    '''
    At the begining, ifEnd = False:
        Check the temperature, if it is below 34, trun on the light
    At the end, ifEnd = True:
        Turn off the light
    '''
    GPIO.setmode(GPIO.BCM) 
    GPIO.setup(conf.pin_number,GPIO.OUT)
    
    if ifEnd == True:
        GPIO.output(conf.pin_number, False)
    #elif read_temp() < 34:                   # If temperature is below 34 
    elif 30 < 34: 
        GPIO.output(conf.pin_number, True)    # Turn on the light bulb on to warm up the computer
    else:                                     # Else turn off 
        GPIO.output(conf.pin_number, False)

def restart():
    '''
    Restart the PI
    '''
    command = '/usr/bin/sudo /sbin/shutdown -r now'
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]


def internet_on():
    '''
    Test if internet access is available
    Return true if available, otherwise return false
    '''
    try:
        response = urllib2.urlopen('http://74.125.228.100', timeout=1)
        print 'Internet is On!'
        return True
    except urllib2.URLError as err: pass
    return False

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
    control_light(False)
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y_%m_%d_%H_%M_%S')
    filename  = str(timestamp) + '.jpg'     
       
    # SETP 1: Get all data from sensors
    humidity, temp_f = get_humidity_and_temp()          # Get humidity and temperature
    moistureA, moistureB, moistureC = get_moisture()    # Get moisture

    ### The following parts are used to debug  ###
    print 'Took picture ' + timestamp		
    print "Humidity:    %.1f %%" % humidity
    print "Internal Temperature: %.1f F" % temp_f
    print "Moisture A = " + str(moistureA)
    print "Moisture B = " + str(moistureB)
    print "Moisture C = " + str(moistureC)
    print 'uploaded picture ' + timestamp

    # STEP 2: Store data locally
    os.system('raspistill -o ' + conf.pi_folder_1 + filename)
    text_file = open("/home/pi/Desktop/parjana_data.txt", "a")
    text_file.write("PI_id: %s"%conf.PI_id 
                    + ", Internal Temp: %s"%temp_f 
                    + ", Internal Humidity: %s"%humidity 
                    + ", Moisture A: %s"%moistureA 
                    + ", Moisture B: %s"%moistureB 
                    + ", Moisture C: %s"%moistureC
                    + ", Time: %s"%timestamp + ", Test Site 2" + '\n')
    text_file.close()
        
    # STEP 3: Send data to the server and database if Internet is available
    if internet_on():
        store_data_to_ftp(filename)  # store pictures to FTP server
        store_data_to_db(temp_f, humidity, moistureA, moistureB, moistureC)
    
    # STEP 4: Turn off the light and then restart PI
    control_light(True)
    time.sleep(conf.period)
    os.system('sudo reboot')


if __name__ == '__main__':

    main()

