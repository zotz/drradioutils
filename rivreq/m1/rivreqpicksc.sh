#!/bin/bash
# rivreqpicksc.sh

source keyvars.txt


# Newer - Riv 4.x
mysql --skip-column-names -u "$user" -p"$pass" "$db" -e "select NUMBER, TITLE, ARTIST from CART LEFT JOIN CART_SCHED_CODES ON CART.NUMBER = CART_SCHED_CODES.CART_NUMBER WHERE CART_SCHED_CODES.SCHED_CODE = 'SSG' ORDER BY RAND() LIMIT $numsongs";


# Older - Riv 2.x

#mysql --skip-column-names -u "$user" -p"$pass" "$db" -e "SELECT NUMBER, TITLE, ARTIST FROM CART WHERE SCHED_CODES LIKE '%G%' ORDER BY RAND() LIMIT $numsongs";

