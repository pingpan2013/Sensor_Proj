#!/usr/bin/python

#
# DESC:
# Get data from the smart-cup water level measurement sensor.
# Determine the status of the pump according to the returned data from sensor.
#

import spidev
import time
import datetime

import conf

water_level_channel = 7

# Turn on water level sensor
spi = spidev.SpiDev()
spi.open(0,0)

def _get_raw_reading():
    '''
    Gets the raw reading from the water level sensor on a channel of the
    MCP3008 chip over GPIO.
    '''
    spidata = spi.xfer2([1, (8 + water_level_channel)<<4, 0])
    adcout = ((spidata[1] & 3) << 8) + spidata[2]
    return adcout

def _calibrate():
    '''
    Have the user help calibrate the sensor.
    '''
    import numpy
    inches = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
    avg_readings = []
    print "Begin calibration."
    for i in inches:
        raw_input("Submerge the sensor to " + str(i) + " inches and press Enter.")
        print("Please wait 5 seconds (do NOT change submersion depth!)...")
        avg = []
        for x in range(0, 500):
            avg.append(round(((_get_raw_reading() * 3300) / 1024),0))
            time.sleep(0.01)
        avg_readings.append(sum(avg) / len(avg))
    regression = numpy.polyfit(avg_readings, inches, 1)
    print "Calibration complete!"
    print "slope =", str(regression[0]), ", y-intercept =", str(regression[1])
    print "Replace the appropriate values in conf.py for more accurate readings."
    return regression

def _convert_to_inches(value, slope=-0.0232, yintercept=62.5864):
    '''
    Determine the water level in inches according to the value returned from
    the sensor.
    Return the level of the water in the range [0, 5].
    '''
    return max(slope * float(value) + yintercept, 0.0)

def get_inches(timespan=1):
    '''
    Get submersion depth in inches using calibration data from conf.
    timespan controls how long to wait for the final value, to help eliminate
    noise in the data.
    '''
    slope = conf.water_level_slope
    intercept = conf.water_level_yintercept
    voltages = []
    for i in range(0, timespan * 100):
        voltages.append(round(((_get_raw_reading() * 3300) / 1024),0))
        time.sleep(0.01)
    avg_voltage = sum(voltages) / len(voltages)
    inches = _convert_to_inches(avg_voltage, slope, intercept)
    return inches

if __name__ == "__main__":
    '''
    Debugging.
    '''
    reading_interval = 1
    regression = _calibrate()
    print "Debugging; press Ctrl+C at any time to stop."
    print "A new reading will be printed every", reading_interval, "seconds."
    try:
        while True:
            # Store multiple voltages to smooth out noise.
            # Voltages are measured in mV.
            voltages = []
            for i in range(0, reading_interval * 100):
                voltages.append(round(((_get_raw_reading() * 3300) / 1024),0))
                time.sleep(0.01)
            avg_voltage = sum(voltages) / len(voltages)
            now = datetime.datetime.now()
            timestamp = now.strftime('%Y_%m_%d_%H_%M_%S')
            depth = _convert_to_inches(avg_voltage, regression[0], regression[1])
            print "Time:", timestamp, "Inches:", depth
    except KeyboardInterrupt:
        print "\nCaught KeyboardInterrupt; stopping debugging."
    except Exception as e:
        print "Exception caught: ", e