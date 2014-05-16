#!/usr/bin/env python
# -*- coding: utf-8 -*-

# < code is not working
## < notes

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
pi_folder_1 = '/home/pi/Desktop/pictures_1/' ##save pictures to folder if no internet
usb_folder = '/media/PARJANA03_/' ##save pictures to USB

PI_id = 2 ##ID of computer
moisture_pinA = 0 ##moisture pins can be in range from (0-8)
moisture_pinB = 1
moisture_pinC = 2
pin_number = 22 ##pin that is connected to lightbulb
humidity_pinA = 17 ##humidity sensor pin #

time_1 = 40 ##maincode wait time
time_2 = 40 ##no internet wait time 
time_3 = 40 ##internet wait time

##see learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/hardware

spi = spidev.SpiDev() ##temperature sensors, if more then one temp sensor, need to find IP of each sensor
spi.open(0,0) ##pin for moisture is 4
#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')
#base_dir = '/sys/bus/w1/devices/'
#device_folder = glob.glob(base_dir + '28*')[0] 
#device_file = device_folder + '/w1_slave'
 
#def read_temp_raw():
#    f = open(device_file, 'r')
#    lines = f.readlines()
#    f.close()
#    return lines

#def read_temp(): #reads temperature and converts it into F
#	lines = read_temp_raw()
#	while lines[0].strip()[-3:] != 'YES':
#		time.sleep(0.2)
#		lines = read_temp_raw()
#	equals_pos = lines[1].find('t=')
#	if equals_pos != -1:
#		temp_string = lines[1][equals_pos+2:]
#		temp_c = float(temp_string) / 1000.0
#		temp_f = temp_c * 9.0 / 5.0 + 32.0
#		return temp_f

def readadc(adcnum): ##reads moisture from pins
	if ((adcnum > 7) or (adcnum < 0)):
		return -1
	r = spi.xfer2([1,(8+adcnum)<<4,0])
	adcout = ((r[1]&3) << 8) + r[2]
	return adcout

def check_moisture(moisture_pinA): ##Check Moisture data pin A
	return (readadc(moisture_pinA))

def check_moisture(moisture_pinB): ##Check Moisture data pin B
	return (readadc(moisture_pinB))

def check_moisture(moisture_pinC): ##Check Moisture data pin C
	return (readadc(moisture_pinC))

def restart(): ##code to reset pi
	command = '/usr/bin/sudo /sbin/shutdown -r now'
	process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
	output = process.communicate()[0]

def internet_on(): ##test if internet is working
	try:
		req = urllib2.urlopen('http://google.com')
		response=urllib2.urlopen('http://google.com',timeout=2)
		true()
	except urllib2.URLError as err:
		print err
		false()

def true(): ##if internet
	Main_code()

def false(): ##if no internet
	Sub_code()

def Sub_code(): ##code if no internet
	
	t0 = time.time()
	while True:
		t1 = time.time()
		if t1-t0 >=time_2: ##wait
			t0 = t1
			t0 = time.time()
	
			GPIO.setmode(GPIO.BCM) ##turn on pins to use light bulb
			GPIO.setup(pin_number,GPIO.OUT)
			GPIO.output(pin_number,True)

			t0 = time.time()
			while True:
					t1 = time.time()
					if t1-t0 >=time_2: ##wait 
						t0 = t1
																			
						now = datetime.datetime.now() #time stamp for saving and naming picture
						timestamp = str(now.strftime('%Y_%m_%d_%H_%M_%S')) ##time format
						filename = str(timestamp) + '.jpg' ##filename of picture
						os.system('raspistill -o ' + pi_folder_1 + filename) ##save picture to file

						##see learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/overview

						#read humidity sensor
						#p=subprocess.Popen('./Adafruit_DHT') #open c code file
						#p=subprocess.Popen('./Adafruit_DHT') #open c code file
						#output = subprocess.check_output(["./Adafruit_DHT", "2302", str(humidity_pinA),]);
						#matches = re.search("Temp =\s+([0-9.]+)", output)
						#if (not matches):
						#	time.sleep(3)
						#	continue
						#temp = float(matches.group(1))
						#temp_f = temp * 9.0 / 5.0 + 32.0 # converts temp to F
						#matches = re.search("Hum =\s+([0-9.]+)", output) #search for humidity printout
						#if (not matches):
						#	time.sleep(3)
						#	continue
						#humidity = float(matches.group(1))
						
						humidity = 1 ##value is 1 as a place holder due to the code not working
						temp_f = 1 ##value is 1 as a place holder due to the code not working
						
						##used to verify code is working 
						print 'took picture ' + timestamp		
						print "Humidity:    %.1f %%" % humidity
						print "Internal Temperature: %.1f F" % temp_f
						#print "External Temperature = " + str(read_temp())
						print "Moisture A = " + str(check_moisture(moisture_pinA))
						print "Moisture B = " + str(check_moisture(moisture_pinB))
						print "Moisture C = " + str(check_moisture(moisture_pinC))
						print 'uploaded picture ' + timestamp
						
						##creates text file of all data recorded from previous code
						text_file = open("/home/pi/Desktop/parjana_data.txt", "a")
						text_file.write("PI_id: %s"%PI_id + ",  Internal Temp: %s"%temp_f + ", Internal Humidity: %s"%humidity + ", Moisture A: %s"%check_moisture(moisture_pinA) + ", Moisture B: %s"%check_moisture(moisture_pinB) + ", Moisture C: %s"%check_moisture(moisture_pinC) + ", Time: %s"%timestamp + ", Test Site 2" + '\n')		
						#text_file.write("PI_id: %s"%PI_id + ",  Internal Temp: %s"%temp_f + ", Internal Humidity: %s"%humidity + ", External Temp: %s"%read_temp() + ", Moisture A: %s"%check_moisture(moisture_pinA) + ", Moisture B: %s"%check_moisture(moisture_pinB) + ", Moisture C: %s"%check_moisture(moisture_pinC) + ", Time: %s"%timestamp + ", Test Site 3" + '\n')		
						text_file.close()	
						
						GPIO.setmode(GPIO.BCM) ##turn off light by disabling pins
						GPIO.setup(pin_number,GPIO.OUT)
						GPIO.output(pin_number,False)			
					
						##code needs to restart after recording data to make sure the system resets itself and a minimum amount of bugs are found
						#restart()											
	
def Main_code(): ##runs code if internet is on

	t0 = time.time()
	while True:
		t1 = time.time()
		if t1-t0 >=time_3:	##wait
			t0 = t1	
			
			print 'internet' ##verify internet is working
			
			##see learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/overview

			#read humidity sensor
			#p=subprocess.Popen('./Adafruit_DHT') #open c code file
			#p=subprocess.Popen('./Adafruit_DHT') #open c code file
			#output = subprocess.check_output(["./Adafruit_DHT", "2302", str(humidity_pinA),]);
			#matches = re.search("Temp =\s+([0-9.]+)", output)
			#if (not matches):
			#	time.sleep(3)
			#	continue
			#temp = float(matches.group(1))
			#temp_f = temp * 9.0 / 5.0 + 32.0 # converts temp to F
			#matches = re.search("Hum =\s+([0-9.]+)", output) #search for humidity printout
			#if (not matches):
			#	time.sleep(3)
			#	continue
			#humidity = float(matches.group(1))
			
			humidity = 1 ##value is 1 as a place holder due to the code not working
			temp_f = 1 ##value is 1 as a place holder due to the code not working
			
			now = datetime.datetime.now() #time stamp for saving and naming picture
			timestamp = str(now.strftime('%Y_%m_%d_%H_%M_%S')) ##time format
			filename = str(timestamp) + '.jpg' ##filename of picture
			os.system('raspistill -o ' + pi_folder_1 + filename) ##save picture to file
			
			##used to verify code is working
			print "Humidity:    %.1f %%" % humidity
			print "Internal Temperature: %.1f F" % temp_f
			#print "External Temperature = " + str(read_temp())
			print "Moisture A = " + str(check_moisture(moisture_pinA))
			print "Moisture B = " + str(check_moisture(moisture_pinB))
			print "Moisture C = " + str(check_moisture(moisture_pinC))
			
			##creates text file of all data recorded from previous code
			text_file = open("/home/pi/Desktop/parjana_data.txt", "a")
			#text_file.write("PI_id: %s"%PI_id + ",  Internal Temp: %s"%temp_f + ", Internal Humidity: %s"%humidity + ", Moisture A: %s"%check_moisture(moisture_pinA) + ", Moisture B: %s"%check_moisture(moisture_pinB) + ", Moisture C: %s"%check_moisture(moisture_pinC) + ", Time: %s"%timestamp + ", Test Site 3" + '\n')		
			text_file.write("PI_id: %s"%PI_id + ",  Internal Temp: %s"%temp_f + ", Internal Humidity: %s"%humidity + ", External Temp: %s 1" + ", Moisture A: %s"%check_moisture(moisture_pinA) + ", Moisture B: %s"%check_moisture(moisture_pinB) + ", Moisture C: %s"%check_moisture(moisture_pinC) + ", Time: %s"%timestamp + ", Test Site 2" + '\n')		
			text_file.close()
				
			
			##data base for MySQL	
			db = MySQLdb.connect(host='198.57.219.221', user= 'theparja_georgeg', passwd= 'ggrzywacz2190', db= 'theparja_airport') #connecting to bluehost.com > theparjanadistribution.com
			
			##camera ftp information
			host = '198.57.219.221' 
			user = 'camera@theparjanadistribution.com'
			password = 'grzywacz1'
			ftp_folder = 'Gallery/Mettetal_1/' ##website photo folder

			filename = str(timestamp) + '.jpg' ##picture file
			os.system('raspistill -o ' + pi_folder + filename) ##save picture to file
				
			##save picture and upload picture to server via FTP	
			#pi_picture = str(timestamp)
			#session = ftplib.FTP(host,user,password)
			#session.pwd()
			#file = open(pi_folder + str(pi_picture) + '.jpg','rb')	# file to send
			#myfolder = ftp_folder
			#session.cwd(myfolder)
			#session.storbinary('STOR ' + str(pi_picture)+ '.jpg',file) # send the file
			#file.close() # close file and FTP
			#session.quit()
				
			##verify camera function works
			print 'took picture ' + timestamp		
			print 'uploaded picture ' + timestamp
				
			with db:
					
				cur = db.cursor()
				##creates table in server
				#cur.execute("CREATE TABLE IF NOT EXISTS Mettetal_3(id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, PI_id TINYINT(6), Location VARCHAR(255), Temperature_Internal FLOAT NOT NULL, Humidity_Internal FLOAT NOT NULL, Temperature_External FLOAT NOT NULL, Moisture_A FLOAT NOT NULL, Moisture_B FLOAT NOT NULL, Moisture_C FLOAT NOT NULL, Time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)")
				cur.execute("CREATE TABLE IF NOT EXISTS Mettetal_2(id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, PI_id TINYINT(6), Location VARCHAR(255), Temperature_Internal FLOAT NOT NULL, Humidity_Internal FLOAT NOT NULL, Moisture_A FLOAT NOT NULL, Moisture_B FLOAT NOT NULL, Moisture_C FLOAT NOT NULL, Time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)")
				
				##selects table
				cur.execute('SELECT * FROM Mettetal_2') #creates a table with above parameters
		
				##inserts data above into table
				#cur.execute("INSERT INTO Mettetal_3(PI_id, Temperature_Internal, Humidity_Internal, Temperature_External, Moisture_A, Moisture_B, Moisture_C, Location) VALUES("+str(PI_id)+", "+str(temp_f)+", "+str(humidity)+", "+str(read_temp())+", "+str(check_moisture(moisture_pinA))+", "+str(check_moisture(moisture_pinB))+", "+str(check_moisture(moisture_pinC))+", 'Test Site 3')")#inserts values into table	
				cur.execute("INSERT INTO Mettetal_2(PI_id, Temperature_Internal, Humidity_Internal, Moisture_A, Moisture_B, Moisture_C, Location) VALUES("+str(PI_id)+", "+str(temp_f)+", "+str(humidity)+", "+str(check_moisture(moisture_pinA))+", "+str(check_moisture(moisture_pinB))+", "+str(check_moisture(moisture_pinC))+", 'Test Site 1')")#inserts values into table	
					
				GPIO.setmode(GPIO.BCM) ##turn off light
				GPIO.setup(pin_number,GPIO.OUT)
				GPIO.output(pin_number,False)	
					
				print 'uploaded'
				
				##code needs to restart after recording data to make sure the system resets itself and a minimum amount of bugs are found
				#restart()
					
t0 = time.time()						
while True:
	t1 = time.time()
	if t1-t0 >=time_1: ##wait 
		t0 = t1
		
		GPIO.setmode(GPIO.BCM) ##turn off light and helps prevent errors in pins on/off
		GPIO.setup(pin_number,GPIO.OUT)
		GPIO.output(pin_number,False)

		##if read_temp() < 34: #turns light bulb on to warm up computer
		
		x=30 ##place holder until external temperature code is fixed
		if x < 34: #turns light bulb on to warm up computer
				GPIO.setmode(GPIO.BCM) #turn on light
				GPIO.setup(pin_number,GPIO.OUT)
				GPIO.output(pin_number,True)
		else:
			GPIO.setmode(GPIO.BCM) #turn off light
			GPIO.setup(pin_number,GPIO.OUT)
			GPIO.output(pin_number,False)
	
		internet_on()
