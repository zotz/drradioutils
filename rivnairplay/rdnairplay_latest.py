#!/usr/bin/python

# rivnairplay_psg_v004e.py


version="v0.04e_psg"

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


names = [] #creates a list to store the job names in
global init_colors
init_colors = True
data = []
header_list = []
# Creates columns names for each column ('column0', 'column1', etc)
header_list = ['Count', 'Cart Number', 'Title', 'Artist', 'Album', 'Line ID', 'Avg Len', 'Start Time']

#toprow = ['S.No.', 'Name', 'Age', 'Marks']

def GetNewLogs():
    
    my_conn = my_db.connect()
    c_set=my_conn.execute('''SELECT * FROM `LOG_MACHINES` WHERE `CURRENT_LOG` > '' ''')

    #print("c_set is: ", c_set)

    #names = [] #creates a list to store the job names in

    for c in c_set:
        names.append(c[6])

    #var.set(a[0]) #sets the default option of options
    #print("names is now: ", names)
    #print("I found %s running logs." % len(names))
    my_conn.close()

GetNewLogs()
"""
    Demo - Resizable Dashboard using Frames

    This Demo Program looks similar to the one based on the Column Element.
    This version has a big difference in how it was implemented and the fact that it can be resized.

    It's a good example of how PySimpleGUI evolves, continuously.  When the original Column-based demo
        was written, none of these techniques such as expansion, were easily programmed.

    Dashboard using blocks of information.

    Copyright 2021 PySimpleGUI.org
"""


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

def blank_frame():
    return sg.Frame("", [[]], pad=(5, 3), expand_x=True, expand_y=True, background_color='#404040', border_width=0)


#font='Any 20', background_color=DARK_HEADER_COLOR
def cart_frame1(cartnum, carttitle, cartartist):
    this_cart_layout = [
        [sg.Text(cartnum, key='_cf1-num_', font='Any 6', text_color='blue', background_color='white', pad=(4,0))],
        [sg.Text(carttitle, key='_cf1-tit_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        [sg.Text(cartartist, key='_cf1-art_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        [sg.VPush()]
        ]
    return sg.Frame("zcl1", this_cart_layout, pad=(0, 1), expand_x=True, expand_y=True, background_color='white', border_width=0)


def cart_frame2(cartnum, carttitle, cartartist):
    this_cart_layout = [
        [sg.Text(cartnum, key='_cf2-num_', font='Any 6', text_color='blue', background_color='white', pad=(4,0))],
        [sg.Text(carttitle, key='_cf2-tit_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        [sg.Text(cartartist, key='_cf2-art_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        [sg.VPush()]
        ]
    return sg.Frame("zcl2", this_cart_layout, pad=(0, 1), expand_x=True, expand_y=True, background_color='white', border_width=0)

def cart_frame3(cartnum, carttitle, cartartist):
    this_cart_layout = [
        [sg.Text(cartnum, key='_cf3-num_', font='Any 6', text_color='blue', background_color='white', pad=(4,0))],
        [sg.Text(carttitle, key='_cf3-tit_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        [sg.Text(cartartist, key='_cf3-art_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        [sg.VPush()]
        ]
    return sg.Frame("zcl3", this_cart_layout, pad=(0, 1), expand_x=True, expand_y=True, background_color='white', border_width=0)

def cart_frame4(cartnum, carttitle, cartartist):
    this_cart_layout = [
        [sg.Text(cartnum, key='_cf4-num_', font='Any 6', text_color='blue', background_color='white', pad=(4,0))],
        [sg.Text(carttitle, key='_cf4-tit_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        [sg.Text(cartartist, key='_cf4-art_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        [sg.VPush()]
        ]
    return sg.Frame("zcl4", this_cart_layout, pad=(0, 1), expand_x=True, expand_y=True, background_color='white', border_width=0)


def cart_frame5(cartnum, carttitle, cartartist):
    this_cart_layout = [
        [sg.Text(cartnum, key='_cf5-num_', font='Any 6', text_color='blue', background_color='white', pad=(4,0))],
        [sg.Text(carttitle, key='_cf5-tit_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        [sg.Text(cartartist, key='_cf5-art_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        [sg.VPush()]
        ]
    return sg.Frame("zcl5", this_cart_layout, pad=(0, 1), expand_x=True, expand_y=True, background_color='white', border_width=0)

def cart_frame6(cartnum, carttitle, cartartist):
    this_cart_layout = [
        [sg.Text(cartnum, key='_cf6-num_', font='Any 6', text_color='blue', background_color='white', pad=(4,0))],
        [sg.Text(carttitle, key='_cf6-tit_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        [sg.Text(cartartist, key='_cf6-art_', font='Any 8', text_color='blue', background_color='white', pad=(4,0))],
        [sg.VPush()]
        ]
    return sg.Frame("zcl6", this_cart_layout, pad=(0, 1), expand_x=True, expand_y=True, background_color='white', border_width=0)




top_banner = [
               [sg.Text('RDnAirPlay', font='Any 20', background_color=DARK_HEADER_COLOR, enable_events=True, grab=False), sg.Push(background_color=DARK_HEADER_COLOR),
               sg.Text(mydate1, font='Any 20', background_color=DARK_HEADER_COLOR),
               sg.Button('Exit')]
               ]

top  = [[sg.Push(), sg.Text('Got to put some stuff up here.', font='Any 20'), sg.Push()],
            [sg.T('This Frame has a relief while the others do not')],
            [sg.T('This window is resizable (see that sizegrip in the bottom right?)')]]

block_3 = [[sg.Text('Block 3', font='Any 20')],
            [sg.Input(), sg.Text('Some Text')],
            [sg.T('This frame has element_justification="c"')]
            ]


block_2 = [
            [cart_frame1(0, "That Song1", "Bob's Yer Uncle1")],
            [cart_frame2(0, "That Song2", "Bob's Yer Uncle2")],
            [cart_frame3(0, "That Song3", "Bob's Yer Uncle3")],
            [cart_frame4(0, "That Song4", "Bob's Yer Uncle4")],
            [cart_frame5(0, "That Song5", "Bob's Yer Uncle5")],
            [cart_frame6(0, "That Song6", "Bob's Yer Uncle6")],
            [sg.Text('Hey, this is some text.')]
          ]




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


    stmt = text('''SELECT LOG_LINES.COUNT, LOG_LINES.CART_NUMBER, CART.TITLE, CART.ARTIST, CART.ALBUM, LOG_LINES.LINE_ID, CART.AVERAGE_LENGTH, LOG_LINES.START_TIME from LOG_LINES INNER JOIN CART WHERE LOG_LINES.CART_NUMBER = CART.NUMBER AND LOG_LINES.LOG_NAME LIKE :x ORDER BY LOG_LINES.COUNT ASC''')
    stmt = stmt.bindparams(x=mylog)
    #print("in GetLogLines, stmt is now: ", stmt)
    
    r_set=my_conn.execute(stmt)
    #print("in GetLogLines, r_set is now: ", r_set)
    # add data to the list for the table
    for dt in r_set:

        myavglen = FixAvgLen(dt[6])

#        logrow = [dt[0],dt[1],dt[2],dt[3],dt[4],dt[5],dt[6]]
        logrow = [dt[0],dt[1],dt[2],dt[3],dt[4],dt[5],myavglen,dt[7]]
        #print("Logrow is now: ", logrow)
        data.append(logrow)
        pass
    #print("in GetLogLines, after select, data is now: ", data)
    my_conn.close()

GetLogLines()


block_4 = [
            [ sg.Text('Choose Log Machine / Running Log'), sg.Text('', key='_OUTPUT_')],
            [sg.Combo(names, font=('Arial Bold', 14),  enable_events=True,  readonly=False), sg.Button('Watch Log')],
            [sg.Table(values=data, headings=header_list,
                      auto_size_columns=True,
                      display_row_numbers=True,
                      justification='left', key='_table_',
                      selected_row_colors='red on yellow',
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



#rcolumn = sg.Column(block_4, size=(1100, 520), pad=BPAD_RIGHT,  expand_x=True, expand_y=True, grab=True)
rcolumn = sg.Column(block_4, pad=BPAD_RIGHT,  expand_x=True, expand_y=True, grab=True)

layout = [
          #[sg.Frame('f01', )],
          [sg.Frame('f1', top_banner,   pad=(0,0), background_color=DARK_HEADER_COLOR, expand_x=True, border_width=0, grab=True)],
          [sg.Frame('f2', top, size=(1310, 100), pad=BPAD_TOP,  expand_x=True,  relief=sg.RELIEF_GROOVE, border_width=3)],
          [sg.Frame('f3', [[sg.Frame('f4', block_2, size=(400,550), pad=BPAD_LEFT_INSIDE, border_width=0, expand_x=True, expand_y=True, )],
                        [sg.Frame('f5', block_3, size=(400,150),  pad=BPAD_LEFT_INSIDE, border_width=0, expand_x=True, expand_y=True, element_justification='c')]],
                    pad=BPAD_LEFT, background_color=BORDER_COLOR, border_width=0, expand_x=True, expand_y=True),
          rcolumn
          #[sg.Frame('f11', [[sg.Frame('f12', block_4, size=(1100,5200), pad=BPAD_RIGHT, border_width=0, expand_x=True, expand_y=True, )],
          #              ],
          #          pad=BPAD_RIGHT, background_color=BORDER_COLOR, border_width=5, expand_x=True, expand_y=True),
          # ]
          ]
        ]

window = sg.Window('RDnAirPlay', layout, size=(1400, 900), margins=(0,0), background_color=BORDER_COLOR, no_titlebar=False, resizable=True, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_LOC_EXIT, enable_close_attempted_event=True)
window.finalize()
#rcolumn.expand(True, True)
myoldloginfo=''
myloginfo=''
while True:             # Event Loop
    event, values = window.read(timeout=5000, timeout_key='timeout')
    #print("event values is ", event, values)
    
    if event != 'timeout':
        #print(ev2)
        pass
    else:
        #print("Reached a Timeout!")
        myoldloginfo = myloginfo
        myloginfo = GetCartLine()
        if myoldloginfo != myloginfo :
            print("myloginfo changed:", myoldloginfo, " to ", myloginfo)
            zfcart1 = int(myloginfo[0])
            print("zfcart1 is: ", zfcart1)
            #print(data[zfcart1])
            #window['_cf1-num_'].update(zfcart1)
            zflogline1 = int(myloginfo[1])
            print("zflogline1 is: ",zflogline1)
            zftitle1 = data[zflogline1][2]
            zfartist1 = data[zflogline1][3]
            window['_cf1-num_'].update(zfcart1)
            window['_cf1-tit_'].update(zftitle1)
            window['_cf1-art_'].update(zfartist1)
            zflogline2 = zflogline1+1
            zfcart2 = data[zflogline2][1]
            zftitle2 = data[zflogline2][2]
            zfartist2 = data[zflogline2][3]
            #zfcart2 = int(zfcart1)+1
            print("zfcart is: ", zfcart2)
            window['_cf2-num_'].update(zfcart2)
            window['_cf2-tit_'].update(zftitle2)
            window['_cf2-art_'].update(zfartist2)

            zflogline3 = zflogline1+2
            zfcart3 = data[zflogline3][1]
            zftitle3 = data[zflogline3][2]
            zfartist3 = data[zflogline3][3]
            window['_cf3-num_'].update(zfcart3)
            window['_cf3-tit_'].update(zftitle3)
            window['_cf3-art_'].update(zfartist3)

            zflogline4 = zflogline1+3
            zfcart4 = data[zflogline4][1]
            zftitle4 = data[zflogline4][2]
            zfartist4 = data[zflogline4][3]
            window['_cf4-num_'].update(zfcart4)
            window['_cf4-tit_'].update(zftitle4)
            window['_cf4-art_'].update(zfartist4)

            zflogline5 = zflogline1+4
            zfcart5 = data[zflogline5][1]
            zftitle5 = data[zflogline5][2]
            zfartist5 = data[zflogline5][3]
            window['_cf5-num_'].update(zfcart5)
            window['_cf5-tit_'].update(zftitle5)
            window['_cf5-art_'].update(zfartist5)

            zflogline6 = zflogline1+5
            zfcart6 = data[zflogline6][1]
            zftitle6 = data[zflogline6][2]
            zfartist6 = data[zflogline6][3]
            window['_cf6-num_'].update(zfcart6)
            window['_cf6-tit_'].update(zftitle6)
            window['_cf6-art_'].update(zfartist6)

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
    elif event == 'Watch Log':
        myoldloginfo=''
        myloginfo=''
        #print('0 event')
        #print("values is now: ", values)
        #GetLogLines()
        init_colors = True#print("mylog is now: ", mylog)
        mylog = values[1]
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
