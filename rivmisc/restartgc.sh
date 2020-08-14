#!/bin/bash
# this is /root/restartgc.sh
# it needs to be executable


# run glasscoder from here temporarily for main stream
#/usr/bin/glassgui --autostart --instance-name=streamtemp &


# run glasscoder for rdlibrary production machine
/usr/bin/glassgui --autostart --instance-name=stream1 &

# run glasscoder for aux1 machine
# Music Only stream - play from Aux 1 log
/usr/bin/glassgui --autostart --instance-name=musiconly &

# Instrumental Only stream - play from Aux 2 log
/usr/bin/glassgui --autostart --instance-name=insonly &


sleep 5
echo "done sleeping, connecting now."
# playout_0 aux 1 log -> musiconly - GlassMO
jack_connect rivendell_1:playout_0L GlassMO:input_1
jack_connect rivendell_1:playout_0R GlassMO:input_2
# playout_1 production machine -> stream1 - GlassP2
jack_connect rivendell_1:playout_1L GlassP2:input_1
jack_connect rivendell_1:playout_1R GlassP2:input_2
# playout_2 aux 2 log -> insonly - GlassIO
jack_connect rivendell_1:playout_2L GlassIO:input_1
jack_connect rivendell_1:playout_2R GlassIO:input_2

