#!/usr/bin/python

import ftplib

if __name__ == '__main__':
    host = '198.57.219.221' 
    user = 'pingpan@theparjanadistribution.com'
    password = 'wlx1134908'
    ftp_folder = '/home/theparja/pingpan/testFTP/'

    ##save picture and upload picture to server via FTP	
    session = ftplib.FTP(host)
    session.login(user, password)    
    session.pwd()
    file = open('test.jpg','rb')	# file to send
    myfolder = ftp_folder
    session.cwd(myfolder)
    session.storbinary('STOR ' + 'test.jpg',file)  # send the file
    file.close() # close file and FTP
    session.quit()
				
    ##verify camera function works
    print 'Uploaded picture'		

