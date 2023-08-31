#!/usr/bin/liquidsoap
# stap3proc.liq

# Functions / Modules --------------------->

# Compressor Module / Limiter Module
compressor = ladspa.sc4(rms_peak = 0.5)
limiter = ladspa.tap_limiter(limit_level = -0.5)

# Single Band Compressor
def multiband_band(process, from, too, attack, release, ratio, threshold, gain)
	from_filter = filter.iir.eq.high(frequency = from,)
	to_filter = filter.iir.eq.low(frequency = too,)
	process_filtered = to_filter(from_filter(process))
	process_compressed = limiter(compressor(attack_time = attack, release_time = release, threshold_level = threshold, ratio=ratio, makeup_gain = gain, process_filtered))
	process_compressed
end

    # Logging

    set("log.file.path", "/home/rd/log/liquidsoap.log")

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


url = "http://localhost:8000/stap3"
radio = mksafe(input.http(url))

input1 = radio

# Audio Input --------------------->

process = input1

# Processing Blocks --------------------->

# Gate
process = ladspa.gate(process, threshold = -60.0, attack = 0.15, hold = 1.0, decay = 200.0, range = -25.0)

# Wideband AGC + Pre-Processing
process = normalize(target = 0., window = 0.03, gain_min = -16., gain_max = 0., process)
process = ladspa.sc4(rms_peak=0.3, attack_time = 0.5, release_time = 3., threshold_level = -36.0, ratio=1., makeup_gain = 6., process)

# Stereo Expander
process = ladspa.matrixspatialiser(width=16, process)

# Bass EQ
process = ladspa.tap_equalizer(band_1_freq=70., band_1_gain=4., process)
process = ladspa.tap_equalizer(band_1_freq=150., band_1_gain=-2., process)

# 5 Bands Compress/Limit
process = add(normalize=false,
  [
  multiband_band(process, 0., 200., 3.5, 30., 3., -10., 2.),
  multiband_band(process, 200., 1000., 2.25, 40., 2., -13., 2.),
  multiband_band(process, 1000., 3500., 2.25, 40., 3., -9., 2.),
  multiband_band(process, 3500., 6500., 2.25, 60., 2., -6., 1.5),
  multiband_band(process, 6500., 20000., 2.25, 70., 2., -4., 1.)
  ])

# 2 Bands Compress/Limit
process = add(normalize=false,
  [
  multiband_band(process, 0., 200., 10., 30., 2., -4., 0.),
  multiband_band(process, 200., 20000., 10., 40., 2., -2., -2.)
  ])

# De-esser
process = ladspa.tap_deesser(threshold_level=-5., frequency=6000., process)

# Final Limiter
process = limiter(process)

# Audio Output --------------------->

output1 = process



output.icecast(%mp3(bitrate=128), mount="/stap3proc", host="localhost", port=8000, password="hackme", output1)
