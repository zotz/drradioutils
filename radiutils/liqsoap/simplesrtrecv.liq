#!/usr/bin/liquidsoap
# simplesrtrecv.liq
# for drew learning

    # Logging

    #set("log.file.path", "/home/pi/log/srtrecv.log")
    set("log.file.path", "/tmp/srtrecv.log")
    set("log.level",5)

# listen on port 7000 for an srt stream to be sent
radio = input.srt(bind_address = "0.0.0.0", port = 7000, content_type = "application/ogg")
# what I need to know: what are acceptable/proper options for application/ogg above
# how can I find this information on my own? Where and how di I look?

# Is what I am doing below the right way to handle this?
# should I be using a different type of file other than .avi?
radio = fallback([radio, single("fallback.avi")])

# how can I output locally? The below does not seem to want to work.
#output.gstreamer.audio_video(radio)
# the below may work for audio only
output.icecast( %opus(bitrate=32, samplerate=8000, frame_size=10.), host="192.168.86.139", port=8000, password="hackme", mount="srt.ogg", radio)

#can't get this to work
#output.icecast(%ogg(%theora, %vorbis), host="192.168.86.139", port=8000, password="hackme", mount="srt.ogg", radio)
# what all can I send to icecast (format wise) and how else to deal with it?
# an example I have found shows this sort of output:
# -f mpegts udp://239.0.0.2:1234?pkt_size=1316

