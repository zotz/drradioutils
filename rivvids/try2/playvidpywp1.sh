#!/bin/bash
echo "---"
#echo "All the command-line parameters are: "$*"" >> /tmp/passedparamspywp1.txt
echo "All the command-line parameters are: "$*"" > /tmp/passedparamspywp1.txt
echo "==="
echo "Sending over $1.mp4"  >> /tmp/passedparamspywp1.txt
# below two lines will send to my ubuntu box to vlc per note 1 comment at the bottom
#echo "add /var/vid/$1.mp4" | nc 192.168.86.145 4212
echo "add /var/vid/$1.mp4" | nc 192.168.86.39 4212
# the below lines are attempts to send to my PI4 box and duplicate the functions of the ubuntu box
# per note 1 at the bottom. see the z*.sh files for current attempts and notes.
#echo "$1.mp4" | nc 192.168.86.126 4212
#echo "$1.mp4" | nc -q 1 192.168.86.126 4213
#echo "$1.mp4" | nc -q 1 192.168.86.39 4213
#echo "$1.mp4" | nc 192.168.86.145 4213


# note 1
Run vlc like this
# vlc -I rc --rc-host 0.0.0.0:4212
# vlc is set to run full screen, not titles, osd, etc. set it how you like
# note 1.1
# I also run nginx with the rtmp module on this ubuntu box
# note 1.2
# I can also run obs on this ubuntu box which can then stream with rtmp to the nginx

exit 0
