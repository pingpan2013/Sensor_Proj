#!/bin/bash
# Clean out data and logs, so it's like we are running fresh.

if [ "$(id -u)" != "0" ]; then
	echo "You must be root to run this script."
	exit 1
fi
echo "WARNING! This will wipe out the local data, pictures and log file(s)."
read -p "Continue (y/n)? " choice
case "$choice" in 
y|Y )
	FILESLOC="/home/pi/Desktop"
	sudo rm -f $FILESLOC/sensorbox*_data.csv
	sudo rm -f $FILESLOC/sensorbox.log
	sudo rm -f $FILESLOC/sensorbox_previous.log
	sudo rm -rf $FILESLOC/pictures_online/
	sudo rm -rf $FILESLOC/pictures_offline/
	echo "Cleaning complete."
	;;
n|N )
	;;
* )
	echo "Invalid input."
	;;
esac
