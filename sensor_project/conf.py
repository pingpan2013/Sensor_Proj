#!/usr/bin/python

#
# File Name: conf.py
# 
# Desc:
# The configuration information about the database and some other stuff
#

####################################################
######### Local directory storing the results ######
####################################################
pi_folder = '/home/pi/Desktop/pictures/'      # the directory for storing the results if the internet is on
pi_folder_1 = '/home/pi/Desktop/pictures_1/'  # the directory for storing the results if the internet is down
usb_folder = '/media/PARJANA03_/'             # USB saving directory

####################################################
######## The hardware interface information ########
####################################################
PI_id = 2           # ID of computer
moisture_pinA = 0   # Moisture pin A (moisture pins can be in range from (0-8))
moisture_pinB = 1   # Moisture pin B
moisture_pinC = 2   # Moisture pin C
pin_number = 22     # Pin that is connected to lightbulb
humidity_pinA = 17  # Humidity sensor pin num


####################################################
################# Time delay needed ################ 
####################################################
timedelay_1 = 1         # maincode wait time
timedelay_2 = 1         # no internet wait time 
timedelay_3 = 1         # internet wait time


####################################################
###### Database and FTP Server Information #########
####################################################
DB = {
    'host' : '198.57.219.221', 
    'user' : 'camera@theparjanadistribution.com',
    'password' : 'grzywacz1',
    'database' : 'theparja_airport'
}

FTP_Server = { 
    'host' : '198.57.219.221',
    'user' : 'pingpan@theparjanadistribution.com',
    'password' : 'wlx1134908',
    'ftp_folder' : 'testFTP/'
}

