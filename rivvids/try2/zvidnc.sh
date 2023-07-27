#!/bin/bash
# zvidnc.sh

mkfifo vidpipe

i=0

while true
do
	#nc -l -p 4213 > testme.txt
	nc -l -p 4213 > vidpipe
	#cat vidpipe | ~/./zffmprtmp.sh
	let i++
	echo "Number of videos played: $i"
done
