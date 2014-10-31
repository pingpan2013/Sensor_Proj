#!/bin/bash

# This script makes it easy to tell if the SensorBox software is currently
# running.

# Author: Christopher Kyle Horton
# Last modified: 10/6/2014

ps aux | grep python | grep -v grep
GREPRESULT=$?
if [[ $GREPRESULT -eq 0 ]] ; then
	echo "Yes"
else
	if [[ $GREPRESULT -eq 1 ]] ; then
		echo "No"
	else
		echo "An error occurred."
	fi
fi