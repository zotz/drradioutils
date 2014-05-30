#!/usr/bin/php
<?php

// rivfeed4.php
// copyright 2014, drew Roberts
// Licensed under the GPL v2.

// this file will work with the rivqueue system to feed another song to
// rdairplay as next and remove it from the rivqueue queue when
// it sees rdairplay spit out some now and next data

// NOT WORKING YET!

include("rivdbinfo.inc.php");
include("twoopendb.php");

function changedz($file, $rqc)
{
    $size = filesize($file);
    $updatez = 0;
    $adtimez = 0;
    $updadz = 0;
    $debugfile = '/home/rduser/feeddebug.txt';
    file_put_contents($debugfile, '');
    while (true) 
	{
		clearstatcache();
		$currentSize = filesize($file);
		if ($size == $currentSize) // a change in size signals info from riv that now&next changed, song finished
		{
			// keep looping and doing nothing as long as we dont get signalled that the song changed
			sleep(20);
			continue;
		} // endif size = currentsize

		if ($updatez % 2 == 0 ) // this is needed because the rml insert from our queue changes next which looks like a song end but isn't
		{
			// we need to handle the fact that a song ended
			echo ("updatez is even." . PHP_EOL );
			echo ("Audio ended, let's do something!" . PHP_EOL);
			// try doing song or ad in the even part
			if ($adtimez % 8 == 0 ) // trying to run an ad every 4 bits of audio
			{
				// insert an ad here
				echo ("OK, so updatez is even and adtimez is divisibale by 8 process and ad." . PHP_EOL );
				echo ("Updatez = $updatez and Adtimez = $adtimez " . PHP_EOL );
				$current = "ADPROC: U=".$updatez." A=".$adtimez." Queued AD cart for playing next." . PHP_EOL;
				file_put_contents($debugfile, $current, FILE_APPEND);

				$outputad = shell_exec("/usr/bin/rmlsend PX\ 1\ \"1\"\!");
				echo ("Ad inserted!" . PHP_EOL);
				// end insert ad code
			} //endif $adtimez % 8 == 0
			else // $adtimez % 8 != 0
			{
				// run a song
				echo ("OK, so updatez is even and adtimez is not divisibale by 8 process a song." . PHP_EOL );

				echo ("Size = " . $size . " |||  CurrentSize = " . $currentSize . PHP_EOL );
				$query4 = "SELECT * FROM rivque WHERE MainBid ORDER BY BidAmt DESC, BidId ASC LIMIT 1";
				echo "query4 is: ";
				echo "<pre>$query4</pre>". PHP_EOL ;
				$result4=mysql_query($query4, $rqc);
				if($result4 === FALSE)
				{
					echo " if we got here we are about to die on a bad result4  ";
					die(mysql_error()); // TODO: better error handling
				} // endif result4 === FALSE
				$r4=mysql_fetch_array($result4);
				$mycart = $r4["CART_NUMBER"];
				echo ("mycart is::: " . $mycart . " ::: ");
				$myBidId = $r4["BidId"];
				echo ("    Our BidId is-----: " . $myBidId . "   ----:    ". PHP_EOL );
				// if got a bid follows
				if ( !(is_null($myBidId)) ) // got a bid
				{
					echo ("We have a valid item to process!". PHP_EOL );
					$mycut = mysql_real_escape_string($r4["CUT_NAME"]);
					$myartist = mysql_real_escape_string($r4["ARTIST"]);
					$mytitle = mysql_real_escape_string($r4["TITLE"]);
					$myBidAmt = $r4["BidAmt"];
					$myBidTime = $r4["BidTime"];
					
					echo ("Updatez = $updatez and Adtimez = $adtimez " . PHP_EOL );
					$current = "SGPROC: U=".$updatez." A=".$adtimez. " Queued $mytitle by $myartist for playing next." . PHP_EOL;
					file_put_contents($debugfile, $current, FILE_APPEND);
					
					$output = shell_exec("/usr/bin/rmlsend PX\ 1\ \"$mycart\"\!");
					$size = $currentSize;
					$nextfile = fopen("nextup.txt","w");
					echo fwrite($nextfile,"NextUp $mytitle by $myartist!");
					fclose($nextfile);
					$query5 = "DELETE FROM rivque WHERE BidId = '$myBidId'";
					echo "     query5 is:     ";
					echo "   <pre>$query5</pre>     " . PHP_EOL;
					$result5=mysql_query($query5, $rqc);
				    if($result5 === FALSE)
				    {
						echo " if we got here we are about to die on a bad result5  ";
						die(mysql_error()); // TODO: better error handling
				    } //endif result5 === FALSE
				    $myLiveQueTime = date ("Y-m-d H:i:s");
				    $myLiveQueTime = mysql_real_escape_string($myLiveQueTime);
				    $query6 = "INSERT INTO rivtran (TranId, BidId, CUT_NAME, CART_NUMBER, ARTIST, TITLE, BidAmt, BidTime, LiveQueTime) VALUES ( '', '$myBidId', '$mycut', '$mycart', '$myartist', '$mytitle', '$myBidAmt', '$myBidTime', '$myLiveQueTime' )";
				    echo "     query6 is:     ";
				    echo "   <pre>$query6</pre>     " . PHP_EOL;
				    $result6=mysql_query($query6, $rqc);
				    if($result6 === FALSE)
				    {
						echo " if we got here we are about to die on a bad result6  ";
						die(mysql_error()); // TODO: better error handling
				    } //endif result6 === FALSE
				    $myParentBid = mysql_real_escape_string($myBidId);
				    $query7 = "SELECT * FROM rivque WHERE ParentBid = '$myParentBid'";
				    echo "     query7 is:     ";
				    echo "   <pre>$query7</pre>     " . PHP_EOL;
				    $result7=mysql_query($query7, $rqc);
				    if($result7 === FALSE)
				    {
						echo " if we got here we are about to die on a bad result7  ";
						die(mysql_error()); // TODO: better error handling
				    }  // endif result7 === FALSE
				    while($r7=mysql_fetch_array($result7))
				    {
				    	// loop through all subbids for just "played" and insert into rivtran. then delete them from rivque later
						$myBidId=mysql_real_escape_string($r7["BidId"]);
						$mycart=mysql_real_escape_string($r7["CART_NUMBER"]);
						$mycut=mysql_real_escape_string($r7["CUT_NAME"]);
						$myartist=mysql_real_escape_string($r7["ARTIST"]);
						$mytitle=mysql_real_escape_string($r7["TITLE"]);
						$mysBidAmt=mysql_real_escape_string($r7["BidAmt"]);
						$myOBidAmt=mysql_real_escape_string($r7["OBidAmt"]);
						$myBidTime=mysql_real_escape_string($r7["BidTime"]);
						$query8 = "INSERT INTO rivtran (TranId, BidId, ParentBid, CUT_NAME, CART_NUMBER, ARTIST, TITLE, BidAmt, OBidAmt, BidTime, LiveQueTime) VALUES ( '', '$myBidId', '$myParentBid', '$mycut', '$mycart', '$myartist', '$mytitle', '$mysBidAmt', '$myOBidAmt', '$myBidTime', '$myLiveQueTime' )";
						echo "     query8 is:     ";
						echo "   <pre>$query8</pre>     " . PHP_EOL;
						$result8=mysql_query($query8, $rqc);
						if($result8 === FALSE)
						{
							echo " if we got here we are about to die on a bad result8  ";
							die(mysql_error()); // TODO: better error handling
						} //endif result8 === FALSE
				    } // endwhile r7=mysql_fetch_array($result7) done inserting into rivtran
				    // ok, loop done for adding to rivtran, now delete from rivque
				    $query9 = "DELETE FROM rivque WHERE ParentBid = '$myParentBid'";
				    echo "     query9 is:     ";
				    echo "   <pre>$query9</pre>     " . PHP_EOL;
				    $result9=mysql_query($query9, $rqc);
				    if($result9 === FALSE)
				    {
						echo " if we got here we are about to die on a bad result9  ";
						die(mysql_error()); // TODO: better error handling
					} // endif result9 === FALSE
				} // endif !(is_null($myBidId)) end got a bid processing
				else // did not get a bid
				{
					$updatez = $updatez + 1;
					$adtimez = $adtimez + 1;
					echo ("No songs in Bid Que to process!" . PHP_EOL );
					$current = "NSPROC: U=".$updatez." A=".$adtimez." No songs in QUEUE play from log........................................" . PHP_EOL;
					file_put_contents($debugfile, $current, FILE_APPEND);
				} // endelse did not get a bid
				$size = $currentSize;
				echo ("Size = " . $size . " |||  CurrentSize = " . $currentSize . PHP_EOL );
			} // endelse $adtimez % 8 != 0
		} // endif $updatez % 2 == 0
		else // $updatez % 2 != 0
		{
			// do nothing here as this happens on making the above next
			echo ("updatez is odd." . PHP_EOL );
			echo ("OK, so updatez is odd and adtimez does not matter, cool out." . PHP_EOL );
			echo ("Updatez = $updatez and Adtimez = $adtimez " . PHP_EOL );
			$current = "CHPROC: U=".$updatez." A=".$adtimez."--------------------".PHP_EOL;
			file_put_contents($debugfile, $current, FILE_APPEND);
			$size = $currentSize;
			echo ("Chillin for a bit.." . PHP_EOL  . PHP_EOL . PHP_EOL . PHP_EOL);
			sleep(15);
		} // endelse $updatez % 2 != 0
		$updatez = $updatez + 1;
		$adtimez = $adtimez + 1;
	} // end while true
} //end function changeds



//include("rivdbinfo.inc.php");
//include("twoopendb.php");
changedz("/tmp/nowplayzlong.txt", $rivqueconn);
