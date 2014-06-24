#!/bin/bash

# TEST HUMIDITY/TEMPERATURE SENSOR

for (( c=1; c<10; c++))
do
    sudo python Adafruit_DHT2.py 2302 17
done
