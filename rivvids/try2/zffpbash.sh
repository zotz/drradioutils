#!/bin/bash
# zffpbash.sh

#echo "playing $1"

#ffplay /var/vid/$1

var=$(cat /home/pi/testme.txt)

echo $var
echo "playing /var/vid/$var"

ffplay -fs -autoexit /var/vid/$var
