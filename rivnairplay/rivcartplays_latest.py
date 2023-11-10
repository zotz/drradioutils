#!/usr/bin/python

# rivcartplays_psg_v001.py


version="v0.01_psg"

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




names = [] #creates a list to store the job names in
groups = []
global init_colors
init_colors = True
data = []
header_list = []
# Creates columns names for each column ('column0', 'column1', etc)
header_list = ['Count', 'Cart Number', 'Title', 'Artist', 'Album', 'Line ID', 'Avg Len', 'Start Time']
pheader_list = ['Plays', 'Title', 'Artist', 'Cut Name', 'Cart Number', 'Group']


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


top_banner = [
               [sg.Text('RivCartPlays', font='Any 20', background_color=DARK_HEADER_COLOR, enable_events=True, grab=False), sg.Push(background_color=DARK_HEADER_COLOR),
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
            [sg.Text('Hey, this is some text.')]
          ]


def GetCartPlays_new():
    my_conn = my_db.connect()
    #print("Getting log lines..........")
    #print("in GetLogLines, data is now: ", data)
    print("in GetCartPlays and mynumcarts is: ", mynumcarts)
    print("in GetCartPlays and mycartorder is now: ", mycartorder)
    data = []
    data.clear()
    # Robert Jeffares SQL Suggestion
    # mysql -uroot Rivendell -A -e "select PLAY_COUNTER,TITLE, CUT_NAME,CART_NUMBER from CUTS JOIN CART ON NUMBER = CART_NUMBER WHERE NUMBER > '10000' ORDER BY PLAY_COUNTER DESC LIMIT 200 INTO OUTFILE 'repetition.txt';"
    #stmt = text('''SELECT PLAY_COUNTER,TITLE, CUT_NAME,CART_NUMBER, CART.GROUP_NAME from CUTS JOIN CART ON NUMBER = CART_NUMBER WHERE NUMBER > '10000' AND GROUP_NAME LIKE :x ORDER BY :y DESC LIMIT :z ''')
    match mycartorder:
        case "CUTS.PLAY_COUNTER":
            print("GetCartPlays : PLAY_COUNTER order")
            stmt = text('''SELECT PLAY_COUNTER,TITLE, CUT_NAME,CART_NUMBER, CART.GROUP_NAME from CUTS JOIN CART ON NUMBER = CART_NUMBER WHERE GROUP_NAME LIKE :x ORDER BY "CUTS.PLAY_COUNTER" DESC LIMIT :y ''')
        case "CART.TITLE":
            print("GetCartPlays : Title order")
            stmt = text('''SELECT PLAY_COUNTER,TITLE, CUT_NAME,CART_NUMBER, CART.GROUP_NAME from CUTS JOIN CART ON NUMBER = CART_NUMBER WHERE GROUP_NAME LIKE :x ORDER BY "CART.TITLE" DESC LIMIT :y ''')
        case "CUTS.CUT_NAME":
            print("GetCartPlays : CUT_NAME order")
            stmt = text('''SELECT PLAY_COUNTER,TITLE, CUT_NAME,CART_NUMBER, CART.GROUP_NAME from CUTS JOIN CART ON NUMBER = CART_NUMBER WHERE GROUP_NAME LIKE :x ORDER BY "CUTS.CUTNAME" DESC LIMIT :y ''')

    #stmt = text('''SELECT PLAY_COUNTER,TITLE, CUT_NAME,CART_NUMBER, CART.GROUP_NAME from CUTS JOIN CART ON NUMBER = CART_NUMBER WHERE GROUP_NAME LIKE :x ORDER BY :y DESC LIMIT :z ''')
    stmt = stmt.bindparams(x=mygroup,y=mynumcarts)
    
    r_set=my_conn.execute(stmt)
    for dt in r_set:
        logrow = [dt[0],dt[1],dt[2],dt[3],dt[4]]
        #print("Logrow is now: ", logrow)
        data.append(logrow)
        pass
    print("in GetLogLines, after select, data is now: ", data)
    my_conn.close()
    match mycartorder:
        case "CUTS.PLAY_COUNTER":
            print("GetCartPlaysp2 : PLAY_COUNTER order")
            srt =  sorted(data, key=operator.itemgetter(0), reverse=True)
            data = srt
        case "CART.TITLE":
            print("GetCartPlaysp2 : Title order")
            srt =  sorted(data, key=operator.itemgetter(1), reverse=True)
            data = srt
        case "CUTS.CUT_NAME":
            print("GetCartPlaysp2 : CUT_NAME order")
            srt =  sorted(data, key=operator.itemgetter(2), reverse=True)
            data = srt
    print("data is now: ", data)
    #data = srt


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



GetCartPlays()


block_4 = [
            [ sg.Text('Choose / Enter Options'), sg.Text('', key='_OUTPUT_')],
            [sg.Text('Group'),
             sg.Combo(groups, mygroup, font=('Arial Bold', 14),  key='groupchoice', enable_events=True,  readonly=False),
             sg.Text('Cart Order'),
             sg.Text('', key='_CO_OUTPUT_'),
             sg.Combo(mycartorderopts, mycartorder, font=('Arial Bold', 14),  key='orderchoice', enable_events=True,  readonly=False),
             sg.Text('Cart Limit'),
             sg.Text('', key='_CL_OUTPUT_'),
             sg.Input(mynumcarts, enable_events=True, key='-CL_INPUT-', font=('Arial Bold', 20), expand_x=False, justification='left')
             ],
            [sg.Table(values=data, headings=pheader_list,
                      auto_size_columns=True,
                      display_row_numbers=False,
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
            
            [sg.Text('Riv Cart Plays '), sg.Text('', key='_MYLOG_')],
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

window = sg.Window('RivCartPlays', layout, size=(1400, 900), margins=(0,0), background_color=BORDER_COLOR, no_titlebar=False, resizable=True, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_LOC_EXIT, enable_close_attempted_event=True)
window.finalize()
#rcolumn.expand(True, True)
myoldloginfo=''
myloginfo=''
while True:             # Event Loop
    event, values = window.read(timeout=5000, timeout_key='timeout')
    #print("event values is ", event, values)
    
    if event != 'timeout':
        #print(ev2)
        #pass
    #else:
        #print("Reached a Timeout!")



        if (event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == 'Exit') and sg.popup_yes_no('Do you really want to exit RivCartPlays?') == 'Yes':
            break
        elif event == 'Edit Me':
            sg.execute_editor(__file__)
        elif event == 'Version':
            sg.popup_scrolled(sg.get_versions(), keep_on_top=True)
        elif event == 'File Location':
            sg.popup_scrolled('This Python file is:', __file__)
        elif event == 'groupchoice':
            #print("Select Group changed:", myoldloginfo, " to ", myloginfo)
            mygroup = values['groupchoice']
            GetCartPlays()
            window['_table_'].update(values=data)
            #window['_MYLOG_'].update(mylog)
            #window['_OUTPUT_'].update(vals1[0])
        elif event == 'orderchoice':
            print("Event is orderchoice")
            mycartorder = values['orderchoice']
            print("mycartorder is now: ", mycartorder)
            GetCartPlays()
            window['_table_'].update(values=data)

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
            window['_table_'].update(values=data)
            print("After GetCartPlays, mynumcarts is: ", mynumcarts)
my_db.dispose()
window.close()
