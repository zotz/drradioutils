#!/bin/bash
# rds.sh
# drew Roberts
# Example script using the now part of Rivendell's Now and Next data
# to update the RDS data for a station

testr="1"

# set the ip address of the machines that handles RDS
rdsIP="192.168.1.123"


# read .sngdata file to retrive info
title=$(sed -n '1p' < /home/rd/.sngdata)
artist=$(sed -n '2p' < /home/rd/.sngdata)
grp=$(sed -n '3p' < /home/rd/.sngdata)
grp=$(echo $grp|tr -d '\r')
album=$(sed -n '4p' < /home/rd/.sngdata)



cartist=$(echo $artist|tr -d '\r')
ctitle=$(echo $title|tr -d '\r')




RadTxt="DPS=$ctitle by $cartist"
CallTxt="DPS=88.8 BAHAMIAN O SUMPTIN                                                                                                                                  "

echo $RadTxt > /home/rd/.rdstxt


while true
do
	sleep 2

	echo $RadTxt
	echo $testr
	echo -ne $RadTxt | nc $rdsIP 22201 &

	{
	if [ "$testr" = "1" ]; then
		echo $RadTxt
	fi
	}


	sleep 30

	#let's try updating RDS from this script for now

	echo -ne $CallTxt | nc $rdsIP 22201 &
	{
	if [ "$testr" = "1" ]; then
		echo $CallTxt
	fi
	}

	sleep 30

	#let's try updating RDS from this script for now

	echo -ne $RadTxt | nc $rdsIP 22201 &
	{
	if [ "$testr" = "1" ]; then
		echo $RadTxt
	fi
	}


done
exit
