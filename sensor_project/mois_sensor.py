#!/usr/bin/python

#
# DESC:
# The moisture sensor module, return the mositrue values of 
# the three different sensors
#

import spidev 
import conf

# Turn on moisture sensors
spi = spidev.SpiDev()
spi.open(0,0)

def check_moisture(adcnum):
    '''
    Read moisture from pins
    '''
    if((adcnum > 7) or (adcnum < 0)):
        print 'Wrong pin number'
        return -1
    
    r = spi.xfer2([1, (8 + adcnum)<<4, 0])
    adcout = ((r[1]&3) << 8) + r[2]
    return adcout


def get_moisture():
    '''
    Get the mositrue info from sensors
    '''
    moistureA = check_moisture(conf.moisture_pinA)
    moistureB = check_moisture(conf.moisture_pinB)
    moistureC = check_moisture(conf.moisture_pinC)

    return (moistureA, moistureB, moistureC) 



