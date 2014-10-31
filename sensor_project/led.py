#!/usr/bin/env python

#
# File Name: led.py
#
# Desc:
# Functions for LED control
#
# Date: September 28, 2014
#

import RPi.GPIO as GPIO

LED_YELLOW = 25    # Led that powers on when code starts
LED_GREEN = 23     # Led that powers on when there is internet

def control_LED(pin_num, ifOn):
    '''
    Control the LED light according to the pin number
        if ifOn = True, to turn it on
        else to turn it off
    '''
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_num, GPIO.OUT)
    GPIO.output(pin_num, ifOn)

def turn_LED_on(pin_num):
    '''
    Turns on the LED light according to the pin number
    '''
    control_LED(pin_num, True)

def turn_LED_off(pin_num):
    '''
    Turns off the LED light according to the pin number
    '''
    control_LED(pin_num, False)