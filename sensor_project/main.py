#!/usr/bin/python

#
# File name: main.py
# Desc: the main function of the sensor project
# Dependencies: utilities.py and conf.py     
#

import datetime
import time

import conf
import utilities

if __name__ == '__main__':
    
    time.sleep(conf.timedelay_1)    
    utilities.get_data_and_store()


