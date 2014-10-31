## Sensor Project

Main code files for the sensor project, including:
- `humi_sensor.py`: Humidity sensor part
- `water_level.py`: Codes for getting data from the water level sensor data
- `curr_sensor.py`: Current sensor part
- `mois_sensor.py`: Moisture sensor part
- `temp_sensor.py`: Temperature sensor part
- `conf.py`: Configuration file for the project, including hardware interfaces information and server information.
- `genGraphs.py`: Codes for generating graphs according to a specific .csv file.

    - Usage:
        ```
        $ python genGraphs.py filename
        ```
        The file named filename should be a .csv file with a specific format. I'll attach a dicument to explain the format.

- `server_conn.py`: Codes for connecting with FTP server and database. There might be some problems with the function `store_data_to_ftp()` because I made some changes to let it upload all the files(including pictures when internet is off) in the folder when internet is on, but I haven't tested the codes when connecting with the board yet. Try to test it or you can just use the previous version of the code. It should work well.  
- `sensor_box.py`: Main codes for controlling the Raspberry PI board. If you want to change the way it collects data, just make modifications to this file. Usually it works like this: 

   - Once running, it will start collecting data and processing the data. After a certain time period, it will reboot to begin the next data sampling process.(If you got the power machines to control the power, just use this code. Otherwise you can use the codes we used in the lake house: let it reboot after collecting data for several times instead of rebooting every time. In this way we can minimize the times to reboot.)
