#!/usr/bin/python

#rdnairplay.py
# right now, this is a dirty mashup of things / examples I have found on the web and put to alternative use.
# this is moew to give you ideas and not for use.

version="v0.01"

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


print("This is version: %s" % version)

config = configparser.ConfigParser()
config.read('/etc/rd.conf')
dbuser = config['mySQL']['Loginname']
dbpw = config['mySQL']['Password']
#print("dbuser from config is: %s " % (dbuser))

# get the database login info from /etc/rd.conf - more to do here.
my_conn = create_engine("mysql+mysqldb://%s:%s@localhost/Rivendell" % (dbuser, dbpw)) 


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

def GetDateTime():
  # Get current date and time in ISO8601
  # https://en.wikipedia.org/wiki/ISO_8601 
  # https://xkcd.com/1179/
  #I don't really need this, just here to run GetCartLine. Need to remove and do properly
  return (time.strftime("%Y%m%d", time.gmtime()),
          time.strftime("%H%M%S", time.gmtime()),
          time.strftime("%Y%m%d", time.localtime()),
          time.strftime("%H%M%S", time.localtime()))

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




class Application(tk.Frame):

  def __init__(self, master):

    fontsize = 12
    textwidth = 9

    tk.Frame.__init__(self, master)
    #self.pack()
    #self.grid(row=0)
    
    # Most of this stuff here is not needed and I need to remove it, but when I try, it affects other things
    # and I have not solved that issue yet.

    #tk.Button(self, text='Exit', width = 10, bg = '#FF8080', command=root.destroy).grid(row=9, columnspan=2)
    verlabl = tk.Label(master,
             text="Rivendell new Airplay Version %s" % (version),
             bg="white") 
    #verlabl = "Version " + version
    verlabl.pack()
    
    # define columns
    columns = ('1', '2', '3', '4', '5', '6', '7')
    
    # I don't like making tree global but I can't figure out what I am doing wrong.
    global tree

    #tree = ttk.Treeview(root, columns=columns, show='headings', height=20)
    tree = ttk.Treeview(self, columns=columns, show='headings', height=40)
    #tv=ttk.Treeview(f,show='tree')

    # define headings
    # I really need to change the order of these columns throughout.
    # Also, there may be some I don't need and others I need to include.
    # Soon perhaps.
    tree.heading('1', text='Line_Id')
    tree.heading('2', text='Cart_Number')
    tree.heading('3', text='Title')
    tree.heading('4', text='Artist')
    tree.heading('5', text='Album')
    tree.heading('6', text='Count')
    tree.heading('7', text='Start_Time')



# below is an attempt to get log machine to watch in gui rather than command line
#    c_set=my_conn.execute('''SELECT * FROM `LOG_MACHINES` WHERE `CURRENT_LOG` > '' ''')
    
#    a = [] #creates a list to store the job names in
#    var = StringVar() #creates a stringvar to store the value of options
    
#    for c in c_set:
#        a.append(c[6])
    
#    var.set(a[0]) #sets the default option of options
    
#    options = OptionMenu(root, var, *a) #createa an optionmenu populated with every element of the list
#    button = Button(root, text="Ok", command=lambda:print(var.get())) #prints the current value of options
    
#    options.pack()
#    button.pack()
# here ends attempt to get log machine in interface


        
    stmt = text('''SELECT LOG_LINES.LINE_ID, LOG_LINES.CART_NUMBER, CART.TITLE, CART.ARTIST, CART.ALBUM, LOG_LINES.COUNT, LOG_LINES.START_TIME from LOG_LINES INNER JOIN CART WHERE LOG_LINES.CART_NUMBER = CART.NUMBER AND LOG_LINES.LOG_NAME LIKE :x ORDER BY LOG_LINES.LINE_ID ASC''')
    stmt = stmt.bindparams(x=mylog)
    r_set=my_conn.execute(stmt)

    # add data to the treeview
    for dt in r_set:
        #tree.insert('', tk.END, values=dt)
        
        tree.insert("", 'end',iid=dt[0], text=dt[0],
            values =(dt[0],dt[1],dt[2],dt[3],dt[4],dt[5],dt[6]))
        #tree.insert("", 'end',iid=dt[0], text=dt[0],
        #    values =(dt[0],dt[1],dt[2],dt[3],dt[4]))        


    def item_selected(event):
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record = item['values']
            # show a message
            #showinfo(title='Information', message=','.join(map(str, record)))






    tree.bind('<<TreeviewSelect>>', item_selected)

    #tree.grid(row=0, column=0, sticky='nsew')
    #tree.pack(fill='x')

    # add a scrollbar
    scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    #scrollbar.grid(row=0, column=1, sticky='ns')
    scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
    #ybar.pack(side=tk.RIGHT,fill=tk.Y)
    tree.pack(fill='x')
    self.pack()

    tk.Button(self, text='Exit', width = 10, bg = '#FF8080', command=root.destroy).pack()
    self.gettime()
  pass


  def gettime(self):
    gdt, gtm, ldt, ltm = GetDateTime()
    gdt = gdt[0:4] + '/' + gdt[4:6] + '/' + gdt[6:8]
    gtm = gtm[0:2] + ':' + gtm[2:4] + ':' + gtm[4:6] + ' Z'  
    ldt = ldt[0:4] + '/' + ldt[4:6] + '/' + ldt[6:8]
    ltm = ltm[0:2] + ':' + ltm[2:4] + ':' + ltm[4:6]  
    #self.nowGtime.set(gdt)
    #self.nowGdate.set(gtm)
    #self.LocalTime.set(ldt)
    #self.LocalDate.set(ltm)
    myloginfo = GetCartLine()
    print("============================in gettime - Here comes myloginfo: ",myloginfo)
    zfcart = str(myloginfo[0])
    zflogline = str(myloginfo[1])
    tree.selection_set(zflogline)  # Does work.
    #tree.see(zflogline)
    tree.see(int(zflogline)-10)
    #tree.selection_set(zflogline)  # Does work
    # The below line means what is seen in the interface may lag the playout by 25 seconds.
    # For now, adjust to suit yourself.
    self.after(25000, self.gettime)
    print (ltm)  # Prove it is running this and the external code, too.
  pass


values = []

root = tk.Tk()
root.wm_title('Rivendell New Airplay vlog monitor')
app = Application(master=root)

w = 1500 # width for the Tk root
h = 1000 # height for the Tk root

# get display screen width and height
ws = root.winfo_screenwidth()  # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for positioning the Tk root window

#centered
#x = (ws/2) - (w/2)
#y = (hs/2) - (h/2)

x = ws - w
y = hs - h

#set the dimensions of the screen and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))




root.mainloop()
