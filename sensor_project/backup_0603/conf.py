#!/usr/bin/python

#
# File Name: conf.py
# 
# Desc:
# The configuration information about the database and some other stuff
# 
# Date:
# 05/20/2014
#


#------------------------------------------------------------
#           Local directory storing the results 
#------------------------------------------------------------
pi_folder = '/home/pi/Desktop/pictures/'      # the directory for storing the results if the internet is on
pi_folder_1 = '/home/pi/Desktop/pictures_1/'  # the directory for storing the results if the internet is down
usb_folder = '/media/PARJANA03_/'             # USB saving directory


#------------------------------------------------------------
#       The hardware interface information 
#------------------------------------------------------------
PI_id = 2           # ID of computer
moisture_pinA = 0   # Moisture pin A (moisture pins can be in range from (0-8))
moisture_pinB = 1   # Moisture pin B
moisture_pinC = 2   # Moisture pin C
pin_number = 22     # Pin that is connected to lightbulb
humidity_pinA = 17  # Humidity sensor pin num

ct_port = '/dev/ttyACM0'    # USB port # of the Arduino board
ct_baudrate = 9600              # The BAUD rate of the CT sensor when collecting data


#------------------------------------------------------------
#    The time period between two collections 
#------------------------------------------------------------
period = 900


#------------------------------------------------------------
#         Database and FTP Server Information 
#------------------------------------------------------------
DB = {
    'host' : '198.57.219.221', 
    'user' : 'theparja_georgeg',
    'password' : 'ggrzywacz2190',
    'database' : 'theparja_airport',
    'database_c': 'theparja_Test'
}

FTP_Server = { 
    'host' : '198.57.219.221',
    'user' : 'data@theparjanadistribution.com',
    'password' : 'Parjana1247',
    'ftp_folder' : '/Airport/Mettetal/Camera1/'
}

