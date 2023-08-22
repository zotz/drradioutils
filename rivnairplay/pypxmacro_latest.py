#!/usr/bin/python3

# pypxmacro_v000a.py

version="v0.00a"

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
import pexpect

print("This is version: %s" % version)

# Going to try and work like this
######PX mach cart [offset] [PLAY|SEGUE|STOP]!

#        settrans {line} {play|segue|stop}
#           Set the transition type for a log event.

#       addcart {line} {cart-num}
#           Add a new cart event before line line using cart cart-num.

# Oops, can't addcart with transtype, 2 step process.
# how to know which line to change after adding. TEST.

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



# At first we are going to ignore the offset option???

args = len(sys.argv) - 1
#print ("The script was called with %i arguments" % (args))
if(args == 2):
    mymach = int(sys.argv[1])
    mycart = sys.argv[2]
    myoffset = 0
    mytrans = 'PLAY'
    print("a2: mymach,mycart,myofset,mytrans-> ",mymach,mycart,myoffset,mytrans)
elif(args == 3):
    mymach = int(sys.argv[1])
    mycart = sys.argv[2]
    myoffset = 0
    mytrans = sys.argv[3]
    print("a3: mymach,mycart,myofset,mytrans-> ",mymach,mycart,myoffset,mytrans)
elif(args == 4):
    mymach = int(sys.argv[1])
    mycart = sys.argv[2]
    myoffset = sys.argv[3]
    mytrans = sys.argv[4]
    haveoffset = True
    print("a4: mymach,mycart,myofset,mytrans-> ",mymach,mycart,myoffset,mytrans)
else:
    print("Too few or too many arguments.")
    exit()


print("We do not want to get this far if the commandline arguments are incorrect.")



names = [] #creates a list to store the lob names in
lmachines = []
def GetLMData(mach):
    
    my_connglm = my_db.connect()
    # for now, by swapping the comments on the 2 query lines below you can see all running log machines or
    # just the virtual log machines.
    #c_set=my_conn.execute('''SELECT * FROM `LOG_MACHINES` WHERE `CURRENT_LOG` > '' ''')
    stmtglm = text('''SELECT CURRENT_LOG, LOG_ID, LOG_LINE, MACHINE FROM LOG_MACHINES WHERE MACHINE LIKE :x LIMIT 1''')
    stmtglm = stmtglm.bindparams(x=mach)
    #c_set=my_conn.execute('''SELECT * FROM `LOG_MACHINES` WHERE `CURRENT_LOG` > '' AND `MACHINE` > 99 ''')

    #print("c_set is: ", c_set)

    #names = [] #creates a list to store the job names in
    c_setglm=my_connglm.execute(stmtglm)

    for cglm in c_setglm:
        print("cglm is now: ",cglm)
        lmachines.append(cglm[3])
        #names.append(cglm[6])
        tlog = cglm[0]
        tlogid = cglm[1]
        tlogln = cglm[2]

    #var.set(a[0]) #sets the default option of options
    #print("names is now: ", names)
    #print("I found %s running logs." % len(names))
    my_connglm.close()
    return (tlog, tlogid, tlogln)


#GetNewLogs()
myloginfo = GetLMData(mymach)
print("myloginfo is now: ", myloginfo)


def DoExpect(log,line,cart,ttype):
    print("In DoExpect with this data: ", log,line,cart,ttype)
    child = pexpect.spawn('rdclilogedit\r')
    child.expect("logedit>")
    #print(f'log list is : {output.decode("utf-8")}')
    llogcmd = 'load '+log
    print(llogcmd)
    child.sendline(llogcmd)
    child.expect("]>")
    addcartcmd = 'addcart '+str(line)+' '+str(cart)
    print("addcartcmd is now: ",addcartcmd)
    #child.sendline('addcart 7 999999')
    child.sendline(addcartcmd)
    child.expect("]>")
    output = child.before
    print("ttype is "+str(len(ttype))+" characters long.")
    if len(ttype) > 3 and len(ttype) < 6:
        print(str(len(ttype))+" should be between 3 and 6.")
        settranscmd = 'settrans '+str(line)+' '+str(ttype)
        print("settranscmd should be set to: ", settranscmd)
        child.sendline(settranscmd)
        child.expect("]>")
        output = child.before
    #print(f'log list is : {output.decode("utf-8")}')



    child.sendline('save')
    child.expect("]>")

    child.sendline('quit')
    child.expect(pexpect.EOF)
    #child.expect(":~$")


    output = child.before
    #output = child
    print(f'quit result is : {output.decode("utf-8")}')
    child.close()




#print("names is now: ",names)
print("lmachines is now: ",lmachines)
print("mymach is now: ",mymach)
if mymach in lmachines:
    print("we seem to have a valid machine: ",mymach)
    DoExpect(myloginfo[0],(int(myloginfo[1])+int(myoffset)),mycart,mytrans)
else:
    print("We seem to have an invalid machine: ", mymach," not in ",lmachines)
