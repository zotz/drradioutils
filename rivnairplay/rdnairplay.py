#!/usr/bin/python

#rdnairplay.py
# right now, this is a dirty mashup of things / examples I have found on the web and put to alternative use.
# this is moew to give you ideas and not for use.


import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import time
from sqlalchemy import create_engine
my_conn = create_engine("mysql+mysqldb://rduser:rdusermysqlpasswd@localhost/Rivendell")  




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
    with open('/tmp/rivnan/current_v101.txt') as f:
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
    
    # Most of this stuff here is not needed and I need to remove it, but when I try, it affects other things
    # and I have not solved that issue yet.

    tk.Label(self, font=('Helvetica', fontsize), bg = '#be004e', fg = 'white', width = textwidth,
             text='Local Time').grid(row=0, column=0)
    self.LocalDate = tk.StringVar()
    self.LocalDate.set('waiting...')
    tk.Label(self, font=('Helvetica', fontsize), bg = '#be004e', fg = 'white', width = textwidth,
             textvariable=self.LocalDate).grid(row=0, column=1)

    tk.Label(self, font=('Helvetica', fontsize), bg = '#be004e', fg = 'white', width = textwidth,
             text='Local Date').grid(row=1, column=0)
    self.LocalTime = tk.StringVar()
    self.LocalTime.set('waiting...')
    tk.Label(self, font=('Helvetica', fontsize), bg = '#be004e', fg = 'white', width = textwidth,
             textvariable=self.LocalTime).grid(row=1, column=1)

    tk.Label(self, font=('Helvetica', fontsize), bg = '#40CCC0', fg = 'white', width = textwidth,
             text='GMT Time').grid(row=2, column=0)
    self.nowGdate = tk.StringVar()
    self.nowGdate.set('waiting...')
    tk.Label(self, font=('Helvetica', fontsize), bg = '#40CCC0', fg = 'white', width = textwidth,
             textvariable=self.nowGdate).grid(row=2, column=1)

    tk.Label(self, font=('Helvetica', fontsize), bg = '#40CCC0', fg = 'white', width = textwidth,
             text='GMT Date').grid(row=3, column=0)
    self.nowGtime = tk.StringVar()
    self.nowGtime.set('waiting...')
    tk.Label(self, font=('Helvetica', fontsize), bg = '#40CCC0', fg = 'white', width = textwidth,
             textvariable=self.nowGtime).grid(row=3, column=1)

    tk.Button(self, text='Exit', width = 10, bg = '#FF8080', command=root.destroy).grid(row=4, columnspan=2)
    
    
    # define columns
    columns = ('1', '2', '3', '4', '5', '6', '7')
    
    # I don't like making tree global but I can't figure out what I am doing wrong.
    global tree

    tree = ttk.Treeview(root, columns=columns, show='headings', height=40)

    # define headings
    # I really need to change the order of these columns throughout.
    # Also, there may be some I don't need and others I need to include.
    # Soon perhaps.
    tree.heading('1', text='Line_Id')
    tree.heading('2', text='Count')
    tree.heading('3', text='Start_Time')
    tree.heading('4', text='Cart_Number')
    tree.heading('5', text='Id')
    tree.heading('6', text='Title')
    tree.heading('7', text='Artist')


    # generate sample data
    #r_set = []
    #for n in range(1, 100):
    #    r_set.append((f'first {n}', f'last {n}', f'email{n}@example.com'))
        
    #r_set=my_conn.execute('''SELECT LINE_ID, COUNT, Start_Time, CART_NUMBER, ID from LOG_LINES WHERE LOG_NAME LIKE "AP1_2023_08_08"''')
    r_set=my_conn.execute('''SELECT LOG_LINES.LINE_ID, LOG_LINES.COUNT, LOG_LINES.START_TIME, LOG_LINES.CART_NUMBER, LOG_LINES.ID, CART.TITLE, CART.ARTIST from LOG_LINES INNER JOIN CART WHERE LOG_LINES.CART_NUMBER = CART.NUMBER AND LOG_LINES.LOG_NAME LIKE "AP4_2023_08_09" ORDER BY LOG_LINES.LINE_ID ASC''')

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

    tree.grid(row=0, column=0, sticky='nsew')

    # add a scrollbar
    scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')


    self.gettime()
  pass


  def gettime(self):
    gdt, gtm, ldt, ltm = GetDateTime()
    gdt = gdt[0:4] + '/' + gdt[4:6] + '/' + gdt[6:8]
    gtm = gtm[0:2] + ':' + gtm[2:4] + ':' + gtm[4:6] + ' Z'  
    ldt = ldt[0:4] + '/' + ldt[4:6] + '/' + ldt[6:8]
    ltm = ltm[0:2] + ':' + ltm[2:4] + ':' + ltm[4:6]  
    self.nowGtime.set(gdt)
    self.nowGdate.set(gtm)
    self.LocalTime.set(ldt)
    self.LocalDate.set(ltm)
    myloginfo = GetCartLine()
    print("============================in gettime - Here comes myloginfo: ",myloginfo)
    zfcart = str(myloginfo[0])
    zflogline = str(myloginfo[1])
    tree.selection_set(zflogline)  # Does work.
    tree.see(zflogline)
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

#right bottom corner (misfires in Win10 putting it too low. OK in Ubuntu)
x = ws - w
y = hs - h - 35  # -35 fixes it, more or less, for Win10

#set the dimensions of the screen and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))




root.mainloop()
