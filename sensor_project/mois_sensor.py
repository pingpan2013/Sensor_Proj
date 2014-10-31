#!/usr/bin/python

#
# DESC:
# The moisture sensor module, return the moisture values of 
# the three different sensors
#

import spidev

# Moisture channels can be in a range from 0 to 2
pinA = 0
pinB = 1
pinC = 2

# Turn on moisture sensors
spi = spidev.SpiDev()
spi.open(0,0)

def check_moisture(adcnum):
    '''
    Read moisture from MCP3008 chip channels
    '''
    if((adcnum > 2) or (adcnum < 0)):
        print 'Wrong pin number'
        return -1
    
    r = spi.xfer2([1, (8 + adcnum)<<4, 0])
    adcout = ((r[1]&3) << 8) + r[2]
    return adcout


def get_moistures(num_expected):
    '''
    Get the moisture info from sensors.
    '''
    moistures = []
    if num_expected > 0:
        if num_expected >= 1:
            moistures.append(check_moisture(pinA) / 1023.0)
        if num_expected >= 2:
            moistures.append(check_moisture(pinB) / 1023.0)
        if num_expected >= 3:
            moistures.append(check_moisture(pinC) / 1023.0)

    return tuple(moistures) 
