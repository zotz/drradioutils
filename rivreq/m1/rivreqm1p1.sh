#!/bin/bash
# rivreqm1p1.sh
# runs once an hour from cron
# currently only handles outbound from m1 to m2
# should run at the top of each hour

source keyvars.txt

# How to choose songs for voting
# latest - rivreqlatestsongs.sh
# pick userdefined - rivreqpickud.sh
# pick sched code - rivreqpicksc.sh
pickmethod='rivreqlatestsongs.sh'


#/var/rivreq/m1/rivreqlatestsongs.sh > /var/rivreq/m1/latestsongs.txt
/var/rivreq/m1/$pickmethod > /var/rivreq/m1/chosensongs.txt

# ssh -p 22 m2user@m2hostname

#scp -P 22 /home/rd/latestsongs.txt m2user@m2hostname:/home/m2user/songrequests/latestsongs.txt

#cp /var/rivreq/m1/latestsongs.txt /var/www/html/rivreq/latestsongs.txt

scp /var/rivreq/m1/chosensongs.txt $m2user@$m2ip:/var/rivreq/m2/chosensongs.txt

rm -f /var/rivreq/m1/prevchosensongs.txt

cp /var/rivreq/m1/chosensongs.txt /var/rivreq/m1/prevchosensongs.txt

