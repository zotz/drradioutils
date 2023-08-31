#!/bin/bash
# rsx11vncdr.sh

export DISPLAY=:0.0

/usr/bin/gnome-terminal -- /usr/bin/x11vnc -rfbauth /home/rd/.vnc/passwd -display :0 -shared -forever -solid red
