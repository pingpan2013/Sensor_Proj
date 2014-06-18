#!/usr/bin/python

#
# File Name: utilities.py
#
# Desc:
# Control the sensor to get humidity and moisture infomation
# If internet is down, store the result into local files
# else send the data to the database
#
import os
import time      
import datetime
import sys
import urllib2    # Used to test if internet is available
import urllib
import conf


def internet_on():
    '''
    Test if internet access is available
    Return true if available, otherwise return false
    '''
    try:
        response = urllib2.urlopen('http://74.125.228.100', timeout=1)
        print 'Internet is On!'
        return True
    except urllib2.URLError as err: pass
    return False
    
if __name__ == '__main__':
    try:
        time.sleep(conf.period/10)
        now = datetime.datetime.now()
        timestamp = now.strftime('%Y_%m_%d_%H_%M_%S')
        filename  = str(timestamp) + '.jpg'

        print 'Turn on light for camera >>'
        #control_light_on(24)
        time.sleep(5)
        print 'Taking picture ' + timestamp
        os.system('sudo raspistill -o ' + conf.pi_folder_1 + filename)
        time.sleep(5)
        print 'Turn off light for camera >>'
        #control_light_off(24)
        
        print 'Reconfiguring...'
        time.sleep(60)
        
        if internet_on() == True:
	    print 'Internet is ON, sending data to server >>>>>'
        else:
            print 'Internet is off, data stored locally!'
    finally:
        time.sleep(conf.period/10)
        #os.system('sudo reboot')


