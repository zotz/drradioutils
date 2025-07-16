#!/bin/bash
# rivreqm3.sh 
# from rivreqsys.sh
# lives on m3
# runs once an hour from cron
# run this at the top of the hour.

source keyvars.txt


#let h=$(date +%-k)*3600000
#let h=$(date +%-k)
let h=$(TZ=":US/Eastern" date +%-k)
let m=$(date +%-M)*60000
let s=$(date +%-S)*1000
let ms=$h+$m+$s

NOWDATE=`date +%Y_%m_%d`

#echo $NOWDATE "-" $h > /home/admin5z/public_html/bonsongreq/hold/$NOWDATE"-"$h".txt"

rm -f /var/www/html/rivreq/hold/*.txt
#touch /var/www/html/rivreq/songrequests.txt
touch /var/www/html/rivreq/hold/songrequests.txt
#chmod 666 /var/www/html/rivreq/songrequests.txt
#chown www-data:www-data /var/www/html/rivreq/songrequests.txt
chmod 666 /var/www/html/rivreq/hold/songrequests.txt
# chown www-data:www-data /var/www/html/rivreq/hold/songrequests.txt


rfile="/var/www/html/rivreq/songrequests.txt"

if [ ! -s "$rfile" ]; then
  echo "File '$rfile' is empty or does not exist."
  cp /var/rivreq/m3/srtemp.txt /var/www/html/rivreq/hold/songrequests.txt
else
  echo "File '$rfile' is not empty."
  mv /var/www/html/rivreq/songrequests.txt /var/www/html/rivreq/hold/songrequests.txt
fi

# mv /var/www/html/rivreq/songrequests.tx? /var/www/html/rivreq/hold/

cp /var/www/html/rivreq/hold/songrequests.txt /var/www/html/rivreq/hold/$NOWDATE"-"$h".txt"

