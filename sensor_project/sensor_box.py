#!/usr/bin/env python

#
# File Name: sensor_box.py
#
# Desc:
# Control the sensor to get humidity and moisture infomation
# If internet is down, store the result into local files
# else send the data to the database
#

import os
import time
import datetime
import logging
import subprocess

import RPi.GPIO as GPIO
import conf
from led import turn_LED_on, turn_LED_off, LED_YELLOW, LED_GREEN
import server_conn
import log_management as log_m
import csv_data
import mois_sensor
import humi_sensor
import curr_sensor
import temp_sensor
import water_level

GPIO.setwarnings(False)

def main():
    '''
    The main process of this project:
    1. Get data from sensors, including humidity/moisture/temperature 
    2. Store the data locally 
    3. Check if Internet is available; if so, send the data to the server
    4. Wait to restart cycle
    '''
    # Some preparation work
    # Use yellow LED to indicate code is running
    turn_LED_on(LED_YELLOW)
    internet_working = True
    humidity = None
    temp_f = None
    moistures = None
    temps = None
    water_depth = None
    # Time spent waiting for sensor values with reduced noise
    sensor_reading_time = conf.water_level_interval
    # Ensure required picture directories exist
    if not os.path.exists(conf.online_pictures_folder):
        os.makedirs(conf.online_pictures_folder)
    if not os.path.exists(conf.offline_pictures_folder):
        os.makedirs(conf.offline_pictures_folder)
    
    # Initial stuff at the top of the log file.
    log_m.start_log()
    
    # Begin main program loop
    while True:
        # Get current timestamp first
        now = datetime.datetime.now()
        picture_filename_timestamp = now.strftime('%Y_%m_%d_%H_%M_%S')
        mysql_timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        csv_timestamp = now.strftime('%m/%d/%y %I:%M %p')
        pic_filename  = str(picture_filename_timestamp) + '.jpg'
        pic_path = conf.offline_pictures_folder + pic_filename
        logging.info('Beginning data collection cycle')
        
        # STEP 1: Get all data from sensors
        try:
            if conf.using_humidity_sensor:
                humidity, temp_f = humi_sensor.get_humidity_and_temp()
                logging.debug("Humidity: %.1f %%" % humidity)
                logging.debug("Internal Temperature: %.1f F" % temp_f)
            if conf.num_moisture_sensors > 0:
                moistures = mois_sensor.get_moistures(conf.num_moisture_sensors)
                sensor_chr = 'A'
                for moisture in moistures:
                    logging.debug("Moisture " + sensor_chr + " = " + str(moisture))
                    sensor_chr = chr(ord(sensor_chr) + 1)
                if len(moistures) != conf.num_moisture_sensors:
                    logging.error("Number of moistures doesn't match conf")
            if conf.num_temp_sensors > 0:
                temps = temp_sensor.get_temp_data_f()
                sensor_chr = 'A'
                for temp in temps:
                    logging.debug("Temperature " + sensor_chr + " = " + str(temp))
                    sensor_chr = chr(ord(sensor_chr) + 1)
                if len(temps) != conf.num_temp_sensors:
                    logging.error("Number of temperatures doesn't match conf")
            if conf.using_water_level_sensor:
                water_depth = water_level.get_inches(conf.water_level_interval)
        except:
            logging.exception("Exception occurred while reading sensors")
        logging.info('Gathered data')
        if conf.using_camera:
            subprocess.call(['raspistill', '-o', pic_path])
            logging.debug('Took picture ' + pic_filename)

        # STEP 2: Store data locally
        # Initialize CSV file if not present
        csv_data.initialize()
        # Add new line of data to CSV file
        csv_data.write_data(temp_f,
                            humidity,
                            moistures,
                            temps,
                            water_depth,
                            csv_timestamp
                           )
        logging.debug("Next reading to be collected in " 
                      + str(float(conf.period)/60.0) + " minutes")
        time.sleep((conf.period - sensor_reading_time)/2)
        
        # STEP 3: Send data to the server and database if Internet is available
        try:
            if server_conn.internet_on():
                if not internet_working:
                    logging.warning('Internet restored; sending data...')
                    internet_working = True
                else:
                    logging.info('Sending data...')
                # Turn on green LED to indicate Internet usage
                turn_LED_on(LED_GREEN)
                if conf.using_camera:
                    try:
                        # store pictures to FTP server
                        server_conn.store_data_to_ftp(pic_filename)
                        os.system("rm -f " + conf.offline_pictures_folder + '*')
                    except IOError:
                        logging.exception('Could not send picture file')
                try:
                    # store data in database
                    server_conn.store_data_to_db(temp_f,
                                                 humidity,
                                                 moistures,
                                                 temps,
                                                 water_depth,
                                                 mysql_timestamp
                                                )
                except:
                    logging.exception('Exception occurred with database code')
                logging.info('Data sent')
            else:
                if internet_working:
                    logging.warning('Internet is down; could not send data')
                    internet_working = False
        except:
            logging.exception('Exception occurred when trying to send data')
        turn_LED_off(LED_GREEN)
        
        # STEP 4: Wait until cycle starts over again
        time.sleep((conf.period - sensor_reading_time)/2)
        # End of main loop
    turn_LED_off(LED_YELLOW)
    logging.info('Exited main loop. Stopping data recording')

if __name__ == '__main__':
    main()
