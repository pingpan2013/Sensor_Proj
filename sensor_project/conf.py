#!/usr/bin/python

#
# File Name: conf.py
# 
# Desc:
# The configuration information about the database and some other stuff
#

import RPi.GPIO as GPIO

#==================================================
#     Local directory storing the results 
#==================================================
pi_folder = '/home/pi/Desktop/pictures/'      # the directory for storing the results if the internet is on
pi_folder_1 = '/home/pi/Desktop/pictures_1/'  # the directory for storing the results if the internet is down
usb_folder = '/media/PARJANA03_/'             # USB saving directory

#===================================================
#     The hardware interface information 
#===================================================
PI_id = 12          # ID of computer
moisture_pinA = 0   # Moisture pin A (moisture pins can be in range from (0-8))
moisture_pinB = 1   # Moisture pin B
moisture_pinC = 2   # Moisture pin C
pin_number = 22     # Pin that is connected to lightbulb
humidity_pinA = 17  # Humidity sensor pin num
led_yellow = 25     # Led that powers on when code starts
led_green = 23      # Led that powers on when there is internet


#===================================================
#    The time period between two collections 
#===================================================
period = 120

#===================================================
#     Database and FTP Server Information 
#===================================================
DB = {
    'host' : '198.57.219.221', 
    'user' : 'theparja_georgeg',
    'password' : 'ggrzywacz2190',
    'database' : 'theparja_residential'
}

FTP_Server = { 
    'host' : '198.57.219.221',
    #'user' : '85_lake_basement_1@theparjanadistribution.com',
    #'password' : 'Parjana1274',
    #'ftp_folder' : '/Gallery/Residential/Basement_Monitoring/85_Lake_Brighton_MI/Basement_Camera_1/'
    'user' : 'data@theparjanadistribution.com',
    'password' : 'Parjana1247',
    #'ftp_folder' : '/Airport/Mettetal/Camera1/'
    'ftp_folder' : '/Residential/Basement_Monitoring/85_Lake_Brighton_MI/Basement_Camera_1/'
    
}


#===================================================
#             Utility Functions
#===================================================
def control_LED(pin_num, ifOn):
    '''
    Control the LED light according to the pin number
        if ifOn = True, to turn it on
        else to turn it off
    '''
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_num, GPIO.OUT)
    GPIO.output(pin_num, ifOn)



