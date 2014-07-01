#!/usr/bin/python

#
# DESC:
# The module is responsible for storing the data into the remote 
# ftp and database server.
#

import MySQLdb
import ftplib
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
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.loin(path, f))]
    for i in files:
        print i
    return files

def store_data_to_ftp(filename):
    '''
    Connect to the FTP server, and then store the pictures 
    data to the server, a backup to the local directory is needed
    '''
    # Connect to the FTP server
    session = ftplib.FTP(conf.FTP_Server['host'],
                         conf.FTP_Server['user'],
                         conf.FTP_Server['password'])
    
    print 'Connected to FTP server'

    # Access the target directory and send the picture
    #session.pwd()
    #file = open(conf.pi_folder_1 + filename, 'rb')
    #session.cwd(conf.FTP_Server['ftp_folder'])
    #session.storbinary('STOR ' + filename, file)
    #file.close()
    files = check_folder(conf.pi_folder_1)
    files.append(filename)

    session.pwd()
    for file in files:
        file2send = open(conf.pi_folder_1 + file, 'rb')
        session.cwd(conf.FTP_Server['ftp_folder'])
        session.storbinary('STOR ' + file, file2send)
        print "Uploaded picture" + file
        file2send.close()

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
    
    print 'Connected to database!'
    return conn

def store_data_to_db(temp_f,        # The temperature data
                     humidity,      # The humidity data
                     moistureA,     # The mositure data from PinA
                     moistureB,     # The moisture data from PinB
                     moistureC):    # The mositure data from pinC
    '''
    Store the data(humidity, moisture, etc) to the database
    First create the corresponding SQL codes
    Then execute them
    '''
    conn = connect_db(conf.DB['database'])
    with conn:
        cur = conn.cursor()
        create_table_sql = "CREATE TABLE IF NOT EXISTS 85_Lake_Basement_1(\
                                id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,\
                                PI_id TINYINT(6),\
                                Location VARCHAR(255),\
                                Temperature_Internal FLOAT NOT NULL,\
                                Humidity_Internal FLOAT NOT NULL,\
                                Moisture_A FLOAT NOT NULL,\
                                Moisture_B FLOAT NOT NULL,\
                                Moisture_C FLOAT NOT NULL,\
                                Time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)"
        
        #select_table_sql = 'SELECT * FROM Mettetal_2'
        insert_table_sql = "INSERT INTO 85_Lake_Basement_1(\
                                PI_id, Temperature_Internal,\
                                Humidity_Internal, \
                                Moisture_A, Moisture_B, Moisture_C, Location)\
                            VALUES("+str(conf.PI_id)+", "+str(temp_f)+", "   +str(humidity)+", "\
                                    +str(moistureA)+", " +str(moistureB)+", "+str(moistureC)+",\
                                    'Test Site 1')"
        cur.execute(create_table_sql)
        cur.execute(insert_table_sql)

        print "Uploaded data!"  



