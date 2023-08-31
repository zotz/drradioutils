#!/bin/bash
#Credentials for Rivendell Database
#Edit these as required
user="rduser"
pass="notletmein"
host="localhost"
db="Rivendell"

#Get the current time
let h=$(date +%-k)*3600000
let m=$(date +%-M)*60000
let s=$(date +%-S)*1000
let ms=$h+$m+$s
echo "MS: "$ms

#Get the current date formatted for the log name you use
NOWDATE=$(date +%Y_%m_%d)
#NOWDATE="V987fm_"$(date +%Y_%m_%d)
echo "NOWDATE: "$NOWDATE

#Get the actual log name my logs are 12052015_LOG so change this
#LOG_NAME1="V987fm_"$NOWDATE1
LOG_NAME="AP3_"$NOWDATE
echo "LOG_NAME: "$LOG_NAME

#Get the row count from the DB based on the current time
#let SQLRESULT=$(mysql --skip-column-names -u "$user" -p"$pass" -h "$host" "$db" -e "select LINE_ID from LOG_LINES where LOG_NAME = CONCAT('V987fm_',DATE_FORMAT(curdate(),'%Y%m%d')) and START_TIME BETWEEN ((TIME_TO_SEC(NOW())*1000)-60000) AND (TIME_TO_SEC(NOW())*1000)+(300*1000) LIMIT 1")

let SQLRESULT=$(mysql --skip-column-names -u "$user" -p"$pass" "$db" -e "select COUNT from LOG_LINES WHERE LOG_NAME = \"$LOG_NAME\" AND START_TIME >= $ms LIMIT 1";)-1

echo "SQLRESULT: "$SQLRESULT

#Send the RML command LL to load a log from the specified line
#rmlsend LL\ 1\ $NOWDATE\ $SQLRESULT\!
rmlsend LL\ 3\ $LOG_NAME\ $SQLRESULT\!

