#!/usr/bin/python

import os
import httplib
import time

def test():
    try:
        conn = httplib.HTTPConnection("www.google.com")
        conn.request("GET","/")
        response = conn.getresponse()
        return 0
    except:
        return 1    

def reconnect():
    os.system("netsh wlan disconnect")
    time.sleep(3)
    os.system("netsh wlan connect name=NAME ssid=SSID")

def monitor():
    while 1:
        if test() == 0:
            print time.ctime(time.time()) + ": ALL OK"
        else:
            print time.ctime(time.time()) +":Disconnected"
            reconnect()
        time.sleep(60)


if __name__ == "__main__":
    monitor()    
