#!/bin/bash



# run glasscoder from here temporarily for main stream
#/usr/bin/glassgui --autostart --instance-name=streamtemp &


# run glasscoder for rdaidplay main log
#Airport1
/usr/bin/glassgui --autostart --instance-name=stap1 &




# run glasscoder for aux1 machine
# Airport2 from Aux 1 log
/usr/bin/glassgui --autostart --instance-name=stap2 &

# run glasscoder for aux2 machine
# Airport3 from Aux 2 log
/usr/bin/glassgui --autostart --instance-name=stap3 &

# run glasscoder for vlog101 machine
# Airport4 from Vlog 101
/usr/bin/glassgui --autostart --instance-name=stap4 &


# Instrumental Only stream - play from Aux 2 log
#/usr/bin/glassgui --autostart --instance-name=insonly &

sleep 5
# run stereo too
#/root/stereo_tool_gui_jack_64 &

sleep 15
echo "done sleeping, connecting now."
# playout_0 main log -> ghcmain - GlassP2 - without stereo tool
#jack_connect rivendell_0:playout_0L GlassP2:input_1
#jack_connect rivendell_0:playout_0R GlassP2:input_2
#jack_connect rivendell_0:playout_0L system:playback_1
#jack_connect rivendell_0:playout_0R system:playback_2


# playout_0 main log -> ghcmain - GlassP2 - with stereo tool
#jack_connect rivendell_0:playout_0L stereo_tool:in_l
#jack_connect rivendell_0:playout_0R stereo_tool:in_r
#jack_connect stereo_tool:out_l system:playback_1
#jack_connect stereo_tool:out_r system:playback_2
#jack_connect stereo_tool:out_l GlassP2:input_1
#jack_connect stereo_tool:out_r GlassP2:input_2



# playout_1 production machine -> stream1 - GlassP2
#jack_connect rivendell_0:playout_1L GlassP2:input_1
#jack_connect rivendell_0:playout_1R GlassP2:input_2
# playout_2 aux 2 log -> insonly - GlassIO
#jack_connect rivendell_0:playout_2L GlassIO:input_1
#jack_connect rivendell_0:playout_2R GlassIO:input_2
