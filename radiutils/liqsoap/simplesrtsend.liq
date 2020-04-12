#!/usr/bin/liquidsoap
# simplesrtsend.liq
# for drew learning

    # Logging

    #set("log.file.path", "/home/pi/log/skiptest.log")
    set("log.file.path", "/tmp/srtsend.log")
    set("log.level",5)


# get some video in (right now just a test pattern
radio = mksafe(input.gstreamer.audio_video())
# one thing I would like to know is how to rake in a single video file or a playlist of video files to send along
# so far I am failing in all of my tries.


# send some video to another machine/script using srt
# there is a vm with nat involved and 15003 gets forwarded to 7000 on the vm
# lubuntu 19.10 on both ends
output.srt(id = "srt1", host = "192.168.86.86", port = 15003, %avi,radio)
# one thing I would like to learn is how to find out what options I have in place of %avi in thge line above
