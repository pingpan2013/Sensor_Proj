#!/usr/bin/python

#
# File Name: conf.py
# 
# Desc:
# The configuration information about the database and some other stuff
#

##############################################
##### Directory for storing the results ######
##############################################
pi_folder = '/home/pi/Desktop/pictures/'      # the directory for storing the results if the internet is on
pi_folder_1 = '/home/pi/Desktop/pictures_1/'  # the directory for storing the results if the internet is down
usb_folder = '/media/PARJANA03_/'             # USB saving directory


#############################################
##### The hardware interface information ####
#############################################
PI_id = 2           # ID of computer
moisture_pinA = 0   # Moisture pin A (moisture pins can be in range from (0-8))
moisture_pinB = 1   # Moisture pin B
moisture_pinC = 2   # Moisture pin C
pin_number = 22     # Pin that is connected to lightbulb
humidity_pinA = 17  # Humidity sensor pin num


############################################
######### Acceptable time delay ############ 
############################################
time_1 = 40         # maincode wait time
time_2 = 40         # no internet wait time 
time_3 = 40         # internet wait time


############################################
###### Database Server Information #########
############################################
DB = {
    host = '198.57.219.221', 
    user = 'camera@theparjanadistribution.com',
    password = 'grzywacz1',
}

ftp_folder = 'Gallery/Mettetal_1/'      # Website photo folder
