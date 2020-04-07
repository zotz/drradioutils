#!/usr/bin/liquidsoap
# skiptest.liq
# for tristan setup

    # Logging

    set("log.file.path", "/home/pi/log/skiptest.log")
    set("log.level",5)


set("harbor.bind_addr", "0.0.0.0")
radio = mksafe(playlist("playlist.pls",conservative=true,length=1.0))
def skip_song(~protocol,~data,~headers,uri) =   source.skip(radio)   http_response(     protocol=protocol   ) end
# Expose skip command via HTTP
harbor.http.register(port=8002,method="GET","/skip",skip_song)
output.icecast(   %vorbis,   host = "localhost",   port = 8000,   password = "hackme11212!",   mount = "radio.ogg",   radio )
output.icecast(%opus(bitrate=32, samplerate=8000, frame_size=10.), mount="/low_latency.ogg", host="localhost", port=8000, password="hackme11212!", radio)
#output.alsa(bufferize=false,radio)
#output.alsa(radio)
# Output to jack
output.jack(id = "voip",radio)
# try output srt test
#output.srt(id = "srt1", host = "192.168.86.67", radio)
