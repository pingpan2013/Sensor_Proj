#!/bin/bash

# SensorBox Configuration Wizard
# This script makes it easy to configure new SensorBoxes prior to being
# deployed, after the code is installed.

# Author: Christopher Kyle Horton
# Last modified: 10/5/2014

#=============================================================================
# Variable declarations
#=============================================================================

TITLE="SensorBox Configuration Wizard"
DEBPACKAGES="build-essential python-dev python-pip python-mysqldb"
PIPPACKAGES="ds18b20 spidev"
CONF="sensor_project/conf.py"
CRONCMD="sudo python /home/pi/SensorBox/sensor_project/sensor_box.py &"
CRONJOB="@reboot $CRONCMD"
WALLPAPER="/home/pi/SensorBox/images/sensorbox_desktop.png"

trap "exit 1" TERM
export TOP_PID=$$

#=============================================================================
# Function definitions
#=============================================================================

abort_script() { kill -s TERM $TOP_PID ; }

setup_fail()
{
	if [ $# == 1 ]
	then
		TEXT="$1"
	else
		TEXT="SensorBox Configuration Wizard setup failed (unknown error)."
	fi
	TEXT="$TEXT Please re-run this wizard."
	zenity --error --title="$TITLE" --text="$TEXT"
	abort_script
}

configure_variable()
{
	# First argument is non-string variable in conf, second is new value
	sed -i "s/^$1 = .*/$1 = $2/" "$CONF"
}

configure_string()
{
	# First argument is string variable in conf, second is new value
	sed -i "s|^$1 = .*|$1 = \"$2\"|" "$CONF"
}

ask_is_using()
{
	# First argument is component name, second is conf variable name
	if zenity --question --title="$TITLE" --text="Is this SensorBox using a $1?"
	then
		configure_variable "$2" "True"
	else
		configure_variable "$2" "False"
	fi
}

show_message()
{
	zenity --info --title="$TITLE" --text="$1"
}

ask_how_many()
{
	# First argument is component name, second is conf variable name
	VALUE=`zenity --scale --text="How many $1 does this SensorBox have?" --value=0 --max-value=8`
	case $? in
		0)
			configure_variable "$2" $VALUE;;
		1)
			setup_fail "No value selected.";;
		-1)
			setup_fail "An unexpected error has occurred.";;
	esac
}

ask_for_string()
{
	# Argument 1: Message text
	# Argument 2: Default entry text
	# Argument 3: conf variable name
	VALUE=`zenity --entry \
	--title="$TITLE" \
	--text="$1" \
	--entry-text "$2"`
	case $? in
		1)
			setup_fail "Cannot continue configuration without value."
			;;
		-1)
			setup_fail
			;;
	esac
	configure_string "$3" "$VALUE"
}

#=============================================================================
# Main script
#=============================================================================

show_message "Welcome to the SensorBox Configuration Wizard!\n\nFirst, we will install some needed packages and change some module settings in the filesystem. This might take a few minutes. Please ensure you are connected to the Internet before proceeding."
sudo apt-get update | zenity --progress --title=$TITLE --text="Checking for updates..." --auto-close --pulsate
sudo apt-get upgrade -y | zenity --progress --title=$TITLE --text="Downloading and installing updates..." --auto-close --pulsate
sudo apt-get install $DEBPACKAGES -y | zenity --progress --title=$TITLE --text="Downloading and installing required Debian packages for SensorBox software..." --auto-close --pulsate
sudo pip install $PIPPACKAGES | zenity --progress --title=$TITLE --text="Downloading and installing required pip packages for SensorBox software..." --auto-close --pulsate
# Needed for SPI
sudo sed -i 's/blacklist spi-bcm2708/#blacklist spi-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf
# Needed for DHT humidity sensor
RUNFROM=$(pwd)
(
cd /home/pi/SensorBox/libraries/Adafruit_DHT_Driver_Python/bcm2835-1.36
./configure
make
sudo make check
sudo make install
cd ..
sudo python setup.py install 
)| zenity --progress --title=$TITLE --text="Setting up DHT driver..." --auto-close --pulsate
cd $RUNFROM

if [[ $(hostname | grep -Eq "parjanasensorbox[0-9]{1,}") ]];
then
	setup_fail "System hostname was not configured properly; aborting."
fi
PINUM=`hostname | sed 's/[^0-9]//g'`
configure_variable "PI_id" $PINUM
ask_is_using "camera" "using_camera"
ask_how_many "moisture sensors" "num_moisture_sensors"
ask_how_many "external temperature sensors" "num_temp_sensors"
ask_is_using "humidity sensor" "using_humidity_sensor"
ask_is_using "water level sensor" "using_water_level_sensor"
ask_for_string "Enter a short but descriptive location for this SensorBox:" \
"Test Site" \
"location"
ask_for_string "Enter a MySQL table name for this SensorBox to upload data to:" \
"Test_$PINUM" \
"table_name"
ask_for_string "Enter an FTP folder name for this SensorBox to upload data to:" \
"/Test/$PINUM/" \
"ftp_name"

# Set up sensor_box.py to run at reboot via cron
( crontab -l | grep -v "$CRONCMD" ; echo "$CRONJOB" ) | crontab -

# Change desktop wallpaper to show configuration was done
pcmanfm --set-wallpaper=$WALLPAPER --wallpaper-mode=stretch

show_message "Configuration complete! Your SensorBox will begin collecting data after the next reboot."
