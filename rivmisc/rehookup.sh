#!/bin/bash
# rehookup.sh
# make / remake jack connections for one of my rivendell setups
# I have been asked to post this as an example.

cd
sleep 5
echo "done sleeping, connecting now."
# playout_0 main log -> BON - GlassMain
jack_connect rivendell_2:playout_0L GlassMain:input_1
jack_connect rivendell_2:playout_0R GlassMain:input_2

sleep 5
# playout_0 aux 1 log -> musiconly - GlassMO
jack_connect rivendell_2:playout_1L GlassMO:input_1
jack_connect rivendell_2:playout_1R GlassMO:input_2

sleep 5
# playout_2 aux 2 log -> insonly - GlassIO
jack_connect rivendell_2:playout_2L GlassIO:input_1
jack_connect rivendell_2:playout_2R GlassIO:input_2

sleep 5
# playout_1 production machine -> stream1 - GlassP2
jack_connect rivendell_2:playout_3L GlassP2:input_1
jack_connect rivendell_2:playout_3R GlassP2:input_2
