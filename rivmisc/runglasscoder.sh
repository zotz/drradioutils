#!/bin/bash
# start qjackctl
# this is /root/runglasscoder.sh
# it needs to be set executeable
#
/usr/bin/qjackctl &
# run glasscoder stuff from restart script
/root/restartgc.sh
