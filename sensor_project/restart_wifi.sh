#!/bin/bash

#
# Reconnect Wifi with Network_ID and Wireless_Key
#

ifconfig wlan0
iwconfig wlan0 essid NETWORK_ID key WIRELESS_KEY
dhclient wlan0
