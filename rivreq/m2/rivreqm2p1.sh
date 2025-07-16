#!/bin/bash
# rivreqm2p1.sh
# this should run once an hour from cron
# this is the only .sh script currently running on m2 (the middle machine)
# it uses rivreqm2results.php to do some of the work
# lets try running it at 3 minutes after the hour to give m1 time to send m2 the needed file.
# only handle the outbound to m3 in this part
# handle the inbound from m3 and the outbound to m1 in rivreqm2p2.sh

source keyvars.txt

#m2 to m3
scp /var/rivreq/m2/chosensongs.txt $m3user@$m3ip:/var/www/html/rivreq/chosensongs.txt

