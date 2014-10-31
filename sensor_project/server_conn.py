#!/usr/bin/python

#
# DESC:
# The module is responsible for storing the data into the remote 
# ftp and database server.
#

import os
import MySQLdb
import ftplib
import logging
import urllib2
import conf

def internet_on():
    '''
    Test if internet access is available
    Return true if available, otherwise return false
    '''
    try:
        response = urllib2.urlopen('http://74.125.228.100', timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

def check_folder(path):
    '''
    Check the given folder to list all the files
    Return all the files
    '''
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return files

def ftp_directory_exists(session, dir):
    '''
    Check if FTP directory exists (in current location).
    '''
    filelist = []
    session.retrlines('LIST', filelist.append)
    for f in filelist:
        if f.split()[-1] == dir and f.upper().startswith('D'):
            return True
    return False

def ftp_chdir(session, dir):
    '''
    Checks if the FTP directory exists, else creates it. Then switch to it.
    session is an object created by ftplib.FTP for the logged-in FTP connection.
    '''
    if not ftp_directory_exists(session, dir):
        try:
            session.mkd(dir)
        except ftplib.error_perm:
            # Don't throw a fit if it is already there for some reason
            # Source: http://stackoverflow.com/a/21193066
            pass
    session.cwd(dir)

def store_data_to_ftp(filename):
    '''
    Connect to the FTP server, and then store the pictures 
    data to the server, a backup to the local directory is needed
    '''
    # Connect to the FTP server
    session = ftplib.FTP(conf.FTP_Server['host'],
                         conf.FTP_Server['user'],
                         conf.FTP_Server['password'])
    
    # Access the target directory and send all the pictures
    files = check_folder(conf.offline_pictures_folder)
    files.append(filename)
    
    for file in files:
        with open(conf.offline_pictures_folder + file, 'rb') as file2send:
            ftp_chdir(session, conf.FTP_Server['ftp_folder'])
            session.storbinary('STOR ' + file, file2send)
            logging.debug("Uploaded picture" + file)
        os.system("rm -f {0}".format(file))
    
    # Disconnect 
    session.quit()


def connect_db(database):
    '''
    Build connection to the given database
    '''
    conn = MySQLdb.connect(conf.DB['host'],
                           conf.DB['user'],
                           conf.DB['password'],
                           database)
    return conn

def generate_creation_sql(temp_f, humidity, moistures, temps, water_depth):
    '''Construct the SQL used for creating the table.'''
    create_table_sql  = "CREATE TABLE IF NOT EXISTS " + conf.DB['table'] + "("
    create_table_sql += "id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,"
    create_table_sql += "PI_id TINYINT(6),"
    create_table_sql += "Location VARCHAR(255),"
    if temp_f != None:
        create_table_sql += "Temperature_Internal FLOAT NOT NULL,"
    if humidity != None:
        create_table_sql += "Humidity_Internal FLOAT NOT NULL,"
    if moistures != None:
        sensor_chr = 'A'
        for moisture in moistures:
            create_table_sql += "Moisture_" + sensor_chr + " FLOAT NOT NULL,"
            sensor_chr = chr(ord(sensor_chr) + 1)
    if temps != None:
        sensor_chr = 'A'
        for temp in temps:
            create_table_sql += "Temperature_" + sensor_chr + " FLOAT NOT NULL,"
            sensor_chr = chr(ord(sensor_chr) + 1)
    if water_depth != None:
        create_table_sql += "Water_Level FLOAT NOT NULL,"
    create_table_sql += "Time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)"
    return create_table_sql

def generate_insertion_sql(temp_f, humidity, moistures, temps, water_depth, timestamp=""):
    '''Construct the SQL used for inserting data records.'''
    insert_table_sql  = "INSERT INTO " + conf.DB['table'] + "("
    insert_table_sql += "PI_id, "
    if temp_f != None:
        insert_table_sql += "Temperature_Internal, "
    if humidity != None:
        insert_table_sql += "Humidity_Internal, "
    if moistures != None:
        sensor_chr = 'A'
        for moisture in moistures:
            insert_table_sql += "Moisture_" + sensor_chr + ", "
            sensor_chr = chr(ord(sensor_chr) + 1)
    if temps != None:
        sensor_chr = 'A'
        for temp in temps:
            insert_table_sql += "Temperature_" + sensor_chr + ", "
            sensor_chr = chr(ord(sensor_chr) + 1)
    if water_depth != None:
        insert_table_sql += "Water_Level, "
    if timestamp:
        insert_table_sql += "Time, "
    insert_table_sql += "Location) "
    insert_table_sql += "VALUES("
    insert_table_sql += str(conf.PI_id) + ", "
    if temp_f != None:
        insert_table_sql += str(temp_f) + ", "
    if humidity != None:
        insert_table_sql += str(humidity) + ", "
    if moistures != None:
        for moisture in moistures:
            insert_table_sql += str(moisture) + ", "
    if temps != None:
        for temp in temps:
            insert_table_sql += str(temp) + ", "
    if water_depth != None:
        insert_table_sql += str(water_depth) + ", "
    if timestamp:
        insert_table_sql += "'" + timestamp + "', "
    insert_table_sql += "'" + conf.location + "')"
    return insert_table_sql

def drop_table():
    '''Drop the table to clean up, in case we want to record different data.
    DO NOT CALL THIS DURING NORMAL PROGRAM EXECUTION!
    COULD CAUSE DATA LOSS!'''
    conn = connect_db(conf.DB['database'])
    with conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS " + conf.DB['table'])

def store_data_to_db(temp_f, humidity, moistures, temps, water_depth, timestamp=""):
    '''
    Store the data (humidity, moisture, etc) to the database
    First create the corresponding SQL codes
    Then execute them
    '''
    conn = connect_db(conf.DB['database'])
    with conn:
        cur = conn.cursor()
        create_table_sql = generate_creation_sql(temp_f,
                                                 humidity,
                                                 moistures,
                                                 temps,
                                                 water_depth
                                                )
        insert_table_sql = generate_insertion_sql(temp_f,
                                                  humidity,
                                                  moistures,
                                                  temps,
                                                  water_depth,
                                                  timestamp
                                                 )
        logging.debug("Table creation SQL: " + create_table_sql)
        logging.debug("Table insertion SQL: " + insert_table_sql)
        cur.execute(create_table_sql)
        cur.execute(insert_table_sql)
