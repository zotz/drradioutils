#!/usr/bin/liquidsoap
# jack2iceopus.liq
# demo for tristan on #savonet on freenode irc

    # Logging

    #set("log.file.path", "/home/pi/log/liquidsoap.log")
    set("log.file.path", "/tmp/jack2iceopus.log")

    # to get this to work, add the user pi to the liquidsoap group
    # and sudo chmod 775 /var/log/liquidsoap/
    # this will allow the logfile to be written.

#    set("log.syslog", true)
    set("log.level",5)
    #set("log.level",3)
#    set("log.syslog.facility","DAEMON")
#    set("log.syslog.program","liquidsoap")
#    set("log.unix_timestamps",true)
#    set("scheduler.log",true)

# get stream from jackd on local machine
#radio = input.jack(id="livewithopus")
#specify the icecast stream as an input
# pull from museter is line below
radio = input.http("http://192.184.9.158:8240/stream")



# try capture alsa - problem already busy
#output.icecast(%vorbis, host = "localhost", port = 8000, password = "hackme", mount = "liq.ogg", input.alsa(device="hw:1,0"))
# try capture jack, output to icecast ogg
#output.icecast(%vorbis, host = "localhost", port = 8000, password = "hackme", mount = "liq.ogg", radio)
# try capture jack, output to icecast mp3
#output.icecast(%mp3(bitrate=96), mount="/stream96.mp3", host="localhost", port=8000, password="hackme", radio)
#output.icecast(%mp3(bitrate=128), mount="/stream.mp3", host="localhost", port=8000, password="hackme", radio)
#output.icecast(%mp3(bitrate=256), mount="/stream.mp3", host="localhost", port=8000, password="hackme", radio)
output.icecast(%mp3(bitrate=256), mount="/streamplus.mp3", host="localhost", port=8000, password="hackme", radio)


# tristan, if you adjust the two uncommented lines below to point to your icecast server and etc. it should work...
# dual output to opus
#output.icecast(%opus(samplerate=8000, frame_size=10, bitrate=128), mount="low_latency.ogg", host="localhost", port=8000, password="hackme", radio)
# output.icecast(%opus(bitrate=128, samplerate=8000, frame_size=10.), mount="/low_latency.ogg", host="localhost", port=8000, password="hackme", radio)
output.icecast(%opus(bitrate=128, samplerate=8000, frame_size=10.), mount="/low_latency.ogg", host="localhost", port=8000, password="hackme", radio)
output.icecast(%mp3(bitrate=256), mount="/streamplus.mp3", host="localhost", port=8000, password="hackme", radio)

# Output to ALSA (the pi's audio)
#output.alsa(device="hw:0,0", radiostream)
