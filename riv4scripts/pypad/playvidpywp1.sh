#!/bin/bash
# this is meant to send to another machine running vlc which has the videos in its /var/vid/ directory
# run vlc on that machine something like this:
# vlc -I rc --rc-host 0.0.0.0:4212
# vou can also run obs on that machine, capture desktop audio and the vlc windows and stream to 
# nginx with the rtmp module.
echo "---"
#echo "All the command-line parameters are: "$*"" >> /tmp/passedparamspywp1.txt
echo "All the command-line parameters are: "$*"" > /tmp/passedparamspywp1.txt
echo "==="
echo "Sending over $1.mp4"  >> /tmp/passedparamspywp1.txt
echo "add /var/vid/$1.mp4" | nc 192.168.86.145 4212
#echo "add /var/vid/$1.mp4" | nc -C 192.168.86.39 4212
#echo "$1.mp4" | nc 192.168.86.126 4212
#echo "$1.mp4" | nc -q 1 192.168.86.126 4213
#echo "$1.mp4" | nc -C -q 1 192.168.86.39 4213
#echo "$1.mp4" | nc -q 1 192.168.86.145 4213 &
#echo "$1.mp4" | nc -q 1 192.168.86.145 4212 &
#echo "$1.mp4" | nc 192.168.86.145 4213
exit 0
