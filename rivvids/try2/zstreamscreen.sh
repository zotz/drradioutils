#!/bin/bash
# zstreamscreen.sh
# /home/pi/streamscreen.sh
# stream the captured desktop screen to twitch / youtube / etc.




nginxstabledesktop() {
     INRES="1920x1080" # input resolution
     OUTRES="1920x1080" # output resolution
     FPS="24" # target FPS
     GOP="48" # i-frame interval, should be double of FPS, 
     GOPMIN="24" # min i-frame interval, should be equal to fps, 
     THREADS="2" # max 6
     CBR="1500k" # constant bitrate (should be between 1000k - 3000k)
     QUALITY="ultrafast"  # one of the many FFMPEG preset
     AUDIO_RATE="48000"
     # STREAM_KEY="$1" # use the terminal command Streaming streamkeyhere to stream your video to twitch or justin
     STREAM_KEY="testthis2"
     SERVER="pushmungo" # twitch server in frankfurt, see https://stream.twitch.tv/ingests/ for list
     
# Above plus metadata minus scale
     #ffmpeg -f x11grab -video_size 1920x1080 -framerate $FPS -i $DISPLAY -f jack -i ffmpeg -vf drawtext="fontfile=monofonto.ttf: fontsize=24: box=1: boxcolor=black@0.75: boxborderw=5: fontcolor=white: x=40: y=20: textfile=/home/pi/foo1.txt: reload=1" -c:v h264 -g $GOP -b:v $CBR -preset ultrafast -c:a aac -pix_fmt yuv420p \
	# -f flv "rtmp://192.168.86.145:1935/pushmungo/testthis2"
     ffmpeg -hide_banner -loglevel fatal -f x11grab -video_size 1920x1080 -framerate $FPS -i $DISPLAY -f pulse -i alsa_output.platform-fef00700.hdmi.hdmi-stereo.monitor -ac 2 -c:v h264 -g $GOP -b:v $CBR -preset ultrafast -c:a aac -pix_fmt yuv420p \
	-f flv "rtmp://192.168.86.145:1935/pushmungo/testthis2"
}


while true
do
	nginxstabledesktop
done

top
