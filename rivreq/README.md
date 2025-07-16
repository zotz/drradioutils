Rivendell Request System

Start of README.md for rivreq

If you are running Rivendell as your Radio Automation System and you would like to let your listeners request from a list of songs you choose and to have the most popular choice play in the next hour, the Rivendell Request System could be for you.

It is currently a 3 machine system but it could be a 2 machine system.

The three machines are:

m1 - Rivendell machine.

m2 - raspberry pi that serves as a middle man.

m3 - web server that the users go to to interact with the system.

Cron is involved in the functioning of the system.

m1 crontab

0 * * * *  /var/rivreq/m1/rivreqm1p1.sh

m2 crontab

1 * * * *  /var/rivreq/m2/rivreqm2p1.sh
2 * * * *  /var/rivreq/m2/rivreqm2p2.sh

m3 crontab

0 * * * *  /var/rivreq/m3/rivreqm3.sh

I may need to have each machine have 2 scripts like m2 currently has.

Downstream: m1->m2->m3 to be handled in part 1.

Upstream: m3->m2->m1 to be handled in part 2.
