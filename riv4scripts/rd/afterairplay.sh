#!/bin/bash

rm aip.finished
touch aip.started
cd

mkdir /tmp/rivnan
chmod 777 /tmp/rivnan

rm /home/rd/.rdairplaylock
# this is trying to get the screen size correct when running headless
# but it is not currently working correctly
xrandr --fb 1920x1080
/bin/wmctrl -s 0
#/usr/bin/jackd -R -p16 -dalsa -dhw:NVidia -r48000 -p4096 -n3 &
sleep 10
# for some reason rivendell does not always show up in the jack graph
# so we restart it trying to fix that issue
sudo /root/restartriv.sh
sleep 20
# start up rdairplay (need to change the script name from afterairplay...)
/usr/bin/rdairplay &
sleep 30
#sudo /root/restartriv.sh
sleep 10
# realln need to change the name for this as it starts before rdairplay now.


#sleep 2

#  this next stuff loads my logs for today - nope. do the nowtest stuff below
#NOWDATE=`date +%Y_%m_%d`

# I think the below 2 LOGx= lines are not needed
# I think there is also a missing LOGx= (x=3) line that is also not needed
#LOG1="AP1_"$NOWDATE
#LOG2="AP2_"$NOWDATE
#LOG3="AP3_"$NOWDATE
#LOG4="AP4_"$NOWDATE
#LOG5="VID_"$NOWDATE



# I think the next 2 lines handle the not needed LOG2= line and the missing 
# and not needed LOG3= line.
# below runs Music Only stream on aux1 log
#/home/rd/nowtest_aux1.sh
# Below runs Instrumental Only stream on aux2 log
# take out for now
#/home/rd/nowtest_aux2.sh

cd
sleep 10

# The next line runs a glassgui for the main log stream which is the main
# BON music stream which feeds muester and then BONTV, Youtube etc.
#/usr/bin/glassgui --autostart --instance-name=stream &
#sleep 5

# The next line sets up the glassguis for the Aux 1 Log and the Aux 2 log etc.
/bin/wmctrl -s 1
#sudo /root/runglasscoder.sh
# v4 does not need to run all jackd stuff as root.
# runn the needed glasscoder scripts
~/runglasscoder.sh &
sleep 25
# run the scripts needed to connect the glasscoders in the jack graph
~/reconnectgc.sh &
sleep 15
# The next lines load in the various logs and starts them playing
/home/rd/nowtest_main.sh
sleep 10
/home/rd/nowtest_aux1.sh
sleep 10
/home/rd/nowtest_aux2.sh
sleep 10
/home/rd/nowtest_v101.sh
sleep 10
/home/rd/nowtest_v102.sh
sleep 20
# this is some simple audio processing for the streams
~/runaudprocs.sh &
sleep 20
# this script runs x11vnc
~/rsx11vncdr.sh &
sleep 5
# annnnd we're done
touch aip.finished

top

