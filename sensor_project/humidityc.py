  #!/usr/bin/env python
# -*- coding: utf-8 -*-


import ftplib
import os
import time
import datetime
import glob
import subprocess
import sys
from subprocess import call
import RPi.GPIO as GPIO
import urllib2
import urllib
import tempfile
import re
import glob
import MySQLdb
import spidev ##temp sensor

pi_folder = '/home/pi/Desktop/pictures/' ##save pictures to folder if internet
pi_folder_1 = '/home/pi/Desktop/pictures_1/' ##save pictures to folder if no 

while(True):

  # Run the DHT program to get the humidity and temperature readings!

  output = subprocess.check_output(["./Adafruit_DHT", "2302", "4"]);
  print output
  matches = re.search("Temp =\s+([0-9.]+)", output)
  if (not matches):
	time.sleep(3)
	continue
  temp = float(matches.group(1))
  temp_f = temp * 9.0 / 5.0 + 32.0 # converts temp to F
  
  # search for humidity printout
  matches = re.search("Hum =\s+([0-9.]+)", output)
  if (not matches):
	time.sleep(3)
	continue
  humidity = float(matches.group(1))

  print "Temperature: %.1f F" % temp_f
  print "Humidity:    %.1f %%" % humidity
  
  now = datetime.datetime.now() #time stamp for saving and naming picture
  timestamp = str(now.strftime('%Y_%m_%d_%H_%M_%S')) ##time format
  filename = str(timestamp) + '.jpg' ##filename of picture
  os.system('raspistill -o ' + pi_folder_1 + filename) ##save picture to file
			 
  ##camera ftp information
  host = '198.57.219.221' 
  user = 'data@theparjanadistribution.com'
  password = 'Parjana1247'
  ftp_folder = '/Airport/Mettetal/Camera1/' ##website photo folder

  filename = str(timestamp) + '.jpg' ##picture file
  os.system('raspistill -o ' + pi_folder + filename) ##save picture to file
				
  ##save picture and upload picture to server via FTP	
  pi_picture = str(timestamp)
  session = ftplib.FTP(host,user,password)
  session.pwd()
  file = open(pi_folder + str(pi_picture) + '.jpg','rb')	# file to send
  myfolder = ftp_folder
  session.cwd(myfolder)
  session.storbinary('STOR ' + str(pi_picture)+ '.jpg',file) # send the file
  file.close() # close file and FTP
  session.quit()
				
  #verify camera function works
  print 'took picture ' + timestamp		
  
  time.sleep(10)

