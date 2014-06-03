#!/usr/bin/python

#
# DESC:
# Get data from the CT(Current Transformer) Sensor.
#
#


import serial
import MySQLdb
from datetime import datetime

import conf

def connect_db(database):
    '''
    Build connection to the given database
    '''
    conn = MySQLdb.connect(conf.DB['host'],
                           conf.DB['user'],
                           conf.DB['password'],
                           database)
    
    print 'Connected to database!'
    return conn

def store_data_to_local(file, data):
    text = "Apparent Power: " + data[0] + ", IRMS: " + data[1] + "\n"
    file.write(text)



def create_table(cur):
    create_table_sql = "create table if not exists curInfo(\
                            id int(11) auto_increment primary key,\
                            power float not null,\
                            irms float not null,\
                            curTime timestamp default current_timestamp)"
    
    cur.execute(create_table_sql)



def store_data_to_server(cur, data):
    insert_table_sql = "insert into curInfo(power, irms)\
                        values({0}, {1})".format(data[0], data[1])
    
    cur.execute(insert_table_sql)

def get_and_store_data():
    # Build connection and get current data from USB port
    seri = serial.Serial(conf.ct_port, conf.ct_baudrate)
    
    # Open the file for storing data locally
    try:
        file = open("./res_data/ct_data.txt", "a+")
        print "Local file opened!"
    except IOError:
        print "I/O Error in opening the file!"

    # Connect to database for storing data remotely to the server
    conn = connect_db(conf.DB['database_c'])
    with conn:
        cur = conn.cursor()
        create_table(cur)
        while True:    
            #curTime = datetime.now()
            #curTime = curTime.strftime('%Y_%m_%d_%H_%M_%S')
            line = seri.readline()
            data = line.split()

            if len(data) != 2:
                print "Wrong Values!"
                continue
            
            print data[0] + ", " + data[1]

            store_data_to_local(file, data)
            store_data_to_server(cur, data)
        # END WHILE    
    
    file.close()
    conn.close()




if __name__ == "__main__":

    get_and_store_data()


