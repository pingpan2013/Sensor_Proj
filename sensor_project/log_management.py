#!/usr/bin/env python

#
# File Name: log_management.py
#
# Desc:
# SensorBox-specific functions for handling the software's log file.
#

import logging
from logging import info
from subprocess import call
import os.path

import conf

def log_number_of(sensor_type, num):
    '''
    Used for initial logging of how many of a type of sensor there is.
    '''
    return "\n\tNumber of " + sensor_type + ": " + str(num)

def log_if_using(sensor_type, val):
    '''
    Used for initial logging of whether we are using a particular sensor.
    '''
    response = "Yes" if val else "No"
    return "\n\tUsing " + sensor_type + ": " + response

def setup_log(log_level):
    '''
    Configures logging.
    '''
    logging.basicConfig(filename=conf.log_path,
                        level=log_level,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p'
                       )

def save_previous_log():
    '''
    Save the log file from the last run before starting one for this run.
    Also deletes the log file left over from the last run.
    '''
    if os.path.exists(conf.previous_log_path):
        call(["rm", "-f", conf.previous_log_path])
    if os.path.exists(conf.log_path):
        call(["mv", conf.log_path, conf.previous_log_path])

def start_log():
    '''
    Log initial info when SensorBox starts running.
    '''
    save_previous_log()
    setup_log(logging.INFO)
    info("Begin running SensorBox software " + conf.sensorbox_version + ".")
    info("Configured with the following settings in conf:" +
         "\n\tPI_id: " + str(conf.PI_id) +
         log_if_using("camera", conf.using_camera) +
         log_number_of("moisture sensors", conf.num_moisture_sensors) +
         log_number_of("temperature sensors", conf.num_temp_sensors) +
         log_if_using("humidity sensor", conf.using_humidity_sensor) +
         log_if_using("water level sensor", conf.using_water_level_sensor) +
         "\n\tLocation: " + conf.location +
         "\n\tTable name in database: " + conf.table_name +
         "\n\tFTP folder name on server: " + conf.ftp_name
        )
    interval = str(float(conf.period)/60.0)
    info("Configured to get a new reading every " + interval + " minutes.")
    info("Logging further messages at log level " + str(conf.log_level) + ".")
    logging.getLogger().setLevel(conf.log_level)
