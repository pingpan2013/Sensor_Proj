#!/bin/bash


for (( c=1; c<10; c++))
do
    raspistill -o $c'.jpg'
    sleep 2
    rm -f $c'.jpg'
done
