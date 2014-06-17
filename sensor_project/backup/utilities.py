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
import sys
import urllib2    # Used to test if internet is available
import urllib
import re
import subprocess

##### My configuration file ####
import conf

##### Connection interface with MySQL ######
import MySQLdb

##### Sensor lib ######
import spidev 
import RPi.GPIO as GPIO

# Turn on temperature and moisture sensors
spi = spidev.SpiDev()
spi.open(0,0)

GPIO.setwarnings(False)

#####################################################################
######################## Utility functions ##########################
#####################################################################
def control_light_on(num):
	'''
	Turns on LED lights:
		25 > yellow LED code is running
		23 > Green LED internet on
	'''
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(num,GPIO.OUT)
	GPIO.output(num,True)
	

def control_light_off(num):
	'''
	Turns off LED lights on to show that:
		25 > yellow LED code is running
		23 > Green LED internet on
	'''
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(num,GPIO.OUT)
	GPIO.output(num,False)

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
    #TODO: elif read_temp() < 34:                # If temperature is below 34 
    elif 30 < 34: 
        GPIO.output(conf.pin_number, True)    # Turn on the light bulb on to warm up the computer
    else:                               # Else turn off 
        GPIO.output(conf.pin_number, False)

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


def store_data_to_ftp(filename):
    '''
    Connect to the FTP server, and then store the pictures 
    data to the server, a backup to the local directory is needed
    '''
    # Connect to the FTP server
    session = ftplib.FTP(conf.FTP_Server['host'],
                         conf.FTP_Server['user'],
                         conf.FTP_Server['password'])
    
    print 'Connected to FTP server'

    # Access the target directory and send the picture
    session.pwd()
    file = open(conf.pi_folder_1 + filename, 'rb')
    session.cwd(conf.FTP_Server['ftp_folder'])
    session.storbinary('STOR ' + filename, file)
    file.close()
   
    # Disconnect 
    session.quit()

    #if __debug__:
    print "Uploaded picture to ftp server!" + filename

def connect_db():
    '''
    Build connection to the given database
    '''
    conn = MySQLdb.connect(conf.DB['host'],
                           conf.DB['user'],
                           conf.DB['password'],
                           conf.DB['database'])
    
    print 'Connected to database!'
    return conn

def store_data_to_db(temp_f,        # The temperature data
                     humidity,      # The humidity data
                     moistureA,     # The mositure data from PinA
                     moistureB,     # The moisture data from PinB
                     moistureC):    # The mositure data from pinC
    '''
    Store the data(humidity, moisture, etc) to the database
    First create the corresponding SQL codes
    Then execute them
    '''
    conn = connect_db()
    with conn:
        cur = conn.cursor()
        create_table_sql = "CREATE TABLE IF NOT EXISTS 85_Lake_Basement_1(\
                                id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,\
                                PI_id TINYINT(6),\
                                Location VARCHAR(255),\
                                Temperature_Internal FLOAT NOT NULL,\
                                Humidity_Internal FLOAT NOT NULL,\
                                Moisture_A FLOAT NOT NULL,\
                                Moisture_B FLOAT NOT NULL,\
                                Moisture_C FLOAT NOT NULL,\
                                Time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)"
        
        #select_table_sql = 'SELECT * FROM 85_Lake_Basement_1'
        insert_table_sql = "INSERT INTO 85_Lake_Basement_1(\
                                PI_id, Temperature_Internal,\
                                Humidity_Internal, \
                                Moisture_A, Moisture_B, Moisture_C, Location)\
                            VALUES("+str(conf.PI_id)+", "+str(temp_f)+", "   +str(humidity)+", "\
                                    +str(moistureA)+", " +str(moistureB)+", "+str(moistureC)+",\
                                    'Test Site 1')"
        cur.execute(create_table_sql)
        #cur.execute(select_table_sql)
        cur.execute(insert_table_sql)

        #if __debug__:
        print "Uploaded data to database!"

def get_humidity_and_temp(): 
    '''
    Get humidity and temperature data from sensors
    '''
    try:
        output = subprocess.check_output(["./Adafruit_DHT2.py", "2302", "17"]);
    except Exception:
        print 'Exception happened with humidity sensor ......'
        return (None, None)

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
   
    file = open("test1.txt", "a")
    file.write(str(datetime.datetime.now()) + ': ')
    file.write(str(temp_f) + ',' + str(humidity) + '\n')
    file.close()
    
    return (humidity, temp_f)

def get_moisture():
    '''
    Get the mositrue info from sensors
    '''
    try:
        moistureA = check_moisture(conf.moisture_pinA)
        moistureB = check_moisture(conf.moisture_pinB)
        moistureC = check_moisture(conf.moisture_pinC)
        return (moistureA, moistureB, moistureC) 
    except Exception:
        print 'Exception happened with moisture sensor ......'
        return (None, None, None)

def take_picture(filename):
    '''Start the camera sensor, return False if exception happened'''
    try:
        os.system('raspistill -o ' + conf.pi_folder_1 + filename)
    except Exception:
        'Exception happened with camera, continue ......'
        return False


# The main function  
def get_data_and_store():
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
    print '>>>>>>>>>> Begin data collection >>>>>>>>>>>>>>'
    
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y_%m_%d_%H_%M_%S')
    filename  = str(timestamp) + '.jpg'     

    # SETP 1: Get all data from sensors
    humidity, temp_f = get_humidity_and_temp()  
    if (humidity, temp_f) == (None, None):
        print 'Continue >>>>>>>'
    
    moistureA, moistureB, moistureC = get_moisture()  
    if (moistureA, moistureB, moistureC) == (None, None, None):
        print 'Continue >>>>>>>'
    
    if take_picture(filename) == False:                             
        print 'Continue >>>>>>>'

    ### The following parts are used to debug  ###
    print 'Took picture ' + timestamp
    print "Humidity: %.1f %%" % humidity
    print "Internal Temperature: %.1f F" % temp_f
    print "Moisture A = " + str(moistureA)
    print "Moisture B = " + str(moistureB)
    print "Moisture C = " + str(moistureC)

    # STEP 2: Store data locally
    text_file = open("/home/pi/Desktop/parjana_data.txt", "a")
    text_file.write("PI_id: %s"%conf.PI_id 
                    + ", Internal Temp: %s"%temp_f 
                    + ", Internal Humidity: %s"%humidity 
                    + ", Moisture A: %s"%moistureA 
                    + ", Moisture B: %s"%moistureB 
                    + ", Moisture C: %s"%moistureC
                    + ", Time: %s"%timestamp + ", 85_Lake_Basement_1" + '\n')
    text_file.close()
        
    # STEP 3: Send data to the server and database if Internet is available
    if internet_on() == True:
	print 'Internet is ON, sending data to server >>>>>'
        control_light_on(23)
	store_data_to_ftp(filename)  # store pictures to FTP server
	connect_db()                 # store data to the database
	store_data_to_db(temp_f, humidity, moistureA, moistureB, moistureC)
    else:
        print 'Internet is off, data stored locally!'

    # STEP 4: Turn off the light and then restart PI
    control_light(True)
    control_light_off(23)
    print ">>>>>>>> Finished Processing! Rebooting >>>>>> "



if __name__ == '__main__':
    '''Power ON, turn on LED'''    
    control_light_on(25)    
    
    '''Handle data collection'''
    time.sleep(conf.period/10)
    get_data_and_store()
    time.sleep(conf.period/10)

    '''Turn off LED and reboot'''    
    control_light_off(25)
    #os.system('sudo reboot')



