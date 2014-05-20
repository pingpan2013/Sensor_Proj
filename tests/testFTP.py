#!/usr/bin/python

from ftplib import FTP

if __name__ == '__main__':
    host = '198.57.219.221' 
    user = 'pingpan@theparjanadistribution.com'
    password = 'abcded'
    ftp_folder = '/testFTP/'

    # save picture and upload picture to server via FTP	
    session = FTP(host)
    session.login(user, password)    
    session.pwd()
    file = open('test.jpg','rb')
    myfolder = ftp_folder
    session.cwd(myfolder)
    session.storbinary('STOR ' + 'test.jpg',file)
    file.close() 
    session.quit()
				
    # verify camera function works
    print 'Uploaded picture !!'		

