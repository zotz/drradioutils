#!/usr/bin/python

# rivnairplay_psg_v005.py
# from
# rivnairplay_psg_v004j.py
# jumped back over 
# rivnairplay_psg_v004k.py
# incorporates a cartplays tab

version="v0.05_psg"

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
import operator
from operator import itemgetter


#print("This is version: %s" % version)

#sg.theme('Light green 6')
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

today = datetime.datetime.now()
mydate = today.strftime('_%Y_%m_%d')
mydate1 = today.strftime('%d %B, %Y')

mynumcarts = 30000
mygroup = "MUSIC"
mycartorderopts = ['CUTS.PLAY_COUNTER', 'CART.TITLE', 'CART.ARTIST', 'CUTS.CUT_NAME']
mycartorder = "CUTS.PLAY_COUNTER"
mylastcol = 0
myreverse = True




names = [] #creates a list to store the job names in
groups = []
global init_colors
init_colors = True
data = []
header_list = []
# Creates columns names for each column ('column0', 'column1', etc)
header_list = ['Count', 'Cart Number', 'Title', 'Artist', 'Album', 'Line ID', 'Avg Len', 'Start Time']
pheader_list = ['Plays', 'Title', 'Artist', 'Cut Name', 'Cart Number', 'Group']


#choices = {'a': 1, 'b': 2}
#result = choices.get(key, 'default')

# A = Audio, C = Command (Macro), S = Split (???)
mycarttypes = {1: 'A', 2: 'C', 3: 'S'}
#result = mycarttypes.get(1, 'S')
#print("result is now: ",result)

mytranstypes = {0: 'Play', 1: 'Segue', 2: 'Stop', 255: 'NoTrans'}

args = len(sys.argv) - 1
print ("The script was called with %i arguments" % (args))
if(args > 0):
    print("The important parameter is %s." % (sys.argv[1]))
    mybase = sys.argv[1]
else:
    mybase = "AP1"

t1_mybase = mybase
t2_mybase = mybase
t3_mybase = mybase

today = datetime.datetime.now()
mydate = today.strftime('_%Y_%m_%d')
mydate1 = today.strftime('%d %B, %Y')
#print(mydate)

t1_mylog = t1_mybase+mydate
t2_mylog = t2_mybase+mydate
t3_mylog = t3_mybase+mydate
#print("The log to deal with should be: %s" % mylog)
#
t1_triggerfile = "/tmp/rivnan/current_"+t1_mybase+".txt"
t2_triggerfile = "/tmp/rivnan/current_"+t2_mybase+".txt"
t3_triggerfile = "/tmp/rivnan/current_"+t3_mybase+".txt"
#print("Trigger file is: ",triggerfile)


def GetCartLine(watchtab):

    match watchtab:
        case 't1':
             loctriggerfile = t1_triggerfile
        case 't2':
             loctriggerfile = t2_triggerfile
        case 't3':
             loctriggerfile = t3_triggerfile
        case _:
            loctriggerfile = t1_triggerfile

    with open(loctriggerfile) as f:
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
global t1_init_colors
global t2_init_colors
global t3_init_colors
t1_init_colors = True
t2_init_colors = True
t3_init_colors = True
data = []
header_list = []
# Creates columns names for each column ('column0', 'column1', etc)
header_list = ['StTime', 'TTyp', 'Cart', 'Group', 'ALen', 'Title', 'Artist', 'Album', 'Src', 'LnID', 'Count', 'LLT', 'CT', 'ALenMS']

#toprow = ['S.No.', 'Name', 'Age', 'Marks']


def sort_tuples(sub_li,sortkey,rev):
 
    # itemgetter(1) returns a function that can be used to retrieve the
    # second element of a tuple (i.e., the element at index 1)
    # this function is used as the key for sorting the sublists
    return sorted(sub_li, key=itemgetter(sortkey), reverse=rev)



def GetGroups():
    my_conn = my_db.connect()
    d_set=my_conn.execute('''SELECT NAME FROM `GROUPS` ''')
    for d in d_set:
        groups.append(d[0])
    my_conn.close()
    #print("groups: ", groups)

GetGroups()

def GetCartPlays():
    my_conn = my_db.connect()
    #print("Getting log lines..........")
    #print("in GetLogLines, data is now: ", data)
    #print("in GetCartPlays and mynumcarts is: ", mynumcarts)
    #print("in GetCartPlays and mycartorder is now: ", mycartorder)
    data.clear()
    # Robert Jeffares SQL Suggestion
    # mysql -uroot Rivendell -A -e "select PLAY_COUNTER,TITLE, CUT_NAME,CART_NUMBER from CUTS JOIN CART ON NUMBER = CART_NUMBER WHERE NUMBER > '10000' ORDER BY PLAY_COUNTER DESC LIMIT 200 INTO OUTFILE 'repetition.txt';"
    #stmt = text('''SELECT PLAY_COUNTER,TITLE, CUT_NAME,CART_NUMBER, CART.GROUP_NAME from CUTS JOIN CART ON NUMBER = CART_NUMBER WHERE NUMBER > '10000' AND GROUP_NAME LIKE :x ORDER BY :y DESC LIMIT :z ''')
    stmt = text('''SELECT PLAY_COUNTER, TITLE, ARTIST, CUT_NAME,CART_NUMBER, CART.GROUP_NAME from CUTS JOIN CART ON NUMBER = CART_NUMBER WHERE GROUP_NAME LIKE :x ORDER BY :y DESC LIMIT :z ''')
    stmt = stmt.bindparams(x=mygroup,y=mycartorder,z=mynumcarts)
    
    r_set=my_conn.execute(stmt)
    for dt in r_set:
        logrow = [dt[0],dt[1],dt[2],dt[3],dt[4],dt[5]]
        #print("Logrow is now: ", logrow)
        data.append(logrow)
        #pass
    #print("======================= in GetCartPlays, after select, data is now: ", data)
    #srt =  sorted(data, key=operator.itemgetter(0), reverse=True)
    match mycartorder:
        case "CUTS.PLAY_COUNTER":
            #print("GetCartPlaysp2 : PLAY_COUNTER order")
            srt = sort_tuples(data,0,True)
        case "CART.TITLE":
            #print("GetCartPlaysp2 : Title order")
            srt = sort_tuples(data,1,False)
        case "CART.ARTIST":
            #print("GetCartPlaysp2 : Title order")
            srt = sort_tuples(data,2,False)
        case "CUTS.CUT_NAME":
            #print("GetCartPlaysp2 : CUT_NAME order")
            srt = sort_tuples(data,3,False)


    #print("in GetCartPlays, after select, data is now: ", data)
    data.clear()
    #print("in GetCartPlays, after select, srt is now: ", srt)
    #print("in GetCartPlays, after select, cleared data is now: ", data)
    for i in srt:
        data.append(i)
    #data = [i for i in srt]
    #print("in GetCartPlays, after select, sorted data is now: ", data)
    my_conn.close()
    return(data)



GetCartPlays()

def word():

    return ''.join(random.choice(string.ascii_lowercase) for i in range(10))

def number(max_val=1000):

    return random.randint(0, max_val)



def make_table(num_rows, num_cols):

    data = [[j for j in range(num_cols)] for i in range(num_rows)]

    data[0] = [word() for __ in range(num_cols)]

    for i in range(1, num_rows):

        data[i] = [i, word(), *[number() for i in range(num_cols - 1)]]

    return data


cpheadings = ['Plays', 'Title', 'Artist', 'Cut Name', 'Cart Number', 'Group']


def sort_table(table, cols, srtrev):

    """ sort a table by multiple columns

        table: a list of lists (or tuple of tuples) where each inner list

               represents a row

        cols:  a list (or tuple) specifying the column numbers to sort by

               e.g. (1,0) would sort by column 1, then by column 0

    """

    for col in reversed(cols):

        try:
            if srtrev:
                # srt =  sorted(data, key=operator.itemgetter(2), reverse=True)
                table = sorted(table, key=operator.itemgetter(col), reverse=True)
            else:
                table = sorted(table, key=operator.itemgetter(col), reverse=False)

        except Exception as e:

            sg.popup_error('Error in sort_table', 'Exception in sort_table', e)

    return table







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


def GetLogLines(watchtab):
    my_conn = my_db.connect()
    print("***********************************************************In GetLogLines with a watchtab of: ",watchtab)
    

    #loc_data.clear()
    loc_data = []
    loc_data.clear()

    match watchtab:
        case 't1':
             locmylog = t1_mylog
             print("matched t1, locmylog should show this: ", locmylog)
        case 't2':
             locmylog = t2_mylog
             print("matched t2, locmylog should show this: ", locmylog)
        case 't3':
             locmylog = t3_mylog
             print("matched t3, locmylog should show this: ", locmylog)
        case _:
            locmylog = t1_mylog
    print("locmylog is now: ",locmylog)


    loc_mybase = locmylog[0:3]
    loc_triggerfile = "/tmp/rivnan/current_"+loc_mybase+".txt"


    stmt = text('''SELECT LOG_LINES.START_TIME, LOG_LINES.TRANS_TYPE, LOG_LINES.CART_NUMBER, CART.GROUP_NAME, CART.AVERAGE_LENGTH, CART.TITLE, CART.ARTIST, CART.ALBUM, LOG_LINES.SOURCE, LOG_LINES.COUNT, LOG_LINES.LINE_ID, LOG_LINES.TYPE, CART.TYPE from LOG_LINES INNER JOIN CART WHERE LOG_LINES.CART_NUMBER = CART.NUMBER AND LOG_LINES.LOG_NAME LIKE :x ORDER BY LOG_LINES.COUNT ASC''')
    stmt = stmt.bindparams(x=locmylog)
    #print("in GetLogLines, stmt is now: ", stmt)
    
    r_set=my_conn.execute(stmt)
    #print("in GetLogLines, r_set is now: ", r_set)
    # add data to the list for the table
    for dt in r_set:

        myavglen = FixAvgLen(dt[4])

#        logrow = [dt[0],dt[1],dt[2],dt[3],dt[4],dt[5],dt[6]]
        loc_logrow = [dt[0],dt[1],dt[2],dt[3],myavglen,dt[5],dt[6],dt[7],dt[8],dt[9],dt[10],dt[11],dt[12],dt[4]]
        #print("Logrow is now: ", logrow)
        loc_data.append(loc_logrow)
        pass
    print("in GetLogLines, after select, data is now: ", loc_data)
    my_conn.close()
    return loc_data

t1_data = GetLogLines('t1')
t2_data = GetLogLines('t2')
t3_data = GetLogLines('t3')
t4_data = GetCartPlays()
#print("t1_data is now: ", t1_data)
#print("t2_data is now: ", t2_data)
#print("t3_data is now: ", t3_data)
#print("t4_data is now: ", t4_data)


t1_block_4 = [
            [ sg.Text('Choose Log Machine / Running Log'), sg.Text('', key='_t1_OUTPUT_')],
            [sg.Combo(names, font=('Arial Bold', 14),  key='t1_logchoice', enable_events=True,  readonly=False)],
            [sg.Table(values=t1_data, headings=header_list,
                      auto_size_columns=True,
                      display_row_numbers=True,
                      justification='left', key='_t1_table_',
                      selected_row_colors='red on yellow',
                      vertical_scroll_only = False,
                      enable_events=True,
                      expand_x=True,
                      expand_y=True,
                      enable_click_events=True,
                      num_rows=min(25, len(t1_data))
                      )
             ],
            #[sg.Text('Riv New Airplay Watching Log %s' % vals1[0])],
            
            [sg.Text('Riv New Airplay Watching Log '), sg.Text('', key='_t1_MYLOG_')],
            #[sg.Text(vals1[0])],
            [sg.Text('', key='_t1_OUTPUT1_')]
        ]


t2_block_4 = [
            [ sg.Text('Choose Log Machine / Running Log'), sg.Text('', key='_t2_OUTPUT_')],
            [sg.Combo(names, font=('Arial Bold', 14),  key='t2_logchoice', enable_events=True,  readonly=False)],
            [sg.Table(values=t2_data, headings=header_list,
                      auto_size_columns=True,
                      display_row_numbers=True,
                      justification='left', key='_t2_table_',
                      selected_row_colors='red on yellow',
                      vertical_scroll_only = False,
                      enable_events=True,
                      expand_x=True,
                      expand_y=True,
                      enable_click_events=True,
                      num_rows=min(25, len(t2_data))
                      )
             ],
            #[sg.Text('Riv New Airplay Watching Log %s' % vals1[0])],
            
            [sg.Text('Riv New Airplay Watching Log '), sg.Text('', key='_t2_MYLOG_')],
            #[sg.Text(vals1[0])],
            [sg.Text('', key='_t2_OUTPUT1_')]
        ]


t3_block_4 = [
            [ sg.Text('Choose Log Machine / Running Log'), sg.Text('', key='_t3_OUTPUT_')],
            [sg.Combo(names, font=('Arial Bold', 14),  key='t3_logchoice', enable_events=True,  readonly=False)],
            [sg.Table(values=t3_data, headings=header_list,
                      auto_size_columns=True,
                      display_row_numbers=True,
                      justification='left', key='_t3_table_',
                      selected_row_colors='red on yellow',
                      vertical_scroll_only = False,
                      enable_events=True,
                      expand_x=True,
                      expand_y=True,
                      enable_click_events=True,
                      num_rows=min(25, len(t3_data))
                      )
             ],
            #[sg.Text('Riv New Airplay Watching Log %s' % vals1[0])],
            
            [sg.Text('Riv New Airplay Watching Log '), sg.Text('', key='_t3_MYLOG_')],
            #[sg.Text(vals1[0])],
            [sg.Text('', key='_t3_OUTPUT1_')]
        ]

t41_block_4 = [
            [ sg.Text('Choose Log Machine / Running Log'), sg.Text('', key='_t3_OUTPUT_')],
            [sg.Combo(names, font=('Arial Bold', 14),  key='t3_logchoice', enable_events=True,  readonly=False)],
            [sg.Table(values=t4_data, headings=header_list,
                      auto_size_columns=True,
                      display_row_numbers=True,
                      justification='left', key='_t4_table_',
                      selected_row_colors='red on yellow',
                      vertical_scroll_only = False,
                      enable_events=True,
                      expand_x=True,
                      expand_y=True,
                      enable_click_events=True,
                      num_rows=min(25, len(t4_data))
                      )
             ],
            #[sg.Text('Riv New Airplay Watching Log %s' % vals1[0])],
            
            [sg.Text('Riv New Airplay Watching Log '), sg.Text('', key='_t4_MYLOG_')],
            #[sg.Text(vals1[0])],
            [sg.Text('', key='_t4_OUTPUT1_')]
        ]



t4_block_4 = [[sg.Table(values=t4_data[1:][:], headings=cpheadings, max_col_width=25,
                    auto_size_columns=True,
                    display_row_numbers=True,
                    justification='right',
                    num_rows=min(25, len(t4_data)),
                    key='-TABLE-',
                    selected_row_colors='red on yellow',
                    enable_events=True,
                    expand_x=True,
                    expand_y=True,
                    enable_click_events=True,           # Comment out to not enable header and other clicks
                    tooltip='This is a table')],
          
          [ sg.Text('Choose / Enter Options'), sg.Text('', key='_OUTPUT_')],
            [sg.Text('Group'),
             sg.Combo(groups, mygroup, font=('Arial Bold', 14),  key='groupchoice', enable_events=True,  readonly=False),
             sg.Text('Cart Limit'),
             sg.Text('', key='_CL_OUTPUT_'),
             sg.Input(mynumcarts, enable_events=True, key='-CL_INPUT-', font=('Arial Bold', 20), expand_x=False, justification='left')
             ],

          [sg.Text('Cell clicked:'), sg.T(k='-CLICKED-')]
]


tab1_layout = t1_block_4

tab2_layout = t2_block_4

tab3_layout = t3_block_4

tab4_layout = t4_block_4

tabgrp1_layout = [[sg.TabGroup([
    [sg.Tab('Log Control 1', tab1_layout, background_color='tan1', key='-mykey-'),
     sg.Tab('Log Control 2', tab2_layout, background_color='tan1'),
     sg.Tab('Log Control 3', tab3_layout, background_color='tan1'),
     sg.Tab('Cart Plays Tab', tab4_layout, background_color='tan1')]],
                       key='-group1-', title_color='red',
                       selected_title_color='green', tab_location='bottom')]]



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
#layout_frame2 = block_4
layout_frame2 = tabgrp1_layout

layout = [
    [sg.Frame('f1', top_banner,   pad=(0,0), background_color=DARK_HEADER_COLOR, expand_x=True, border_width=0, grab=True)],
    [sg.Frame('f2', top, size=(1310, 100), expand_x=True,  relief=sg.RELIEF_GROOVE, border_width=3)],
    [sg.Frame("Frame 1", layout_frame1, size=(450, 750)),
     sg.Frame("Frame 2", layout_frame2, size=(1000, 750), title_location=sg.TITLE_LOCATION_TOP)],]





window = sg.Window('RDnAirPlay', layout, size=(1400, 900), margins=(0,0), background_color=BORDER_COLOR, no_titlebar=False, resizable=True, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_LOC_EXIT, enable_close_attempted_event=True)
window.finalize()
#rcolumn.expand(True, True)
progress_bar = window['-PBAR-']
t1_myoldloginfo=''
t1_myloginfo=''
t2_myoldloginfo=''
t2_myloginfo=''
t3_myoldloginfo=''
t3_myloginfo=''
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



        t1_myoldloginfo = t1_myloginfo
        t1_myloginfo = GetCartLine('t1')
        if t1_myoldloginfo != t1_myloginfo :
            myisrunning = True
            mycartstart = time.time()
            mycartelapse = 0            
            #print("myloginfo changed:", myoldloginfo, " to ", myloginfo)
            zfcart1 = int(t1_myloginfo[0])
            #print("zfcart1 is: ", zfcart1)
            #print(data[zfcart1])
            #window['_cf1-num_'].update(zfcart1)
            zflogline1 = int(t1_myloginfo[1])
            #print("zflogline1 is: ",zflogline1)
            # str(timedelta(seconds=elapsed))
            #print("starttime number: ", (data[zflogline1][0]/1000))
            #zfcstart1 = str(datetime.timedelta((data[zflogline1][0]/1000)))
            # tvar = (time.strftime("%H:%M:%S.{}".format(str(elapsed % 1)[2:])[:15], time.gmtime(elapsed)))
            zcst1 = (t1_data[zflogline1][0]/1000)
            zfcstart1 = (time.strftime("%H:%M:%S.{}".format(str((zcst1) % 1)[2:])[:15], time.gmtime(zcst1)))
            zftitle1 = t1_data[zflogline1][5]
            zfartist1 = t1_data[zflogline1][6]
            zfavglen1 = t1_data[zflogline1][4]
            zfmsecs1 = t1_data[zflogline1][13]
            zfcarttype1 = mycarttypes.get(t1_data[zflogline1][12], 'S')
            #print("transtype number is: ", data[zflogline1][1])
            zftranstype1 = mytranstypes.get(t1_data[zflogline1][1], 'Oops')
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
            zfcart2 = t1_data[zflogline2][2]
            zcst2 = (t1_data[zflogline2][0]/1000)
            zfcstart2 = (time.strftime("%H:%M:%S.{}".format(str((zcst2) % 1)[2:])[:15], time.gmtime(zcst2)))
            zftitle2 = t1_data[zflogline2][5]
            zfartist2 = t1_data[zflogline2][6]
            zfavglen2 = t1_data[zflogline2][4]
            zfmsecs2 = t1_data[zflogline2][13]
            zfcarttype2 = mycarttypes.get(t1_data[zflogline2][12], 'S')
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
            zfcart3 = t1_data[zflogline3][2]
            zcst3 = (t1_data[zflogline3][0]/1000)
            zfcstart3 = (time.strftime("%H:%M:%S.{}".format(str((zcst3) % 1)[2:])[:15], time.gmtime(zcst3)))
            zftitle3 = t1_data[zflogline3][5]
            zfartist3 = t1_data[zflogline3][6]
            zfavglen3 = t1_data[zflogline3][4]
            zfmsecs3 = t1_data[zflogline3][13]
            zfcarttype3 = mycarttypes.get(t1_data[zflogline3][12], 'S')
            window['_cf3-ctp_'].update(zfcarttype3)
            window['_cf3-num_'].update(zfcart3)
            window['_cf3-tit_'].update(zftitle3)
            window['_cf3-art_'].update(zfartist3)
            window['_cf3-len_'].update(zfavglen3)
            window['_cf3-sec_'].update(int(zfmsecs3/1000))
            window['_cf3-cst_'].update(zfcstart3)
            #========================================================
            zflogline4 = zflogline1+3
            zfcart4 = t1_data[zflogline4][2]
            zftitle4 = t1_data[zflogline4][5]
            zfartist4 = t1_data[zflogline4][6]
            window['_cf4-num_'].update(zfcart4)
            window['_cf4-tit_'].update(zftitle4)
            window['_cf4-art_'].update(zfartist4)
            #========================================================
            zflogline5 = zflogline1+4
            zfcart5 = t1_data[zflogline5][2]
            zftitle5 = t1_data[zflogline5][5]
            zfartist5 = t1_data[zflogline5][6]
            window['_cf5-num_'].update(zfcart5)
            window['_cf5-tit_'].update(zftitle5)
            window['_cf5-art_'].update(zfartist5)
            #========================================================
            zflogline6 = zflogline1+5
            zfcart6 = t1_data[zflogline6][2]
            zftitle6 = t1_data[zflogline6][5]
            zfartist6 = t1_data[zflogline6][6]
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
        zfcart = str(t1_myloginfo[0])
        zflogline = str(t1_myloginfo[1])
        #print("zflogline is currently: ", zflogline)
        window["_t1_OUTPUT1_"].update(zflogline)
        #win2["_table_"].Widget.see(int(zflogline))
        if int(zflogline) > 31:
            window["_t1_table_"].Widget.yview_moveto(((int(zflogline)-15)/len(t1_data)))
        else:
            window["_t1_table_"].Widget.yview_moveto((int(zflogline)/len(t1_data)))
        #win2['_table_'].update(select_rows = [int(zflogline)])
        if t1_init_colors:
            # set up colors of rows already played
            row_col_list = []
            for crow in range(int(zflogline)):
                #
                #row_colors = ((5, 'white', 'blue'), (0,'red'), (15,'yellow'))
                row_col_list.append((crow, 'DarkGray'))
            t1_init_colors = False
        cur_col_list = []
        cur_col_list.append((int(zflogline), 'white', 'green'))
        #lst_col_list = []
        row_col_list.append(((int(zflogline)-1), 'DarkGray'))
        window['_t1_table_'].update(row_colors=(cur_col_list))
        window['_t1_table_'].update(row_colors=(row_col_list))
        #print("Reached a Timeout!")

# -------------------------------------------------------------------------------------------------



        t2_myoldloginfo = t2_myloginfo
        t2_myloginfo = GetCartLine('t2')
        if t2_myoldloginfo != t2_myloginfo :
            #myisrunning = True
            #mycartstart = time.time()
            #mycartelapse = 0            
            #print("myloginfo changed:", myoldloginfo, " to ", myloginfo)
            t2_zfcart1 = int(t2_myloginfo[0])
            #print("zfcart1 is: ", zfcart1)
            #print(data[zfcart1])
            #window['_cf1-num_'].update(zfcart1)
            t2_zflogline1 = int(t2_myloginfo[1])
            #print("zflogline1 is: ",zflogline1)
            # str(timedelta(seconds=elapsed))
            #print("starttime number: ", (data[zflogline1][0]/1000))
            #zfcstart1 = str(datetime.timedelta((data[zflogline1][0]/1000)))
            # tvar = (time.strftime("%H:%M:%S.{}".format(str(elapsed % 1)[2:])[:15], time.gmtime(elapsed)))


            #========================================================
        else:
            pass
            

        #print("============================in gettime - Here comes myloginfo: ", myloginfo)
        t2_zfcart = str(t2_myloginfo[0])
        t2_zflogline = str(t2_myloginfo[1])
        #print("zflogline is currently: ", zflogline)
        window["_t2_OUTPUT1_"].update(t2_zflogline)
        #win2["_table_"].Widget.see(int(zflogline))
        if int(t2_zflogline) > 31:
            window["_t2_table_"].Widget.yview_moveto(((int(t2_zflogline)-15)/len(t2_data)))
        else:
            window["_t2_table_"].Widget.yview_moveto((int(t2_zflogline)/len(t2_data)))
        #win2['_table_'].update(select_rows = [int(zflogline)])
        if t2_init_colors:
            # set up colors of rows already played
            t2_row_col_list = []
            for t2_crow in range(int(t2_zflogline)):
                #
                #row_colors = ((5, 'white', 'blue'), (0,'red'), (15,'yellow'))
                t2_row_col_list.append((t2_crow, 'DarkGray'))
            t2_init_colors = False
        t2_cur_col_list = []
        t2_cur_col_list.append((int(t2_zflogline), 'white', 'green'))
        #lst_col_list = []
        t2_row_col_list.append(((int(t2_zflogline)-1), 'DarkGray'))
        window['_t2_table_'].update(row_colors=(t2_cur_col_list))
        window['_t2_table_'].update(row_colors=(t2_row_col_list))
        #print("Reached a Timeout!")


# .............................................................................................

        t3_myoldloginfo = t3_myloginfo
        t3_myloginfo = GetCartLine('t3')
        if t3_myoldloginfo != t3_myloginfo :
            #myisrunning = True
            #mycartstart = time.time()
            #mycartelapse = 0            
            #print("myloginfo changed:", myoldloginfo, " to ", myloginfo)
            t3_zfcart1 = int(t3_myloginfo[0])
            #print("zfcart1 is: ", zfcart1)
            #print(data[zfcart1])
            #window['_cf1-num_'].update(zfcart1)
            t3_zflogline1 = int(t3_myloginfo[1])
            #print("zflogline1 is: ",zflogline1)
            # str(timedelta(seconds=elapsed))
            #print("starttime number: ", (data[zflogline1][0]/1000))
            #zfcstart1 = str(datetime.timedelta((data[zflogline1][0]/1000)))
            # tvar = (time.strftime("%H:%M:%S.{}".format(str(elapsed % 1)[2:])[:15], time.gmtime(elapsed)))


            #========================================================
        else:
            pass
            

        #print("============================in gettime - Here comes myloginfo: ", myloginfo)
        t3_zfcart = str(t3_myloginfo[0])
        t3_zflogline = str(t3_myloginfo[1])
        #print("zflogline is currently: ", zflogline)
        window["_t3_OUTPUT1_"].update(t3_zflogline)
        #win2["_table_"].Widget.see(int(zflogline))
        if int(t3_zflogline) > 31:
            window["_t3_table_"].Widget.yview_moveto(((int(t3_zflogline)-15)/len(t3_data)))
        else:
            window["_t3_table_"].Widget.yview_moveto((int(t3_zflogline)/len(t3_data)))
        #win2['_table_'].update(select_rows = [int(zflogline)])
        if t3_init_colors:
            # set up colors of rows already played
            t3_row_col_list = []
            for t3_crow in range(int(t3_zflogline)):
                #
                #row_colors = ((5, 'white', 'blue'), (0,'red'), (15,'yellow'))
                t3_row_col_list.append((t3_crow, 'DarkGray'))
            t3_init_colors = False
        t3_cur_col_list = []
        t3_cur_col_list.append((int(t3_zflogline), 'white', 'green'))
        #lst_col_list = []
        t3_row_col_list.append(((int(t3_zflogline)-1), 'DarkGray'))
        window['_t3_table_'].update(row_colors=(t3_cur_col_list))
        window['_t3_table_'].update(row_colors=(t3_row_col_list))
        #print("Reached a Timeout!")


# ------------------------------------------------------------------------------------------------


    if (event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == 'Exit') and sg.popup_yes_no('Do you really want to exit RDnAirPlay?') == 'Yes':
        break
    elif event == 't1_logchoice':
        # NOTE: As of now, when we first begin monitoring a log, the system does not know how far along the playback of the initial cart is.
        # The progress bar/etc. will be messed up until we change to the next song.
        # Also, the time elapsed, time remaining, and progress bar are approximations / guesses. There is no communication between caed, etc. and this system
        t1_myoldloginfo=''
        t1_myloginfo=''
        #print('0 event')
        #print("values is now: ", values)
        #GetLogLines()
        t1_init_colors = True
        #print("mylog is now: ", mylog)
        t1_mylog = values['t1_logchoice']
        print("t1_mylog is now: ", t1_mylog)
        t1_mybase = t1_mylog[0:3]
        print("t1_mybase is now: ", t1_mybase)
        t1_triggerfile = "/tmp/rivnan/current_"+t1_mybase+".txt"
        
        t1_data = GetLogLines('t1')
        window['_t1_table_'].update(values=t1_data)
        window['_t1_MYLOG_'].update(t1_mylog)
        #window['_OUTPUT_'].update(vals1[0])
    elif event == 't2_logchoice':
        # NOTE: As of now, when we first begin monitoring a log, the system does not know how far along the playback of the initial cart is.
        # The progress bar/etc. will be messed up until we change to the next song.
        # Also, the time elapsed, time remaining, and progress bar are approximations / guesses. There is no communication between caed, etc. and this system
        t2_myoldloginfo=''
        t2_myloginfo=''
        #print('0 event')
        #print("values is now: ", values)
        #GetLogLines()
        t2_init_colors = True
        #print("mylog is now: ", mylog)
        t2_mylog = values['t2_logchoice']
        print("t2_mylog is now: ", t2_mylog)
        t2_mybase = t2_mylog[0:3]
        print("t2_mybase is now: ", t2_mybase)
        t2_triggerfile = "/tmp/rivnan/current_"+t2_mybase+".txt"
        t2_data = GetLogLines('t2')
        window['_t2_table_'].update(values=t2_data)
        window['_t2_MYLOG_'].update(t2_mylog)
    elif event == 't3_logchoice':
        # NOTE: As of now, when we first begin monitoring a log, the system does not know how far along the playback of the initial cart is.
        # The progress bar/etc. will be messed up until we change to the next song.
        # Also, the time elapsed, time remaining, and progress bar are approximations / guesses. There is no communication between caed, etc. and this system
        t3_myoldloginfo=''
        t3_myloginfo=''
        #print('0 event')
        #print("values is now: ", values)
        #GetLogLines()
        t3_init_colors = True
        #print("mylog is now: ", mylog)
        t3_mylog = values['t3_logchoice']
        print("t3_mylog is now: ", t3_mylog)
        t3_mybase = t3_mylog[0:3]
        print("t3_mybase is now: ", t3_mybase)
        t3_triggerfile = "/tmp/rivnan/current_"+t3_mybase+".txt"
        t3_data = GetLogLines('t3')
        window['_t3_table_'].update(values=t3_data)
        window['_t3_MYLOG_'].update(t3_mylog)

    if event == 'groupchoice':
        #print("Select Group changed:", myoldloginfo, " to ", myloginfo)
        mygroup = values['groupchoice']
        GetCartPlays()
        window['-TABLE-'].update(values=data)
    elif event == '-CL_INPUT-':
        print("Event is -CL_INPUT-")
        print(values['-CL_INPUT-'])
        if values['-CL_INPUT-'][-1] not in ('0123456789'):
            sg.popup("Only digits allowed")
            window['-CL_INPUT-'].update(values['-CL_INPUT-'][:-1])
        print("Before, mynumcarts is: ", mynumcarts)
        mynumcarts = int(values['-CL_INPUT-'])
        print("After, mynumcarts is: ", mynumcarts)
        GetCartPlays()
        window['-TABLE-'].update(values=data)
        print("After GetCartPlays, mynumcarts is: ", mynumcarts)

    if isinstance(event, tuple):

        # TABLE CLICKED Event has value in format ('-TABLE=', '+CLICKED+', (row,col))

        if event[0] == '-TABLE-':

            if event[2][0] == -1 and event[2][1] != -1:           # Header was clicked and wasn't the "row" column

                col_num_clicked = event[2][1]
                print("col_num_clicked: ", col_num_clicked," mylastcol: ", mylastcol)
                if (col_num_clicked == mylastcol):
                    if myreverse:
                        myreverse = False
                    else:
                        myreverse = True
                else:
                    mylastcol = col_num_clicked
                
                if myreverse:
                    new_table = sort_table(data[1:][:],(col_num_clicked, 0), True)
                    # srt =  sorted(data, key=operator.itemgetter(2), reverse=True)
                else:
                    new_table = sort_table(data[1:][:],(col_num_clicked, 0), False)

                window['-TABLE-'].update(new_table)

                data = [data[0]] + new_table

            window['-CLICKED-'].update(f'{event[2][0]},{event[2][1]}')




my_db.dispose()
window.close()
