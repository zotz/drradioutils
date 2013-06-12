#! /usr/bin/env python
# need to do this the python way
# fixpod.py

import datetime, time, urlparse, os, glob, sys, re, shutil
import PyRSS2Gen
import eyeD3


prepdir = "/var/data/bitt"
#stagedir = "/var/data/bitt/stage"
stagedir = "/var/www/rhtorr"
torrdir = "/var/www/rhtorr"
#torrdir = "/var/data/bitt/stage"
torrurl = "http://oldmail.tribunemedia.net/rhtorr"



os.system("mv %s/*mp3 %s/" % (stagedir, prepdir))
os.system("rm %s/*.torrent" % (torrdir))
