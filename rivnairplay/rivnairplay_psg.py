#!/usr/bin/python

# rivnairplay_psg.py

# right now, this is a dirty mashup of things / examples I have found on the web and put to alternative use.
# this is more to give you ideas and not for use.



version="v0.03_psg"

import PySimpleGUI as sg
#import pandas as pd
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


print("This is version: %s" % version)

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
my_conn = create_engine("mysql+mysqldb://%s:%s@%s/%s" % (dbuser, dbpw, dbhost, dbdbase))


today = datetime.datetime.now()
mydate = today.strftime('_%Y_%m_%d')
#print(mydate)

args = len(sys.argv) - 1
#print ("The script was called with %i arguments" % (args))
if(args > 0):
    #print("The important parameter is %s." % (sys.argv[1]))
    mybase = sys.argv[1]
else:
    mybase = "VID"

mylog = mybase+mydate
print("The log to deal with should be: %s" % mylog)
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


c_set=my_conn.execute('''SELECT * FROM `LOG_MACHINES` WHERE `CURRENT_LOG` > '' ''')

print("c_set is: ", c_set)

names = [] #creates a list to store the job names in
#var = StringVar() #creates a stringvar to store the value of options

for c in c_set:
    names.append(c[6])

#var.set(a[0]) #sets the default option of options
print("names is now: ", names)
print("I found %s running logs." % len(names))


#lst = sg.Combo(names, font=('Arial Bold', 14),  expand_x=True, enable_events=True,  readonly=False, key='-COMBO-')
# Design pattern 1 - First window does not remain active

layout = [[ sg.Text('Choose Log Machine / Running Log'),],
          [sg.Text('', key='_OUTPUT_')],
          [sg.Combo(names, font=('Arial Bold', 14),  expand_x=True, enable_events=True,  readonly=False)],
          [sg.Button('Watch Log')],
          [sg.Button('Exit')]]

win1 = sg.Window('Choose Log Machine / Running Log', layout)
win2_active=False
while True:
    ev1, vals1 = win1.Read(timeout=100)
    #print("vals1 is now: ", vals1)
    #if ev2 == sg.WIN_CLOSED or ev2 == 'Exit':
    if ev1 == sg.WIN_CLOSED or ev1 == 'Exit':
        win1.Close()
        break
    win1['_OUTPUT_'].update(vals1[0])
    #win1['_OUTPUT1_'].update(vals1[1])

    if ev1 == 'Watch Log'  and not win2_active:
        mylog = vals1[0]
        mybase = mylog[0:3]
        triggerfile = "/tmp/rivnan/current_"+mybase+".txt"
        win2_active = True
        win1.Hide()
        #
        #values1 = []
        init_colors = True
        data = []
        header_list = []

        stmt = text('''SELECT LOG_LINES.LINE_ID, LOG_LINES.CART_NUMBER, CART.TITLE, CART.ARTIST, CART.ALBUM, LOG_LINES.COUNT, LOG_LINES.START_TIME from LOG_LINES INNER JOIN CART WHERE LOG_LINES.CART_NUMBER = CART.NUMBER AND LOG_LINES.LOG_NAME LIKE :x ORDER BY LOG_LINES.LINE_ID ASC''')
        stmt = stmt.bindparams(x=mylog)
        r_set=my_conn.execute(stmt)

        # add data to the list for the table
        for dt in r_set:

            logrow = [dt[0],dt[1],dt[2],dt[3],dt[4],dt[5],dt[6]]
            #print("Logrow is now: ", logrow)
            data.append(logrow)
            pass



        # Creates columns names for each column ('column0', 'column1', etc)
        header_list = ['Line ID', 'Cart Number', 'Title', 'Artist', 'Album', 'Count', 'Start Time']
                


        layout2 = [
            [sg.Table(values=data,
                      headings=header_list,
                      display_row_numbers=True,
                      auto_size_columns=True,
                      enable_click_events=True,           # Comment out to not enable header and other clicks
                      expand_x=True,
                      expand_y=True,
                      vertical_scroll_only=False,
                      key='table2',
                      num_rows=min(25, len(data)))],
            [sg.Text('Riv New Airplay Watching Log %s' % vals1[0])],
            [sg.Text(vals1[0])],
            [sg.Text('', key='_OUTPUT1_')],
            [sg.Button('Exit')]
        ]

        #window = sg.Window('Table', layout, grab_anywhere=False, resizable=True)


        myloginfo = GetCartLine()
        #print("============================in gettime - Here comes myloginfo: ",myloginfo)
        zfcart = str(myloginfo[0])
        zflogline = str(myloginfo[1])
        #print("zflogline is currently: ",zflogline)
        #window['-TABLE-'].update(row_colors=((zflogline, 'white', 'red'), (9, 'green')))
        #window['-TABLE-'].Update(select_rows = [zflogline])

        
        
        #
        #layout2 = [[sg.Text('Riv New Airplay Watching Log %s' % vals1[0])],       # note must create a layout from scratch every time. No reuse
        #    [sg.Text(vals1[0])],      
        #    [sg.Button('Exit')]]
        
        if init_colors:
            # set up colors of rows already played
            row_col_list = []
            for crow in range(int(zflogline)):
                #
                #row_colors = ((5, 'white', 'blue'), (0,'red'), (15,'yellow'))
                row_col_list.append((crow, 'DarkGray'))

        win2 = sg.Window('Riv New Airplay Watching Log %s' % vals1[0], layout2, resizable=True)
        while True:
            ev2, vals2 = win2.Read(timeout=5000, timeout_key='timeout')
            if ev2 != 'timeout':
                #print(ev2)
                pass
            else:
                #print("Reached a Timeout!")
                myloginfo = GetCartLine()
                #print("============================in gettime - Here comes myloginfo: ", myloginfo)
                zfcart = str(myloginfo[0])
                zflogline = str(myloginfo[1])
                #print("zflogline is currently: ", zflogline)
                win2["_OUTPUT1_"].update(zflogline)
                #win2["table2"].Widget.see(int(zflogline))
                if int(zflogline) > 31:
                    win2["table2"].Widget.yview_moveto(((int(zflogline)-15)/len(data)))
                else:
                    win2["table2"].Widget.yview_moveto((int(zflogline)/len(data)))
                #win2['table2'].update(select_rows = [int(zflogline)])
                cur_col_list = []
                cur_col_list.append((int(zflogline), 'green'))
                #lst_col_list = []
                row_col_list.append(((int(zflogline)-1), 'DarkGray'))
                win2['table2'].update(row_colors=(cur_col_list))
                win2['table2'].update(row_colors=(row_col_list))
                #print("Reached a Timeout!")

            if ev2 == sg.WIN_CLOSED or ev2 == 'Exit':
                win2.Close()
                win2_active = False
                win1.UnHide()
                break

