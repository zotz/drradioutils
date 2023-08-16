#!/usr/bin/python

# rivnairplay_psg_v004i.py


version="v0.04i_psg"

import PySimpleGUI as sg
import os
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import time
import datetime
import sys
from sqlalchemy import create_engine
from sqlalchemy import text
import configparser
import random
import string


#print("This is version: %s" % version)

sg.theme('Light Blue 6')

config = configparser.ConfigParser()
config.read('/etc/rd.conf')
dbuser = config['mySQL']['Loginname']
dbpw = config['mySQL']['Password']
dbhost = config['mySQL']['Hostname']
dbdbase = config['mySQL']['Database']
#print("dbuser from config is: %s " % (dbuser))

# get the database login info from /etc/rd.conf - more to do here.
#my_conn = create_engine("mysql+mysqldb://%s:%s@localhost/Rivendell" % (dbuser, dbpw))
my_db = create_engine("mysql+mysqldb://%s:%s@%s/%s" % (dbuser, dbpw, dbhost, dbdbase))


#choices = {'a': 1, 'b': 2}
#result = choices.get(key, 'default')

# A = Audio, C = Command (Macro), S = Split (???)
mycarttypes = {1: 'A', 2: 'C', 3: 'S'}
#result = mycarttypes.get(1, 'S')
#print("result is now: ",result)

mytranstypes = {0: 'Play', 1: 'Segue', 2: 'Stop', 255: 'NoTrans'}

args = len(sys.argv) - 1
#print ("The script was called with %i arguments" % (args))
if(args > 0):
    #print("The important parameter is %s." % (sys.argv[1]))
    mybase = sys.argv[1]
else:
    mybase = "VID"

today = datetime.datetime.now()
mydate = today.strftime('_%Y_%m_%d')
mydate1 = today.strftime('%d %B, %Y')
#print(mydate)

mylog = mybase+mydate
#print("The log to deal with should be: %s" % mylog)
#
triggerfile = "/tmp/rivnan/current_"+mybase+".txt"
#print("Trigger file is: ",triggerfile)


def GetCartLine():
    # get info in file /tmp/rivnan/current_main.txt
    with open(triggerfile) as f:
        contents = f.read()
        fdata = contents.split(':')
        #print(contents)
        #print(fdata)
        fcart = fdata[1]
        flogline = fdata[2]
        return (fcart, flogline)


global myisrunning
myisrunning = False
names = [] #creates a list to store the job names in
global init_colors
init_colors = True
data = []
header_list = []
# Creates columns names for each column ('column0', 'column1', etc)
header_list = ['StTime', 'TTyp', 'Cart', 'Group', 'ALen', 'Title', 'Artist', 'Album', 'Src', 'LnID', 'Count', 'LLT', 'CT', 'ALenMS']

#toprow = ['S.No.', 'Name', 'Age', 'Marks']

def GetNewLogs():
    
    my_conn = my_db.connect()
    # for now, by swapping the comments on the 2 query lines below you can see all running log machines or
    # just the virtual log machines.
    c_set=my_conn.execute('''SELECT * FROM `LOG_MACHINES` WHERE `CURRENT_LOG` > '' ''')
    #c_set=my_conn.execute('''SELECT * FROM `LOG_MACHINES` WHERE `CURRENT_LOG` > '' AND `MACHINE` > 99 ''')

    #print("c_set is: ", c_set)

    #names = [] #creates a list to store the job names in

    for c in c_set:
        names.append(c[6])

    #var.set(a[0]) #sets the default option of options
    #print("names is now: ", names)
    #print("I found %s running logs." % len(names))
    my_conn.close()

GetNewLogs()


theme_dict = {'BACKGROUND': '#2B475D',
                'TEXT': '#FFFFFF',
                'INPUT': '#F2EFE8',
                'TEXT_INPUT': '#000000',
                'SCROLL': '#F2EFE8',
                'BUTTON': ('#000000', '#C2D4D8'),
                'PROGRESS': ('#FFFFFF', '#C7D5E0'),
                'BORDER': 0,'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0}

sg.theme_add_new('Dashboard', theme_dict)
sg.theme('Dashboard')

BORDER_COLOR = '#C7D5E0'
DARK_HEADER_COLOR = '#1B2838'
BPAD_TOP = ((20,20), (20, 10))
BPAD_LEFT = ((20,10), (0, 0))
BPAD_LEFT_INSIDE = (0, (10, 0))
BPAD_RIGHT = ((10,20), (10, 0))




def FixAvgLen(ms):
    if isinstance(ms, int):
        seconds, ms = divmod(ms, 1000)
        #seconds = (ms/1000)
        minutes, seconds = divmod(seconds, 60)
        #print(f'{int(minutes):01d}:{int(seconds):02d}')
        #myfixavg = datetime.strftime(f'{int(minutes):01d}:{int(seconds):02d}')
        # str(i).zfill(5)
        myfixavg = str(minutes).zfill(1)+":"+str(seconds).zfill(2)
        #print(myfixavg)
        return(myfixavg)
    else:
        return('0:00')
    
def FixSeconds(seconds):
    if isinstance(seconds, int):
        #seconds, ms = divmod(ms, 1000)
        #seconds = (ms/1000)
        minutes, seconds = divmod(seconds, 60)
        #print(f'{int(minutes):01d}:{int(seconds):02d}')
        #myfixavg = datetime.strftime(f'{int(minutes):01d}:{int(seconds):02d}')
        # str(i).zfill(5)
        myfixsecs = str(minutes).zfill(1)+":"+str(seconds).zfill(2)
        #print(myfixavg)
        return(myfixsecs)
    else:
        return('0:00')


def GetLogLines():
    my_conn = my_db.connect()
    #print("Getting log lines..........")
    #print("in GetLogLines, data is now: ", data)
    data.clear()
    #print("in GetLogLines, data is now: ", data)
    #print("in GetLogLines, mylog is now: ", mylog)
    #mylog = vals1[0]
    mybase = mylog[0:3]
    triggerfile = "/tmp/rivnan/current_"+mybase+".txt"


    stmt = text('''SELECT LOG_LINES.START_TIME, LOG_LINES.TRANS_TYPE, LOG_LINES.CART_NUMBER, CART.GROUP_NAME, CART.AVERAGE_LENGTH, CART.TITLE, CART.ARTIST, CART.ALBUM, LOG_LINES.SOURCE, LOG_LINES.COUNT, LOG_LINES.LINE_ID, LOG_LINES.TYPE, CART.TYPE from LOG_LINES INNER JOIN CART WHERE LOG_LINES.CART_NUMBER = CART.NUMBER AND LOG_LINES.LOG_NAME LIKE :x ORDER BY LOG_LINES.COUNT ASC''')
    stmt = stmt.bindparams(x=mylog)
    #print("in GetLogLines, stmt is now: ", stmt)
    
    r_set=my_conn.execute(stmt)
    #print("in GetLogLines, r_set is now: ", r_set)
    # add data to the list for the table
    for dt in r_set:

        myavglen = FixAvgLen(dt[4])

#        logrow = [dt[0],dt[1],dt[2],dt[3],dt[4],dt[5],dt[6]]
        logrow = [dt[0],dt[1],dt[2],dt[3],myavglen,dt[5],dt[6],dt[7],dt[8],dt[9],dt[10],dt[11],dt[12],dt[4]]
        #print("Logrow is now: ", logrow)
        data.append(logrow)
        pass
    #print("in GetLogLines, after select, data is now: ", data)
    my_conn.close()

GetLogLines()


block_4 = [
            [ sg.Text('Choose Log Machine / Running Log'), sg.Text('', key='_OUTPUT_')],
            [sg.Combo(names, font=('Arial Bold', 14),  key='logchoice', enable_events=True,  readonly=False)],
            [sg.Table(values=data, headings=header_list,
                      auto_size_columns=True,
                      display_row_numbers=True,
                      justification='left', key='_table_',
                      selected_row_colors='red on yellow',
                      vertical_scroll_only = False,
                      enable_events=True,
                      expand_x=True,
                      expand_y=True,
                      enable_click_events=True,
                      num_rows=min(25, len(data))
                      )
             ],
            #[sg.Text('Riv New Airplay Watching Log %s' % vals1[0])],
            
            [sg.Text('Riv New Airplay Watching Log '), sg.Text('', key='_MYLOG_')],
            #[sg.Text(vals1[0])],
            [sg.Text('', key='_OUTPUT1_')]
        ]





def blank_frame():
    return sg.Frame("", [[]], pad=(5, 3), expand_x=True, expand_y=True, background_color='#404040', border_width=0)


def blank_framex(x):
    return sg.Frame(x, [[]], pad=(5, 3), expand_x=True, expand_y=True, background_color='#404040', border_width=0)

def cart_frame1(c_type, cartnum, cgroup, cstart, cavglen, cttype, carttitle, cartartist, csecs, elsecs, resecs):
    this_cart_layout = [
        [sg.Text(c_type, key='_cf1-ctp_', font='Any 6', text_color='blue', background_color='white', pad=(4,0)), sg.Text(cartnum, key='_cf1-num_', font='Any 6', text_color='blue', background_color='white', pad=(4,0)), sg.Text(cgroup, key='_cf1-grp_', font='Any 6', text_color='blue', background_color='white', pad=(4,0)), sg.Text(cstart, key='_cf1-cst_', font='Any 6', text_color='blue', background_color='white', pad=(4,0)), sg.Text(cavglen, key='_cf1-len_', font='Any 6', text_color='blue', background_color='white'), sg.Text(cttype, key='_cf1-ttp_', font='Any 6', text_color='blue', background_color='white', pad=(4,0))],
        [sg.Text(carttitle, key='_cf1-tit_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        [sg.Text(cartartist, key='_cf1-art_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        #[sg.Text(elsecs, key='_cf1-ese_', font='Any 8', text_color='blue', background_color='white', pad=(4,0)), sg.Text(csecs, key='_cf1-sec_', font='Any 8', text_color='blue', background_color='white', pad=(4,0)), sg.Text(resecs, key='_cf1-rse_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        [sg.Text(elsecs, key='_cf1-ese_', font='Any 8', text_color='blue', background_color='white', pad=(4,0)), sg.ProgressBar(csecs, orientation='h', expand_x=True, size=(20, 20), bar_color=('green1', 'grey70'), key='-PBAR-'), sg.Text(resecs, key='_cf1-rse_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        
        [sg.VPush()]
        ]
    return sg.Frame("zcl1", this_cart_layout, pad=(0, 1), expand_x=True, expand_y=True, background_color='white', border_width=0)


def cart_frame2(c_type, cartnum, cgroup, cstart, cavglen, cttype, carttitle, cartartist, csecs, elsecs, resecs):
    this_cart_layout = [
        [sg.Text(c_type, key='_cf2-ctp_', font='Any 6', text_color='blue', background_color='white', pad=(4,0)), sg.Text(cartnum, key='_cf2-num_', font='Any 6', text_color='blue', background_color='white', pad=(4,0)), sg.Text(cgroup, key='_cf2-grp_', font='Any 6', text_color='blue', background_color='white', pad=(4,0)), sg.Text(cstart, key='_cf2-cst_', font='Any 6', text_color='blue', background_color='white', pad=(4,0)), sg.Text(cavglen, key='_cf2-len_', font='Any 6', text_color='blue', background_color='white')],
        [sg.Text(carttitle, key='_cf2-tit_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        [sg.Text(cartartist, key='_cf2-art_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        [sg.Text(csecs, key='_cf2-sec_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        
        [sg.VPush()]
        ]
    return sg.Frame("zcl2", this_cart_layout, pad=(0, 1), expand_x=True, expand_y=True, background_color='white', border_width=0)

def cart_frame3(c_type, cartnum, cgroup, cstart, cavglen, cttype, carttitle, cartartist, csecs, elsecs, resecs):
    this_cart_layout = [
        [sg.Text(c_type, key='_cf3-ctp_', font='Any 6', text_color='blue', background_color='white', pad=(4,0)), sg.Text(cartnum, key='_cf3-num_', font='Any 6', text_color='blue', background_color='white', pad=(4,0)), sg.Text(cgroup, key='_cf3-grp_', font='Any 6', text_color='blue', background_color='white', pad=(4,0)), sg.Text(cstart, key='_cf3-cst_', font='Any 6', text_color='blue', background_color='white', pad=(4,0)), sg.Text(cavglen, key='_cf3-len_', font='Any 6', text_color='blue', background_color='white')],
        [sg.Text(carttitle, key='_cf3-tit_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        [sg.Text(cartartist, key='_cf3-art_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        [sg.Text(csecs, key='_cf3-sec_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        
        [sg.VPush()]
        ]
    return sg.Frame("zcf3", this_cart_layout, pad=(0, 1), expand_x=True, expand_y=True, background_color='white', border_width=0)

def cart_frame4(c_type, cartnum, cgroup, cstart, cavglen, cttype, carttitle, cartartist, csecs, elsecs, resecs):
    this_cart_layout = [
        [sg.Text(c_type, key='_cf4-ctp_', font='Any 6', text_color='blue', background_color='white', pad=(4,0)), sg.Text(cartnum, key='_cf4-num_', font='Any 6', text_color='blue', background_color='white', pad=(4,0)), sg.Text(cgroup, key='_cf4-grp_', font='Any 6', text_color='blue', background_color='white', pad=(4,0)), sg.Text(cstart, key='_cf4-cst_', font='Any 6', text_color='blue', background_color='white', pad=(4,0)), sg.Text(cavglen, key='_cf4-len_', font='Any 6', text_color='blue', background_color='white')],
        [sg.Text(carttitle, key='_cf4-tit_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        [sg.Text(cartartist, key='_cf4-art_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        [sg.VPush()]
        ]
    return sg.Frame("zcf4", this_cart_layout, pad=(0, 1), expand_x=True, expand_y=True, background_color='white', border_width=0)


def cart_frame5(c_type, cartnum, cgroup, cstart, cavglen, cttype, carttitle, cartartist, csecs, elsecs, resecs):
    this_cart_layout = [
        [sg.Text(c_type, key='_cf5-ctp_', font='Any 6', text_color='blue', background_color='white', pad=(4,0)), sg.Text(cartnum, key='_cf5-num_', font='Any 6', text_color='blue', background_color='white', pad=(4,0)), sg.Text(cgroup, key='_cf5-grp_', font='Any 6', text_color='blue', background_color='white', pad=(4,0)), sg.Text(cstart, key='_cf5-cst_', font='Any 6', text_color='blue', background_color='white', pad=(4,0)), sg.Text(cavglen, key='_cf5-len_', font='Any 6', text_color='blue', background_color='white')],
        [sg.Text(carttitle, key='_cf5-tit_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        [sg.Text(cartartist, key='_cf5-art_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        [sg.VPush()]
        ]
    return sg.Frame("zcf5", this_cart_layout, pad=(0, 1), expand_x=True, expand_y=True, background_color='white', border_width=0)

def cart_frame6(c_type, cartnum, cgroup, cstart, cavglen, cttype, carttitle, cartartist, csecs, elsecs, resecs):
    this_cart_layout = [
        [sg.Text(c_type, key='_cf6-ctp_', font='Any 6', text_color='blue', background_color='white', pad=(4,0)), sg.Text(cartnum, key='_cf6-num_', font='Any 6', text_color='blue', background_color='white', pad=(4,0)), sg.Text(cgroup, key='_cf6-grp_', font='Any 6', text_color='blue', background_color='white', pad=(4,0)), sg.Text(cstart, key='_cf6-cst_', font='Any 6', text_color='blue', background_color='white', pad=(4,0)), sg.Text(cavglen, key='_cf6-len_', font='Any 6', text_color='blue', background_color='white')],
        [sg.Text(carttitle, key='_cf6-tit_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        [sg.Text(cartartist, key='_cf6-art_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        [sg.VPush()]
        ]
    return sg.Frame("zcf6", this_cart_layout, pad=(0, 1), expand_x=True, expand_y=True, background_color='white', border_width=0)


top_banner = [
               [sg.Text('RDnAirPlay', font='Any 20', background_color=DARK_HEADER_COLOR, enable_events=True, grab=False), sg.Push(background_color=DARK_HEADER_COLOR),
               sg.Text(mydate1, font='Any 20', background_color=DARK_HEADER_COLOR),
               sg.Button('Exit')]
               ]

top  = [[sg.Push(), sg.Text('Check Paradise Island Cam https://www.paradiseislandcam.com/', font='Any 20'), sg.Push()],
            [sg.T('This Frame has a relief while the others do not')],
            [sg.T('This window is resizable (see that sizegrip in the bottom right?)')]]

#sg.theme('DarkGrey4')






block_2 = [
            [cart_frame1('CTYP', 0, 'MUSIC', '14:31:12.0', "0:00", 'ttyp', "That Song1", "Bob's Yer Uncle1", 10000, 0, 10000)],
            [cart_frame2('CTYP', 0, 'MUSIC', '14:31:12.0', "0:00", 'ttyp', "That Song2", "Bob's Yer Uncle2", 10000, 0, 10000)],
            [cart_frame3('CTYP', 0, 'MUSIC', '14:31:12.0', "0:00", 'ttyp', "That Song3", "Bob's Yer Uncle3", 10000, 0, 10000)],
            [cart_frame4('CTYP', 0, 'MUSIC', '14:31:12.0', "0:00", 'ttyp', "That Song4", "Bob's Yer Uncle4", 10000, 0, 10000)],
            [cart_frame5('CTYP', 0, 'MUSIC', '14:31:12.0', "0:00", 'ttyp', "That Song5", "Bob's Yer Uncle5", 10000, 0, 10000)],
            [cart_frame6('CTYP', 0, 'MUSIC', '14:31:12.0', "0:00", 'ttyp', "That Song6", "Bob's Yer Uncle6", 10000, 0, 10000)],
            [sg.Text('Hey, this is some text.')]
          ]


layout_frame1 = [
    #[blank_framex('bf1'), blank_framex('bf2')],
    #[blank_framex('bf1')],
    [sg.Frame('f4', block_2, size=(400,550), pad=BPAD_LEFT_INSIDE, border_width=0, expand_x=True, expand_y=True, )],
    [sg.Frame("Frame 3", [[blank_framex('bf3')]], pad=(5, 3), expand_x=True, expand_y=True, title_location=sg.TITLE_LOCATION_TOP)],
]

#layout_frame2 = [[blank_framex('bfa')]]
layout_frame2 = block_4

layout = [
    [sg.Frame('f1', top_banner,   pad=(0,0), background_color=DARK_HEADER_COLOR, expand_x=True, border_width=0, grab=True)],
    [sg.Frame('f2', top, size=(1310, 100), expand_x=True,  relief=sg.RELIEF_GROOVE, border_width=3)],
    [sg.Frame("Frame 1", layout_frame1, size=(450, 750)),
     sg.Frame("Frame 2", layout_frame2, size=(1000, 750), title_location=sg.TITLE_LOCATION_TOP)],]





window = sg.Window('RDnAirPlay', layout, size=(1400, 900), margins=(0,0), background_color=BORDER_COLOR, no_titlebar=False, resizable=True, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_LOC_EXIT, enable_close_attempted_event=True)
window.finalize()
#rcolumn.expand(True, True)
progress_bar = window['-PBAR-']
myoldloginfo=''
myloginfo=''
while True:             # Event Loop
    event, values = window.read(timeout=1000, timeout_key='timeout')
    print("event | values is ", event, " | ", values)
    
    if event != 'timeout':
        #print(ev2)
        #if myisrunning:
        #    print("is running is: ",myisrunning)
        #    mycartelapse = mycartstart - datetime.datetime.now()
        #    print("mycartelapse is now: ", mycartelapse)
        pass
    else:
        # def cart_frame1(c_type, cartnum, cgroup, cstart, cavglen, cttype, carttitle, cartartist, msecs):
        #
        #print("Reached a Timeout!")
        myoldloginfo = myloginfo
        myloginfo = GetCartLine()
        if myoldloginfo != myloginfo :
            myisrunning = True
            mycartstart = time.time()
            mycartelapse = 0            
            #print("myloginfo changed:", myoldloginfo, " to ", myloginfo)
            zfcart1 = int(myloginfo[0])
            #print("zfcart1 is: ", zfcart1)
            #print(data[zfcart1])
            #window['_cf1-num_'].update(zfcart1)
            zflogline1 = int(myloginfo[1])
            #print("zflogline1 is: ",zflogline1)
            # str(timedelta(seconds=elapsed))
            #print("starttime number: ", (data[zflogline1][0]/1000))
            #zfcstart1 = str(datetime.timedelta((data[zflogline1][0]/1000)))
            # tvar = (time.strftime("%H:%M:%S.{}".format(str(elapsed % 1)[2:])[:15], time.gmtime(elapsed)))
            zcst1 = (data[zflogline1][0]/1000)
            zfcstart1 = (time.strftime("%H:%M:%S.{}".format(str((zcst1) % 1)[2:])[:15], time.gmtime(zcst1)))
            zftitle1 = data[zflogline1][5]
            zfartist1 = data[zflogline1][6]
            zfavglen1 = data[zflogline1][4]
            zfmsecs1 = data[zflogline1][13]
            zfcarttype1 = mycarttypes.get(data[zflogline1][12], 'S')
            #print("transtype number is: ", data[zflogline1][1])
            zftranstype1 = mytranstypes.get(data[zflogline1][1], 'Oops')
            window['_cf1-ctp_'].update(zfcarttype1)
            window['_cf1-ttp_'].update(zftranstype1)
            window['_cf1-num_'].update(zfcart1)
            window['_cf1-tit_'].update(zftitle1)
            window['_cf1-art_'].update(zfartist1)
            window['_cf1-len_'].update(zfavglen1)
            #window['_cf1-sec_'].update(int(zfmsecs1/1000))
            window['_cf1-rse_'].update(int(zfmsecs1/1000))
            window['_cf1-cst_'].update(zfcstart1)
            #window['-PBAR-'].update(max=int(zfmsecs1/1000))
            window['-PBAR-'].update(max=100)
            window['-PBAR-'].update(current_count=0)
            #progress_bar.UpdateBar(0, int(zfmsecs1/1000))
            progress_bar.UpdateBar(0+1, int(zfmsecs1/1000))
            
            #========================================================
            zflogline2 = zflogline1+1
            zfcart2 = data[zflogline2][2]
            zcst2 = (data[zflogline2][0]/1000)
            zfcstart2 = (time.strftime("%H:%M:%S.{}".format(str((zcst2) % 1)[2:])[:15], time.gmtime(zcst2)))
            zftitle2 = data[zflogline2][5]
            zfartist2 = data[zflogline2][6]
            zfavglen2 = data[zflogline2][4]
            zfmsecs2 = data[zflogline2][13]
            zfcarttype2 = mycarttypes.get(data[zflogline2][12], 'S')
            window['_cf2-ctp_'].update(zfcarttype2)
            #print("zfcart is: ", zfcart2)
            window['_cf2-ctp_'].update(zfcarttype2)
            window['_cf2-num_'].update(zfcart2)
            window['_cf2-tit_'].update(zftitle2)
            window['_cf2-art_'].update(zfartist2)
            window['_cf2-len_'].update(zfavglen2)
            window['_cf2-sec_'].update(int(zfmsecs2/1000))
            window['_cf2-cst_'].update(zfcstart2)
            #========================================================
            zflogline3 = zflogline1+2
            zfcart3 = data[zflogline3][2]
            zcst3 = (data[zflogline3][0]/1000)
            zfcstart3 = (time.strftime("%H:%M:%S.{}".format(str((zcst3) % 1)[2:])[:15], time.gmtime(zcst3)))
            zftitle3 = data[zflogline3][5]
            zfartist3 = data[zflogline3][6]
            zfavglen3 = data[zflogline3][4]
            zfmsecs3 = data[zflogline3][13]
            zfcarttype3 = mycarttypes.get(data[zflogline3][12], 'S')
            window['_cf3-ctp_'].update(zfcarttype3)
            window['_cf3-num_'].update(zfcart3)
            window['_cf3-tit_'].update(zftitle3)
            window['_cf3-art_'].update(zfartist3)
            window['_cf3-len_'].update(zfavglen3)
            window['_cf3-sec_'].update(int(zfmsecs3/1000))
            window['_cf3-cst_'].update(zfcstart3)
            #========================================================
            zflogline4 = zflogline1+3
            zfcart4 = data[zflogline4][2]
            zftitle4 = data[zflogline4][5]
            zfartist4 = data[zflogline4][6]
            window['_cf4-num_'].update(zfcart4)
            window['_cf4-tit_'].update(zftitle4)
            window['_cf4-art_'].update(zfartist4)
            #========================================================
            zflogline5 = zflogline1+4
            zfcart5 = data[zflogline5][2]
            zftitle5 = data[zflogline5][5]
            zfartist5 = data[zflogline5][6]
            window['_cf5-num_'].update(zfcart5)
            window['_cf5-tit_'].update(zftitle5)
            window['_cf5-art_'].update(zfartist5)
            #========================================================
            zflogline6 = zflogline1+5
            zfcart6 = data[zflogline6][2]
            zftitle6 = data[zflogline6][5]
            zfartist6 = data[zflogline6][6]
            window['_cf6-num_'].update(zfcart6)
            window['_cf6-tit_'].update(zftitle6)
            window['_cf6-art_'].update(zfartist6)
            #========================================================
        else:
            # note, when first starting to watch a log, the time remaining will most likely be incorrect.
            #print("this is what we do when we timeout but cart has not changed")
            myelapsedtime = abs(int(mycartstart - time.time()))
            #print("myelapsed time is: ",myelapsedtime)
            #print("mycartstart, myelapsedtime, zfmsecs1: ", mycartstart, myelapsedtime, zfmsecs1)
            mytimeremaining =int( ((zfmsecs1/1000) - myelapsedtime))
            #print("my time remaining is: ", mytimeremaining)
            #print("mycartstart, mytimeremaining: ",mycartstart, mytimeremaining)
            #window['_cf1-sec_'].update(mytimeremaining)
            fixmytimeremaining = FixSeconds(mytimeremaining)
            fixmyelapsedtime = FixSeconds(myelapsedtime)
            window['_cf1-rse_'].update(fixmytimeremaining)
            window['_cf1-ese_'].update(fixmyelapsedtime)
            #print("passing myelapsed time to -PBAR- : ", myelapsedtime)
            #window['-PBAR-'].update(current_count=int(0+myelapsedtime))
            #progress_bar.update_bar(int(myelapsedtime)+1, 100)
            progress_bar.UpdateBar(myelapsedtime+1, int(zfmsecs1/1000))
            #progress_bar.update_bar(myelapsedtime+1)
            # def FixSeconds(seconds):
            

        #print("============================in gettime - Here comes myloginfo: ", myloginfo)
        zfcart = str(myloginfo[0])
        zflogline = str(myloginfo[1])
        #print("zflogline is currently: ", zflogline)
        window["_OUTPUT1_"].update(zflogline)
        #win2["_table_"].Widget.see(int(zflogline))
        if int(zflogline) > 31:
            window["_table_"].Widget.yview_moveto(((int(zflogline)-15)/len(data)))
        else:
            window["_table_"].Widget.yview_moveto((int(zflogline)/len(data)))
        #win2['_table_'].update(select_rows = [int(zflogline)])
        if init_colors:
            # set up colors of rows already played
            row_col_list = []
            for crow in range(int(zflogline)):
                #
                #row_colors = ((5, 'white', 'blue'), (0,'red'), (15,'yellow'))
                row_col_list.append((crow, 'DarkGray'))
            init_colors = False
        cur_col_list = []
        cur_col_list.append((int(zflogline), 'white', 'green'))
        #lst_col_list = []
        row_col_list.append(((int(zflogline)-1), 'DarkGray'))
        window['_table_'].update(row_colors=(cur_col_list))
        window['_table_'].update(row_colors=(row_col_list))
        #print("Reached a Timeout!")

    if (event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == 'Exit') and sg.popup_yes_no('Do you really want to exit RDnAirPlay?') == 'Yes':
        break
    elif event == 'Edit Me':
        sg.execute_editor(__file__)
    elif event == 'Version':
        sg.popup_scrolled(sg.get_versions(), keep_on_top=True)
    elif event == 'File Location':
        sg.popup_scrolled('This Python file is:', __file__)
    elif event == 'logchoice':
        # NOTE: As of now, when we first begin monitoring a log, the system does not know how far along the playback of the initial cart is.
        # The progress bar/etc. will be messed up until we change to the next song.
        # Also, the time elapsed, time remaining, and progress bar are approximations / guesses. There is no communication between caed, etc. and this system
        myoldloginfo=''
        myloginfo=''
        #print('0 event')
        #print("values is now: ", values)
        #GetLogLines()
        init_colors = True
        #print("mylog is now: ", mylog)
        mylog = values['logchoice']
        #print("mylog is now: ", mylog)
        mybase = mylog[0:3]
        #print("mybase is now: ", mybase)
        triggerfile = "/tmp/rivnan/current_"+mybase+".txt"
        GetLogLines()
        window['_table_'].update(values=data)
        window['_MYLOG_'].update(mylog)
        #window['_OUTPUT_'].update(vals1[0])
my_db.dispose()
window.close()
