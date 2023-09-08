#!/usr/bin/python3
# audioreport.py
# Copyright 2013-2023, drew Roberts
# adjusted for python3 Sep 2023
#
# Written by drew Roberts <zotzbro@gmail.com>
# Licensed under GNU GPL V3 or later.

# Will walk the current or a given directory and report on various audio files
# found there. Currently deals with wav (pcm and mp2 at least) and mp3 files.
#
# There are still some issues and some needed functionality. If you can help,
# please do.


import fnmatch
import sys
import os
from os.path import join, getsize
import re
from subprocess import call
import subprocess
from datetime import datetime, timedelta

# Begin Function definitions ============================================

def getfilelen( str ):
	audiolen = "0.00"
	filedata = str
	m = re.search('ID_LENGTH=(.+?)\n', str.decode('utf-8'))
	if m:
		audiolen = m.group(1)
	else:
		#audiolen = "0.00"
		# we have a problem
		print("***** WE HAVE A LENGTH PROBLEM *****")
	#print("================== AUDIO Length ================")
	#print(audiolen)
	#print("================== AUDIO Length ================")
	return audiolen

def getfileenc( str ):
	audioenc = ""
	filedata = str
	m = re.search('ID_AUDIO_CODEC=(.+?)\n', str.decode('utf-8'))
	if m:
		audioenc = m.group(1)
		print(audioenc)
	else:
		#audioenc = ""
		# we have a problem
		print("***** WE HAVE AN ENCODING PROBLEM *****")
		print(str)
		print("================== AUDIO Encoding ================")
	#print("================== AUDIO Encoding ================"
	# print(audioenc
	#print("================== AUDIO Encoding ================"
	return audioenc


def filechkr( filen, str ):
	filename = filen
	filedata = str
	audiolen = "0.00"
	audlencode = ""
	audioenc = ""
	audenccode = ""
	audiofilename = ""
	audfncode = ""
	#m = re.search('ID_LENGTH=(.+?)\n', str)
	m = re.search('ID_LENGTH=(.+?)\n', str.decode('utf-8'))
	if m:
		audiolen = m.group(1)
		audlencode = "AudLen good"
		print("AudLen: ", audiolen)
	else:
		audiolen = "0.00"
		audlencode = "AudLen bad"
		print("Problem with Audio Lenght")
	n = re.search('ID_AUDIO_CODEC=(.+?)\n', str.decode('utf-8'))
	if n:
		audioenc = n.group(1)
		audenccode = "AudEnc good"
		print("AudEnc: ", audioenc)
	else:
		#audioenc = ""
		audenccode = "AudEnc bad"
		print("Problem with Audio Encoding")
	o = re.search('ID_FILENAME=(.+?)\n', str.decode('utf-8'))
	if o:
		audiofilename = o.group(1)
		audfncode = "AudFNCode good"
		print("AudFN: ", audiofilename)
	else:
		#audiofilename = ""
		audfncode = "AudFNCode bad"
		print("Problem with Audio File Name")
	print("====================================================")
	retup = (filename, audlencode, audiolen, audenccode, audioenc, audfncode, audiofilename)
	return retup


matches = []
totaudlen = 0
totaudfiles = 0
totaudsize = 0
totmp3size = 0
totwavsize = 0
totpcmwsize = 0
totmpgwsize = 0
totwavs = 0
totmp3s = 0
totwavlen = 0
totmp3len = 0
totpcmwlen = 0
totmpgwlen = 0
minlen = 59.00 # will break if the min len is actually larger try and solve this in a better way
maxlen = 0.00
fsonglen = 0.00

anadir = "."
anadir = sys.argv[-1]
print("passed in anadir: ", anadir)
if anadir == "audioreport.py":
	print("working on current directory......")
	anadir = "."

# Script starts from here
if len(sys.argv) < 2:
	anadir = "."

middir = "/home/rd"


reptdir = "/home/rd"
reptfile = open('%s/audioreport.txt' % (reptdir), 'a+')


patterns = ['*.wav', '*.WAV', '*.Wav', '*.mp3', '*.MP3', '*.Mp3']
for p in patterns:
	plow = p.lower()
	for root, dirnames, filenames in os.walk(anadir):
		for filename in fnmatch.filter(filenames, p):
			#matches.append(os.path.join(root, filename))
			print("Here comes the current filename: ",filename)
			print("root is currently: ",root)
			#output = subprocess.Popen(["midentify.sh", os.path.join(root,filename)], stdout=subprocess.PIPE).communicate()[0]
			output = subprocess.Popen([os.path.join(middir,"midentify.sh"), os.path.join(root,filename)], stdout=subprocess.PIPE).communicate()[0]
			preptowrite = filechkr(filename, output)
			print(preptowrite)
			towrite = root+"||"+preptowrite[0]+"||"+preptowrite[1]+"||"+preptowrite[2]+"||"+preptowrite[3]+"||"+preptowrite[4]+"||"+preptowrite[5]+"||"+preptowrite[6]+"\n"
			reptfile.write(towrite)
			if (plow == '*.wav'):
				#print("Got a wav")
				#output = subprocess.Popen(["midentify.sh", os.path.join(root,filename)], stdout=subprocess.PIPE).communicate()[0]
				#print("====================================================")
				#print(output)
				#print("====================================================")
				songlen = getfilelen(output)
				songenc = getfileenc(output)
				totwavs+= 1
				totaudfiles += 1
				fsonglen = float(songlen)
				totaudlen += fsonglen
				totwavlen += fsonglen
				if (fsonglen < minlen):
					minlen = fsonglen
				if (fsonglen > maxlen):
					maxlen = fsonglen
				totaudsize += getsize(os.path.join(root, filename))
				totwavsize += getsize(os.path.join(root, filename))
				if (songenc == "ffmp2float"):
					totmpgwlen += fsonglen
					totmpgwsize += getsize(os.path.join(root, filename))
				if (songenc == "pcm"):
					totpcmwlen += fsonglen
					totpcmwsize += getsize(os.path.join(root, filename))
			elif (plow == '*.mp3'):
				#print("Got an mp3")
				#output = subprocess.Popen(["midentify.sh", os.path.join(root,filename)], stdout=subprocess.PIPE).communicate()[0]
				#print("====================================================")
				#print(output)
				#print("====================================================")
				songlen = getfilelen(output)
				#songenc = getfileenc(output)
				totmp3s+= 1
				totaudfiles += 1
				fsonglen = float(songlen)
				totaudlen += fsonglen
				totmp3len += fsonglen
				if (fsonglen < minlen):
					minlen = fsonglen
				if (fsonglen > maxlen):
					maxlen = fsonglen
				totaudsize += getsize(os.path.join(root, filename))
				totmp3size += getsize(os.path.join(root, filename))
			else:
				print("This file should not be in the audiostore")

sec = timedelta(seconds=int(totaudlen))
d = datetime(1,1,1) + sec
wavsec = timedelta(seconds=int(totwavlen))
wavd = datetime(1,1,1) + wavsec
mp3sec = timedelta(seconds=int(totmp3len))
mp3d = datetime(1,1,1) + mp3sec
wavpcmsec = timedelta(seconds=int(totpcmwlen))
wavpcmd = datetime(1,1,1) + wavpcmsec
wavmpgsec = timedelta(seconds=int(totmpgwlen))
wavmpgd = datetime(1,1,1) + wavmpgsec
print("====================================================")
print('Total wavs: ', totwavs)
print('Total mp3s: ', totmp3s)
print('Total audio files: ', totaudfiles)
print("====================================================")
print('Total audio file length in seconds: ', totaudlen)
print("DAYS:HOURS:MIN:SEC")
print("%d:%d:%d:%d" % (d.day-1, d.hour, d.minute, d.second))
print("====================================================")
print('Total wav audio file length in seconds: ', totwavlen)
print("DAYS:HOURS:MIN:SEC")
print("%d:%d:%d:%d" % (wavd.day-1, wavd.hour, wavd.minute, wavd.second))
print("----------------------------------------------------")
print('Breakdown of wav files between pcm and mp2:')
print('Total pcm wav audio file length in seconds: ', totpcmwlen)
print('Total mp2 wav audio file length in seconds: ', totmpgwlen)
print("DAYS:HOURS:MIN:SEC")
print("%d:%d:%d:%d" % (wavpcmd.day-1, wavpcmd.hour, wavpcmd.minute, wavpcmd.second))
print("DAYS:HOURS:MIN:SEC")
print("%d:%d:%d:%d" % (wavmpgd.day-1, wavmpgd.hour, wavmpgd.minute, wavmpgd.second))
print("====================================================")
print('Total mp3 audio file length in seconds: ', totmp3len)
print("DAYS:HOURS:MIN:SEC")
print("%d:%d:%d:%d" % (mp3d.day-1, mp3d.hour, mp3d.minute, mp3d.second))
print("====================================================")
print('Total audio filesize in Bytes is: ', totaudsize)
print('Total audio filesize in Kilobytes is: ', (totaudsize / 1024))
print('Total audio filesize in Megabytes is: ', ((totaudsize / 1024)/1024))
print('Total audio filesize in Gigabytes is: ', (((totaudsize / 1024)/1024)/1024))
print('Total audio filesize in Terabytes is: ', ((((totaudsize / 1024)/1024)/1024)/1024))
print('Minimum cut length: ',  minlen)
print('Maximum cut length: ',  maxlen)
print("====================================================")
print('Total wav filesize in Bytes is: ', totwavsize)
print('Total wav filesize in Kilobytes is: ', (totwavsize / 1024))
print('Total wav filesize in Megabytes is: ', ((totwavsize / 1024)/1024))
print('Total wav filesize in Gigabytes is: ', (((totwavsize / 1024)/1024)/1024))
print('Total wav filesize in Terabytes is: ', ((((totwavsize / 1024)/1024)/1024)/1024))
print("====================================================")
print('Total mp3 filesize in Bytes is: ', totmp3size)
print('Total mp3 filesize in Kilobytes is: ', (totmp3size / 1024))
print('Total mp3 filesize in Megabytes is: ', ((totmp3size / 1024)/1024))
print('Total mp3 filesize in Gigabytes is: ', (((totmp3size / 1024)/1024)/1024))
print('Total mp3 filesize in Terabytes is: ', ((((totmp3size / 1024)/1024)/1024)/1024))
print("====================================================")
print('Total pcm wav filesize in Bytes is: ', totpcmwsize)
print('Total pcm wav filesize in Kilobytes is: ', (totpcmwsize / 1024))
print('Total pcm wav filesize in Megabytes is: ', ((totpcmwsize / 1024)/1024))
print('Total pcm wav filesize in Gigabytes is: ', (((totpcmwsize / 1024)/1024)/1024))
print('Total pcm wav filesize in Terabytes is: ', ((((totpcmwsize / 1024)/1024)/1024)/1024))
print("====================================================")
print('Total mp2 wav filesize in Bytes is: ', totmpgwsize)
print('Total mp2 wav filesize in Kilobytes is: ', (totmpgwsize / 1024))
print('Total mp2 wav filesize in Megabytes is: ', ((totmpgwsize / 1024)/1024))
print('Total mp2 wav filesize in Gigabytes is: ', (((totmpgwsize / 1024)/1024)/1024))
print('Total mp2 wav filesize in Terabytes is: ', ((((totmpgwsize / 1024)/1024)/1024)/1024))
print("====================================================")


reptfile.close()
