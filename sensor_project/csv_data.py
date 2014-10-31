#!/usr/bin/env python

#
# File Name: csv_data.py
#
# Desc:
# Simplify working with the CSV data file being recorded.
#

import logging
import os

import conf

csv_path = conf.desktop + conf.csv_filename
FLOAT_FORMAT_STR = "{:." + str(conf.precision) + "f}"
PERCENT_FORMAT_STR = "{:." + str(conf.precision) + "%}"

def make_csv_line(items):
    '''
    Makes a single line for a CSV file from a provided list of strings.
    '''
    # Use Windows-style line endings for Excel compatibility.
    return ",".join(items) + "\r\n"

def initialize():
    '''
    Initialize the CSV file using conf settings if it is not present.
    '''
    if not os.path.exists(csv_path):
        with open(csv_path, "w") as csv_file:
            headers = []
            temp_unit = " (" + conf.temperature_units + ")"
            if conf.using_humidity_sensor:
                headers.append("Internal Temperature" + temp_unit)
                headers.append("Internal Humidity %")
            if conf.num_moisture_sensors > 0:
                sensor_chr = 'A'
                for i in range(0, conf.num_moisture_sensors):
                    headers.append("Moisture " + sensor_chr)
                    sensor_chr = chr(ord(sensor_chr) + 1)
            if conf.num_temp_sensors > 0:
                sensor_chr = 'A'
                for i in range(0, conf.num_temp_sensors):
                    headers.append("Temperature " + sensor_chr + temp_unit)
                    sensor_chr = chr(ord(sensor_chr) + 1)
            if conf.using_water_level_sensor:
                headers.append("Water Level (inches)")
            headers.append("Timestamp")
            csv_file.write(make_csv_line(headers))
    logging.info('CSV file ' + csv_path + ' initialized')

def write_data(temp_f, humidity, moistures, temps, water_depth, timestamp):
    '''
    Write a single line of data to an already-initialized CSV file.
    '''
    with open(csv_path, "a") as csv_file:
        data_items = []
        if conf.using_humidity_sensor and temp_f != None and humidity != None:
            data_items.append(FLOAT_FORMAT_STR.format(temp_f))
            data_items.append(FLOAT_FORMAT_STR.format(humidity) + "%")
        if conf.num_moisture_sensors > 0 and moistures != None:
            for moisture in moistures:
                data_items.append(FLOAT_FORMAT_STR.format(moisture) + "%")
        if conf.num_temp_sensors > 0 and temps != None:
            for temp in temps:
                data_items.append(FLOAT_FORMAT_STR.format(temp))
        if conf.using_water_level_sensor and water_depth != None:
            data_items.append(FLOAT_FORMAT_STR.format(water_depth))
        data_items.append(timestamp)
        csv_file.write(make_csv_line(data_items))
    logging.info('Wrote data to file')
