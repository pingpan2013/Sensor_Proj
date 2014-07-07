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
from datetime import datetime

import conf
import server_conn

def store_data_to_local(file, status, curTime):
    text = "Status: " + str(status) + "  Timestamp: " + str(curTime) + "\n"
    file.write(text)


def create_table(cur):
    create_table_sql = "create table if not exists currentInfor(\
                            id int(11) auto_increment primary key,\
                            status varchar(20) not null,\
                            curTime timestamp default current_timestamp)"
    
    cur.execute(create_table_sql)


def store_data_to_server(cur, status):
    insert_table_sql = "insert into currentInfor(status) values (%s)"
    args = (status)
    cur.execute(insert_table_sql, args)


def determineIfOn(pre_power, cur_power):
    if pre_power == -1:
        return "off"
    elif float(cur_power) - float(pre_power) >= 2.00:
        return "on"
    else:
        return "off"

def get_and_store_data():
    pre_power = -1
    
    # Build connection and get current data from USB port
    seri = serial.Serial(conf.ct_port, conf.ct_baudrate)
    
    # Open the file for storing data locally
    try:
        file = open("./res_data/ct_on_data.txt", "a+")
    except IOError:
        print "I/O Error in opening the file!"

    # Connect to database for storing data remotely to the server
    try:
        conn = server_conn.connect_db(conf.DB['database_c'])
        cur = conn.cursor()
        create_table(cur)
        while True:    
            curTime = datetime.now()
            curTime = curTime.strftime('%Y_%m_%d_%H_%M_%S')
            line = seri.readline()
            data = line.split()
            
            if len(data) != 2:
                print "Wrong Values!"
                continue
            
            status = determineIfOn(pre_power, float(data[0]))
            
            print data[0] + ", " + data[1]
            print status

            store_data_to_local(file, str(status), curTime)
            store_data_to_server(cur, str(status))
            
            pre_power = data[0]
            time.sleep(2)
    except MySQLdb.Error, e:
        print "MySQL Error [%d]: %s".format(e.args[0], e.args[1]) 
        return False
    except:
        print "Exception Happened: ", sys.exc_info()[0]
        return False
    finally:
        file.close()
        conn.close()
        print "File and Connection closed!"

if __name__ == "__main__":

    if get_and_store_data() == False:
        print "Move On..."


