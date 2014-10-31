#!/bin/bash

# This script simplifies the upgrade process for SensorBox software.

# Author: Christopher Kyle Horton
# Last modified: 10/6/2014

if zenity --question --text="Upgrading SensorBox software will require reconfiguration afterwards. Proceed?"
then
	cd /home/pi/SensorBox/
	git checkout -- sensor_project/conf.py
	git pull
	./config_wizard.sh
fi