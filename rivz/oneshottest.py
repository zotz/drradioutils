#!/usr/bin/python

#// oneshottest.py
#// copyright 2020, drew Roberts

#// written to investigate a problem I am having
#// rivfeed4.php is the original php script that works as expected. 
#// rivfeed4.py is the replacement python script that just will not work.
#=========================================================
# From rivfeed4.php
#201227 13:12:05	 2404 Query	SELECT * FROM rivque WHERE MainBid ORDER BY BidAmt DESC, BidId ASC LIMIT 1
#		 2404 Query	DELETE FROM rivque WHERE BidId = '371'
#		 2404 Query	SELECT * FROM rivque WHERE ParentBid = '371'
#		 2404 Query	DELETE FROM rivque WHERE ParentBid = '371'

#		 2404 Query	INSERT INTO rivtran (TranId, BidId, CUT_NAME, CART_NUMBER, ARTIST, TITLE, BidAmt, BidTime, LiveQueTime) VALUES ( '', '371', '010001_001', '10001', 'Rupert & The Rolling Coins', 'The Mail', '6.00', '2020-12-27 13:03:53', '2020-12-27 13:12:06' )
#		 2404 Query	INSERT INTO rivtran (TranId, BidId, ParentBid, CUT_NAME, CART_NUMBER, ARTIST, TITLE, BidAmt, OBidAmt, BidTime, LiveQueTime) VALUES ( '', '372', '371', '010001_001', '10001', 'Rupert & The Rolling Coins', 'The Mail', '2.00', '2.00', '2020-12-27 13:04:06', '2020-12-27 13:12:06' )
#		 2404 Query	INSERT INTO rivtran (TranId, BidId, ParentBid, CUT_NAME, CART_NUMBER, ARTIST, TITLE, BidAmt, OBidAmt, BidTime, LiveQueTime) VALUES ( '', '373', '371', '010001_001', '10001', 'Rupert & The Rolling Coins', 'The Mail', '3.00', '3.00', '2020-12-27 13:04:18', '2020-12-27 13:12:06' )
#=========================================================
# From rivfeed4.py
#201227 13:24:24	 2430 Query	SELECT * FROM rivque WHERE MainBid ORDER BY BidAmt DESC, BidId ASC LIMIT 1
#		 2430 Query	DELETE FROM rivque WHERE BidId = '374'
#		 2430 Query	SELECT * FROM rivque WHERE ParentBid = '374'
#		 2430 Query	DELETE FROM rivque WHERE ParentBid = '374'

#		 2430 Query	INSERT INTO rivtran (TranId, BidId, CUT_NAME, CART_NUMBER, ARTIST, TITLE, BidAmt, BidTime, LiveQueTime) VALUES ( '', '374', '010001_001', '10001', 'Rupert & The Rolling Coins', 'The Mail', '5.00', '2020-12-27 13:15:26', '2020-12-27 13:24:24.894618' )
#		 2430 Query	INSERT INTO rivtran (TranId, BidId, ParentBid, CUT_NAME, CART_NUMBER, ARTIST, TITLE, BidAmt, OBidAmt, BidTime, LiveQueTime) VALUES ( '', '375', '374', '010001_001', '10001', 'Rupert & The Rolling Coins', 'The Mail', '2.00', '2.00', '2020-12-27 13:15:36', '2020-12-27 13:24:24.898540' )
#		 2430 Query	INSERT INTO rivtran (TranId, BidId, ParentBid, CUT_NAME, CART_NUMBER, ARTIST, TITLE, BidAmt, OBidAmt, BidTime, LiveQueTime) VALUES ( '', '376', '374', '010001_001', '10001', 'Rupert & The Rolling Coins', 'The Mail', '2.00', '2.00', '2020-12-27 13:15:45', '2020-12-27 13:24:24.900105' )


import mysql.connector
import os
import subprocess
import time
from datetime import datetime


mydb = mysql.connector.connect(
	host="localhost",
	user="rduser",
	password="letmein",
	database="rivz"
)

mycursor = mydb.cursor()

def changedz(myfile, mycursor):

	query4 = "SELECT * FROM rivque WHERE MainBid ORDER BY BidAmt DESC, BidId ASC LIMIT 1"
	mycursor.execute(query4)
	myresult = mycursor.fetchall()
	print("Here comes the result...")
	print(myresult)
	for x in myresult:
		mycart = (x[4])
		myBidId = (x[0])
		myParentBid = (x[2])
		print(query4)
		print("From Q4: myBidId is: " + str(myBidId))
		# // if got a bid follows
		if (myBidId > 0):
			mycut = (x[3])
			myartist = (x[5])
			mytitle = (x[6])
			myBidAmt = (x[7])
			myBidTime = (x[9])
			print("Q5:myBidId is: " + str(myBidId))
			query5 = "DELETE FROM rivque WHERE BidId = '%s'"
			print(query5)
			mycursor.execute(query5, (myBidId, ))
			myLiveQueTime = datetime.now()
			print("Q6:myBidId is: " + str(myBidId))
			query6 = "INSERT INTO rivtran (TranId, BidId, CUT_NAME, CART_NUMBER, ARTIST, TITLE, BidAmt, BidTime, LiveQueTime) VALUES ( '', '%s', %s, '%s', %s, %s, %s, %s, %s )"
			print(query6)
			mycursor.execute(query6, (myBidId, mycut, mycart, myartist, mytitle, myBidAmt, myBidTime, myLiveQueTime))
			myParentBid = myBidId
			# $query7 = "SELECT * FROM rivque WHERE ParentBid = '$myParentBid'";
			print("Q7:myBidId is: " + str(myBidId))
			print("Q7:myParentBid is: " + str(myParentBid))
			query7 = "SELECT * FROM rivque WHERE ParentBid = '%s'"
			print(query7)
			mycursor.execute(query7, (myParentBid, ))
			myresulty = mycursor.fetchall()
			for y in myresulty:
				print("Here comes y: ")
				print y
				myBidId = (y[0])
				mycut = (y[3])
				mycart = (y[4])
				myartist = (y[5])
				mytitle = (y[6])
				myBidAmt = (y[7])
				myOBidAmt = (y[8])
				myBidTime = (y[9])
				myLiveQueTime = datetime.now()
				print("Q8:myBidId is: " + str(myBidId))
				print("Q8:myParentBid is: " + str(myParentBid))
				query8 = "INSERT INTO rivtran (TranId, BidId, ParentBid, CUT_NAME, CART_NUMBER, ARTIST, TITLE, BidAmt, OBidAmt, BidTime, LiveQueTime) VALUES ( '', '%s', '%s', %s, '%s', %s, %s, %s, %s, %s, %s )"
				print(query7)
				mycursor.execute(query8, (myBidId, myParentBid, mycut, mycart, myartist, mytitle, myBidAmt, myOBidAmt, myBidTime, myLiveQueTime))
			print("Q9:myBidId is: " + str(myBidId))
			print("Q9:myParentBid is: " + str(myParentBid))
			query9 = "DELETE FROM rivque WHERE ParentBid = '%s'"
			print(query9)
			mycursor.execute(query9, (myParentBid, ))


changedz("/tmp/nowplayzlong.txt", mycursor);

