#!/bin/bash
# zffmprtmp.sh
# sample below
# ffmpeg -re -i crowdrun.mp4 -c:v libx264 -c:v aac -f flv rtmp://localhost/show/stream
# -c:v h264 -g $GOP -b:v $CBR -preset ultrafast -c:a aac

     FPS="24" # target FPS
     GOP="48" # i-frame interval, should be double of FPS, 
     GOPMIN="24" # min i-frame interval, should be equal to fps, 
     THREADS="2" # max 6
     CBR="1000k" # constant bitrate (should be between 1000k - 3000k)

#echo "playing $1"

#ffplay /var/vid/$1

while true
do


    #var=$(cat /home/pi/testme.txt)
    var=$(cat /home/pi/vidpipe)
    echo $var
    echo "playing /var/vid/$var"

    ffmpeg -hide_banner -loglevel fatal -re -i /var/vid/$var -c:v libx264 -g $GOP -b:v $CBR -preset ultrafast -c:a aac -f flv "rtmp://192.168.86.145:1935/pushmungo/testthis2"

done
