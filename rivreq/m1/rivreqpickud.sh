#!/bin/bash
# rivreqpickud.sh

source keyvars.txt


mysql --skip-column-names -u "$user" -p"$pass" "$db" -e "select NUMBER, TITLE, ARTIST from CART WHERE GROUP_NAME = 'MUSIC' AND USER_DEFINED = 'PK' ORDER BY number DESC LIMIT $numsongs";
