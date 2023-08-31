#!/bin/bash
export DISPLAY=:0.0
#
#/usr/bin/rdlogmanager -g -m -t -s ONAIR -d 1
#/usr/bin/rdlogmanager -g -t -s ONAIR -d 5
#/usr/bin/rdlogmanager -P -g -s ONAIR -d 0
#/usr/bin/rdlogmanager -P -t -s ONAIR -d 0
#/usr/bin/rdlogmanager -g -s musiconly -d 1
#/usr/bin/rdlogmanager -g -s insonly -d 1
#/usr/bin/rdlogmanager -g -s adinsert -d 1
/usr/bin/rdlogmanager -g -s A1 -d 1
/usr/bin/rdlogmanager -g -s A2 -d 1
/usr/bin/rdlogmanager -g -s A3 -d 1
/usr/bin/rdlogmanager -g -s A4 -d 1
/usr/bin/rdlogmanager -g -s video -d 1

exit 0

