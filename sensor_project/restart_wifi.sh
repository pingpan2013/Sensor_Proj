#!/bin/sh

#
# Script to config wifi
#

ifconfig wlan0
iwconfig wlan0 essid NETWORK_ID key PASSWORD
dhclient wlan0
