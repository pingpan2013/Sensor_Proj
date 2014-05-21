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


#####################################################################
######################## Utility functions ##########################
#####################################################################
def check_temperature():
    '''
    Check the temperature, if it is above 34, it won't
    trun on the light bulbs
    '''
    GPIO.setmode(GPIO.BCM) 
    GPIO.setup(pin_number,GPIO.OUT)
    
    if read_temp() < 34:                # If temperature is below 34 
        GPIO.output(pin_number,True)    # Turn on the light bulb on to warm up the computer
    else:                               # Else turn off 
        GPIO.output(pin_number,False)

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
        return True
    except urlib2.URLError as err: pass
    return False


def connect_db():
    '''
    Build connection to the given database
    '''
    conn = MySQLdb.connect(conf.DB['host'],
                           conf.DB['user'],
                           conf.DB['password'],
                           conf.DB['database'])
    return conn


def store_data_to_ftp(filename):
    '''
    Connect to the FTP server, and then store the pictures 
    data to the server, a backup to the local directory is needed
    '''
    os.system('raspistill -o ' + pi_folder + filename)  # first store the picture locally as backup
    
    # Connect to the FTP server
    session = ftplib.FTP(conf.FTP_Server['host'],
                         conf.FTP_Server['user'],
                         conf.FTP_Server['password'])
    
    # Access the target directory and send the picture
    session.pwd()
    file = open(pi_folder + filename, 'rb')
    session.cwd(FTP_Server['ftp_folder'])
    session.storbinary('STOR ' + filename, file)
    file.close()
   
    # Disconnect 
    session.quit()

    if __debug__:
        print "Uploaded picture" + filename


def store_data_to_db(temp_f,        # The temperature data
                     humidity,      # The humidity data
                     moistureA,     # The mositure data from PinA
                     mositureB,     # The moisture data from PinB
                     mositureC):    # The mositure data from pinC
    '''
    Store the data(humidity, moisture, etc) to the database
    First create the corresponding SQL codes
    Then execute them
    '''
    conn = connect_db()
    with conn:
        cur = conn.cursor()
        create_table_sql = "CREATE TABLE IF NOT EXISTS Mettetal_2(
                                id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                                PI_id TINYINT(6), 
                                Location VARCHAR(255), 
                                Temperature_Internal FLOAT NOT NULL, 
                                Humidity_Internal FLOAT NOT NULL, 
                                Moisture_A FLOAT NOT NULL, 
                                Moisture_B FLOAT NOT NULL, 
                                Moisture_C FLOAT NOT NULL, 
                                Time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)"
        
        select_table_sql = 'SELECT * FROM Mettetal_2'
        insert_table_sql = "INSERT INTO Mettetal_2(
                                PI_id, Temperature_Internal, 
                                Humidity_Internal, 
                                Moisture_A, Moisture_B, Moisture_C, Location) 
                            VALUES("+str(conf.PI_id)+", "+str(temp_f)+", "   +str(humidity)+", "
                                    +str(moistureA)+", " +str(moistureB)+", "+str(moistureC)+", 
                                    'Test Site 1')"
        cur.execute(create_table_sql)
        cur.execute(select_table_sql)
        cur.execute(insert_table_sql)

        if __debug__:
            print "Uploaded data!"


def get_data_and_store():
    '''
    The main process of this project:
    1. Get the necessary data from sensors, 
    2. Store the data locally 
    3. Check if Internet is available. If available, send the data to the server
    Repeat from 1
    '''
    while True:
        # Some preparation work
        # check_temperature()
        time.sleep(conf.timedelay_2)          
        
        # SETP 1: Get all data from sensors
        now = datetime.datetime.now()
        timestamp = now.strftime('%Y_%m_%d_%H_%M_%S')
        filename  = str(timestamp) + '.jpg'     
       
        # P = subprocess.Popen('./Adafruit_DHT')
        # output = subprocess.check_output(['./Adafruit_DHT', '2302', str(humidity_pinA),]
        # TODO 
        
        # Open temperature sensors
        # spi = spidev.SpiDev()
        # spi.open(0, 0)

        humidity = 1;
        temp_f = 1;
        
        # mositureA = check_moisture(conf.moisture_pinA)
        # mositureB = check_moisture(conf.moisture_pinB)
        # mositureC = check_moisture(conf.moisture_pinC)
        moistureA = 0.1
        moistureB = 0.2
        mositureC = 0.3

        ### The following parts are used to debug  ###
        if __debug__:
            print 'took picture ' + timestamp		
	    print "Humidity:    %.1f %%" % humidity
	    print "Internal Temperature: %.1f F" % temp_f
	    print "Moisture A = " + moistureA
	    print "Moisture B = " + moistureB
	    print "Moisture C = " + moistureC
	    print 'uploaded picture ' + timestamp

        # STEP 2: Store data locally
        os.system('raspistill -o ' + pi_folder_1 + filename)
        # text_file = open("/home/pi/Desktop/parjana_data.txt", "a")
        text_file = open("/home/life/test1.log", "a")
        text_file.write("PI_id: %s"%conf.PI_id 
                        + ", Internal Temp: %s"%temp_f 
                        + ", Internal Humidity: %s"%humidity 
                        + ", Moisture A: %s"%moistureA 
                        + ", Moisture B: %s"%moistureB 
                        + ", Moisture C: %s"%moistureC
                        + ", Time: %s"%timestamp + ", Test Site 2" + '\n')
        text_file.close()
        
        # STEP 3: Send data to the server and database if Internet is available
        #if internet_on():
        #    store_data_to_ftp(filename)  # store pictures to FTP server
        #    connect_db()                 # store data to the database
        #    store_data_to_db(temp_f, humidity, moistureA, moistureB, moistureC)






