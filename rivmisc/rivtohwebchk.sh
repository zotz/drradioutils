#!/bin/bash
# rivtohwebchkp.sh
# near toh macro that calls this:
# RN /home/rd/rivtohwebchkp.sh
# SP 1000!
# adjust SP line smaller to your liking.
# schedule the macro just after every TOH in your log.
# It should download the text file from your webserver and leave a copy in /tmp.
# It hould also leave evidence of the download event in your web server's logs.

sudo -u rd /usr/bin/wget -O /tmp/station1chk.txt http://www.mydomain1.com/rivchks/station1chk.txt
