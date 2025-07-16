#!/bin/bash
# rivreqm2p2.sh
# this should run once an hour from cron
# it uses rivreqm2results.php to do some of the work
# lets try running it at 6 minutes after the hour to give m3 to get
# the files we send it and do its thing
# handle the outbound to m3 in rivreqm2p1.sh
# handle the inbound from m3 and the outbound to m1 in this part

source keyvars.txt

# m3 to m2
# try scp
scp $m3user@$m3ip:/var/www/html/rivreq/hold/*txt /var/rivreq/m2/data/
# try wget
#wget -N -P /var/rivreq/m2/data -r -np -nd -R "index.html*" http://$m3ip/rivreq/hold/
#wget -N -P /var/rivreq/m2/data -r -np -nd -R "index.html" http://$m3ip/rivreq/hold/



shortcart=$(/var/rivreq/m2/rivreqm2results.php)
echo "here comes shortcart"
echo $shortcart
cart=$(printf %06d $shortcart)
echo "here comes cart"
echo $cart

echo $cart > /var/rivreq/m2/thishourrequest.txt


# m2 to m1
scp -P 22  /var/rivreq/m2/thishourrequest.txt $m1user@$m1ip:/var/rivreq/m1/thishourrequest.txt
