#!/bin/bash
# Get the IP address of this Raspberry Pi.
echo "$( ifconfig wlan0 | grep "inet " | awk -F'[: ]+' '{print $4}' )"
