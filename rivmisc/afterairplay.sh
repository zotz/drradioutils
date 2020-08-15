#!/usr/bin/bash

cd

rm /home/rd/.rdairplaylock
/usr/bin/rdairplay &
touch afterairplay.begun

sleep 15

sudo /root/runglasscoder.sh &

sleep 30

NOWDATE=`date +%Y%m%d`

# I think the below 2 LOGx= lines are not needed
# I think there is also a missing LOGx= (x=3) line that is also not needed
LOG1="mainfm_"$NOWDATE
#LOG2="adins_"$NOWDATE

# I think the next 2 lines handle the not needed LOG2= line and the missing 
# and not needed LOG3= line.
# below runs Music Only stream on aux1 log
#/home/rd/nowtest_aux1.sh
# Below runs Instrumental Only stream on aux2 log
# take out for now
#/home/rd/nowtest_aux2.sh

cd
sleep 1

# The next line runs a glassgui for the main log stream which is the main
# BON music stream which feeds muester and then BONTV, Youtube etc.
#/usr/bin/glassgui --autostart --instance-name=stream &
#sleep 5

# The next line sets up the glassguis for the Aux 1 Log and the Aux 2 log etc.
#sudo /root/runglasscoder.sh
sleep 1
# The next line loads in the main log and starts it playing
/home/rd/nowtest_main.sh

# annnnd we're done
touch afterairplay.finished
top
