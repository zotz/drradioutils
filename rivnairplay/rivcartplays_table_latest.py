1#!/usr/bin/env python

# rivcartplays_table_psg_v001.py


version="t_v0.01_psg"

import PySimpleGUI as sg

import random

import string

import operator

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


"""

    Table Element Demo With Sorting



    The data for the table is assumed to have HEADERS across the first row.

    This is often the case for CSV files or spreadsheets



    In release 4.48.0 a new enable_click_events parameter was added to the Table Element

    This enables you to click on Column Headers and individual cells as well as the standard Row selection



    This demo shows how you can use these click events to sort your table by columns



"""



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
#header_list = ['Count', 'Cart Number', 'Title', 'Artist', 'Album', 'Line ID', 'Avg Len', 'Start Time']
#pheader_list = ['Plays', 'Title', 'Artist', 'Cut Name', 'Cart Number', 'Group']


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



GetCartPlays()

# ------ Some functions to help generate data for the table ------

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



# ------ Make the Table Data ------

#data = make_table(num_rows=15, num_cols=6)

# headings = [str(data[0][x])+'     ..' for x in range(len(data[0]))]

#headings = [f'Col {col}' for col in range(len(data[0]))]
headings = ['Plays', 'Title', 'Artist', 'Cut Name', 'Cart Number', 'Group']


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



# ------ Window Layout ------

layout = [[sg.Table(values=data[1:][:], headings=headings, max_col_width=25,

                    auto_size_columns=True,

                    display_row_numbers=True,

                    justification='right',

                    num_rows=20,

                    alternating_row_color='lightyellow',

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



# ------ Create Window ------

window = sg.Window('RivCartPlays_Table', layout,

                   ttk_theme='clam',

                   resizable=True)



# ------ Event Loop ------

while True:

    event, values = window.read()

    print(event, values)

    if event == sg.WIN_CLOSED:

        break

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

window.close()


