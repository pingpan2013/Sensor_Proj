#!/usr/bin/python

#
# DESC:
# Get data from the smart-cup water level measurement sensor.
# Determine the status of the pump according to the returned data from sensor.
# Store the status to remote database for furthur uses.
# 
# DATE:
# 07/07/2014
#

import serial
import MySQLdb
import time
import sys
from datetime import datetime

import conf
import server_conn

def store_data_to_local(file, status, vol, curTime):
    text = str(status) + "," + str(vol) + "," + str(curTime) + "\n"
    file.write(text)
    
    print "Stored data locally!"

def create_table(cur):
    create_table_sql = "create table if not exists waterLevelInfor(\
                            id int(11) auto_increment primary key,\
                            status varchar(20) not null,\
                            volume varchar(20) not null,\
                            curTime timestamp default current_timestamp)"
    cur.execute(create_table_sql)
    print "Created table!"

def store_data_to_server(cur, status, vol):
    insert_table_sql = "insert into waterLevelInfor(\
                            status, volume)\
                        values (" + str(status) + ", " + str(vol) + ")"
    cur.execute(insert_table_sql)
    print "Uploaded data to database!"

def determineWaterLevel(resis):
    '''
    Determine the water level according to the resistance value returned from the sensor
    Return the level of the water, [0, 1, 2, 3, 4, 5, 6]
    '''
    if resis <= 1000:
        return 5
    elif resis > 1000 and resis <= 1400:
        return 4
    elif resis > 1400 and resis <= 1800:
        return 3
    elif resis > 1800 and resis <= 2200:
        return 2
    elif resis > 2200 and resis <= 2600:
        return 1
    else:
        return 0

def get_and_store_data():
    '''
    Get data from the usb port connected with UNO board
    Then record and process the data collected
    '''
    pre_zone = -1;

    try:
        while True:   
            curTime = datetime.now()
            curTime = curTime.strftime('%Y_%m_%d_%H_%M_%S')
            
            file = open("./water_level.txt", "a+")
            conn = server_conn.connect_db(conf.DB['database'])
            seri = serial.Serial(conf.sc_port, conf.sc_baud)
            
            with conn, seri, file:
                line = seri.readline()
                data = line.split(',')
                if len(data) != 2:
                    print "Wrong Values! Beginning the next collection!"
                    continue
                else:
                    res = float(data[0])
                    vol = float(data[1])
                    print "Resistance: " + str(res) + ", Vol: " + str(vol)
            
                status = determineWaterLevel(res)
                print "Water Level: " + str(status)
                
                if pre_zone != status:
                    cur = conn.cursor()
                    create_table(cur)
                    store_data_to_local(file, str(status), str(vol), curTime)
                    store_data_to_server(cur, str(status), str(vol))
                    pre_zone = status
                    print "================================================"
                else:
                    print "Same water level!"
                    print "================================================"

                time.sleep(10)
    except IOError:
        print "I/O Error in opening the file!"
    except MySQLdb.Error, e:
        print "MySQL Error [{0}]: {1}".format(e.args[0], e.args[1]) 
    finally:
        if file.closed == False:
            file.close()
        
        if seri.isOpen() == True:
            seri.close()
        
        if conn.open == False:
            conn.close()
        print "All Interfaces are closed! Exiting ..."

if __name__ == "__main__":

    if get_and_store_data() == False:
        print "Move On..."
    else:
        print "Finished Processing!"




