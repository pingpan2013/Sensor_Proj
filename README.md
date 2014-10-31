#Sensor Box Project
================================================

Sensor box uses Python to gather data from different kinds of sensors, namely the moisture sensor, humidity sensor, camera, current sensor and water level measurement sensor. The database and FTP parts are configured in `sensor_project/server_conn.py`, and we store the data both locally and remotely for further uses in the water management field. Also wrote scripts to control the data collection processes.

In the end, it should work like this: Once the power for the Raspberry Pi board is plugged in, the microcomputer (loaded with the customized Linux system called [Raspbian](http://www.raspbian.org/)) within the board will boot up and run `sensor_project/sensor_box.py` automatically via cron to gather and store the necessary data. After 10 minutes, the main loop will begin another sampling cycle.

Also, this repository contains Python programs to help process the collected data. They can generate graphs for a given .csv file with specific formats. Also, there are several Bash (`.sh`) scripts which can be used to make certain maintenance tasks easier.

##Related Sensors and Boards
------------------------------
The sensors we used include a humidity sensor, moisture sensor, camera sensor, current sensor and water level measurement sensor. The detailed sensor information is as follows:

* [The DHT22 Humidity/Temperature Sensor](http://www.adafruit.com/products/385)
* [DS18B20 Temperature Sensor](https://learn.adafruit.com/downloads/pdf/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing.pdf)
* [Moisture Sensor](http://www.abra-electronics.com/products/SEN0114-Soil-Moisture-Sensor-(Arduino-Compatible)-Immersion-Gold.html)
* [Raspberry Pi Camera Board](http://www.adafruit.com/products/1367)
* [YHDC SCT-013-000 Current Transformer](http://openenergymonitor.org/emon/buildingblocks/report-yhdc-sct-013-000-current-transformer)
* [Liquid Level Sensor](http://www.adafruit.com/products/1786)

The current sensor and liquid level sensor are embeded within the Arduino UNO board, and the rest of the sensors are embedded in the Raspberry Pi board: 

* [Arduino UNO Board](http://arduino.cc/en/Main/ArduinoBoardUno) 
* [Adafruit Raspberry Pi Board](http://www.adafruit.com/categories/105)

##Prerequisites
-----------------------------------------

**Python Libraries**
* [API for DHT22 Humidity Sensor](https://github.com/adafruit/adafruit-raspberry-pi-python-code/#adafruits-raspberry-pi-python-code-library)
* [API for Current Transformer](https://github.com/openenergymonitor/EmonLib)
* [API for DS18B20 Temperature Sensor](https://github.com/timofurrer/ds18b20)
* [API for Raspberry PI Camera](http://picamera.readthedocs.org/en/latest/api.html)

**Software**
* [The Arduino Software Platform](http://arduino.cc/en/Main/Software)

Please see the [Wiki](https://github.com/ParjanaDistribution/SensorBox/wiki) for detailed documentation related to setting this up and using it.

##Group Members
* Pingpan Cheng <[pingpan@umich.edu](mailto:pingpan@umich.edu)> 
* George Grzywacz
* Christopher Kyle Horton <[chrishorton@parjanadistribution.com](mailto:chrishorton@parjanadistribution.com)>
* Joseph James Kielasa <[josephkielasa@parjanadistribution.com](mailto:josephkielasa@parjanadistribution.com)>

##License
* GNU GPLv3

##Cool Pictures
![PI](http://www.savagehomeautomation.com/storage/thumbnails/13113340-20696104-thumbnail.jpg?__SQUARESPACE_CACHEVERSION=1350765957292)
![PI](http://www.savagehomeautomation.com/storage/thumbnails/13113340-20696109-thumbnail.jpg?__SQUARESPACE_CACHEVERSION=1350766052558)
![PI](http://www.savagehomeautomation.com/storage/thumbnails/13113340-20696126-thumbnail.jpg?__SQUARESPACE_CACHEVERSION=1350766287652)
![PI](http://www.savagehomeautomation.com/storage/thumbnails/13113340-20696133-thumbnail.jpg?__SQUARESPACE_CACHEVERSION=1350766246395)
