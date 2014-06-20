#!/usr/bin/python

'''Reboot if the program runs for more than 20mins'''

import time
import datetime
import os

time.sleep(300)
os.system('sudo reboot')
