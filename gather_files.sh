#!/bin/bash
# Gather recorded files into a tarball for copying.

DESKTOP="/home/pi/Desktop"
GATHEREDFOLDER="SensorBox_files"
GATHEREDPATH="$DESKTOP/$GATHEREDFOLDER/"
cd $DESKTOP/
mkdir $GATHEREDFOLDER
cp -r sensorbox*_data.csv $GATHEREDPATH
cp -r pictures_online $GATHEREDPATH
cp -r pictures_offline $GATHEREDPATH
tar -zcvf $GATHEREDFOLDER.tar.gz $GATHEREDPATH
