#! /bin/bash
# the below works but vlc closes down between videos try something else
#cvlc /var/vid/$1.mp4
# lets try netcat to a vlc running the rc interface like so:
# vlc -I rc --rc-host 0.0.0.0:8080
# and the netcat line wil be:
echo "add /var/vid/$1.mp4" | nc 192.168.86.224 4212

