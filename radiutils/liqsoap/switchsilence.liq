#!/usr/bin/liquidsoap
# switchsilence.liq
# snip
# The metadata (Cart Name) for the break will determine which playlist gets played
# at the client end.
# Seems to be sort of working As of Feb 14/2015
# Need to sort out reliability issues.

    # Logging

    set("log.file.path", "/tmp/switchsilence.log")
    #set("log.syslog", true)
    set("log.level",3)
    #set("log.syslog.facility","DAEMON")
    #set("log.syslog.program","liquidsoap")
    #set("log.unix_timestamps",true)
    set("scheduler.log",true)
    set("scheduler.fast_queues",3)
    set("scheduler.generic_queues",6)
    set("server.telnet",true)

# define transitions to and from stream
default_dj_fade = ref 0.

def to_break(a,b) =
  log("transition TO_BREAK called...")
  source.skip(b)
  add(normalize=false,
     [ sequence([ blank(duration=0.01),
                   fade.initial(duration=!default_dj_fade, b) ]),
        a ])
end


def to_stream(a,b) =
  log("transition TO_STREAM called...")
  add(normalize=false,
     [ sequence([ blank(duration=0.01),
                   b ]),
        fade.final(duration=!default_dj_fade, a) ])
end


# set up for metadata switching
breakz = ref ["COOL"]

#specify the icecast stream as an input


# Below is BON museter
# change this to a stream you can control the metadata on ignaciovenezia

stream = input.http("http://192.184.9.158:8240/stream")


# try some breaks
# create these directories and put some "silence" in at least one of them ignaciovenezia

break1 = playlist(mode="normal",conservative=true, reload_mode="watch","/var/audio/traffic/break1/")
break2 = playlist(mode="normal",conservative=true, reload_mode="watch","/var/audio/traffic/break2/")
break3 = playlist(mode="normal",conservative=true, reload_mode="watch","/var/audio/traffic/break3/")
break4 = playlist(mode="normal",conservative=true, reload_mode="watch","/var/audio/traffic/break4/")



# amplify the breaks
break1 = amplify(1.3,override="replay_gain",break1)
break2 = amplify(1.3,override="replay_gain",break2)
break3 = amplify(1.3,override="replay_gain",break3)
break4 = amplify(1.3,override="replay_gain",break4)

#specify the fail over file (could change this to be a template or directory of files)
# make this file for testing ignaciovenezia
failover = mksafe(single("/var/audio/emergency/EnergencyMix1.mp3"))


def f(x) =
    (snd(x))
end


# ignaciovenezia - if you leave these print statements and launch the script from a
# terminal, you should see when metadata changes...
def on_meta (meta)
    print (meta)
    breakz := list.map(f,meta)
    print (!breakz)
    print (!breakz == [" - Break1 - "])
    print (!breakz == [" - Break2 - "])
    print (!breakz == [" - Break3 - "])
    print (!breakz == [" - Break4 - "])
end


stream = on_metadata(on_meta, stream)


radiostream = switch (track_sensitive=false, transitions=[to_break, to_break, to_break, to_break, to_stream], [
  ({ (!breakz == [" - Break1 - "]) }, break1),
  ({ (!breakz == [" - Break2 - "]) }, break2),
  ({ (!breakz == [" - Break3 - "]) }, break3),
  ({ (!breakz == [" - Break4 - "]) }, break4),
  ({ (true) }, stream)
])


#Specify what to switch to when silence is detected
radiostream = fallback(track_sensitive=false, [radiostream, failover])

dummystream = fallback(track_sensitive=false, [stream, failover])

# Output to ALSA (the pi's audio)
output.alsa(device="hw:1,0", radiostream)
#output.alsa(radiostream)

# try this to keep stream checking metadata
output.dummy(dummystream)

