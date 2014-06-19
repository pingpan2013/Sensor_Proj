Sensor Box Project
================================================

Sensor Box project for the summer internship in Parjana. 

Used python codes to gather data from different kinds of sensors, namely moisture sensor, humidity sensor, camera and current sensor. Configured the database and ftp parts in server, and stored the data both locally and remotely for furthur uses in water management field. Also wrote scripts to control the data collection processes.

In the end, it should work like this: Once plugged in the power for the Raspberry PI Board, the micro computer(loaded with customized Linux system) within the board will boot up and run the codes automitically to gather and store the necessay data. After 15mins, the micro computer will reboot to begin another cycle.

Related Sensors and Boards
------------------------------
The sensors we used including humidity sensor, moisture sensor, camera sensor, and current sensor. The detailed sensors information is as follows:

* [The DHT22 Humidity Sensor](http://www.adafruit.com/products/385)
* [DS18B20 Temperature Sensor](https://learn.adafruit.com/downloads/pdf/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing.pdf)
* [Moisture Sensor](http://www.abra-electronics.com/products/SEN0114-Soil-Moisture-Sensor-(Arduino-Compatible)-Immersion-Gold.html)
* [Raspberry Pi Camera Board](http://www.adafruit.com/products/1367)
* [YHDC SCT-013-000 Current Transformer](http://openenergymonitor.org/emon/buildingblocks/report-yhdc-sct-013-000-current-transformer)

The current sensor is embeded within the Arduino UNO board, and the rest of the boards are embedded in the Raspberry board: 

* [Arduino UNO Board](http://arduino.cc/en/Main/ArduinoBoardUno) 
* [Adafruit Raspberry Pi Board](http://www.adafruit.com/categories/105)

##Pre Requisites
-----------------------------------------

**Python Libraries**
* [API for DHT22 Humidity Sensor](https://github.com/adafruit/adafruit-raspberry-pi-python-code/#adafruits-raspberry-pi-python-code-library)
* [API for Current Transformer](https://github.com/openenergymonitor/EmonLib)
* [API for DS18B20 Temperature Sensor](https://github.com/timofurrer/ds18b20)
* [API for Raspberry PI Camera](http://picamera.readthedocs.org/en/latest/api.html)

**Software**
* [The Arduino Software Platform](http://arduino.cc/en/Main/Software)

##Group Members
* Pingpan Cheng
* George Grzywacz

##License
* GNU Licence


