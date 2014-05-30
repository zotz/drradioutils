<?php

// rivlib4-form.php
// copyright 2014, drew Roberts
// Licensed under the GPL v2.

// this file will allow files to be queued for play by rdairplay



include("rivdbinfo.inc.php");
include("twoopendb.php");

  $aCut = $_POST['rivExport'];
  $aBidAmt = $_POST['lrivBidAmt'];
  $lp = $_POST['lpg'];
  $nBidAmt = array();
  for($j=0; $j < 10; $j++)
  {
    //echo ($j . " || ");
    //echo($aBidAmt[$j] . " || ");
    //echo($aCut[$j] . " || "); 
    if ($aBidAmt[$j] != NULL ) 
    {
     //echo "aBidAmt is not null! || ";
      $nBidAmt[] = $aBidAmt[$j];
      //echo (" == " . $aBidAmt[$j] . " == ");
    }
  }

  $aCut = $_POST['rivExport'];
  $N = count($aCut);
  //echo "N is: ";
  //echo $N;
  //echo "||";
  for($i=0; $i < $N; $i++)
  {
    //echo ($i);
    //echo " - Cut: ";
    //echo($aCut[$i] . " || ");
    //echo($nBidAmt[$i] . " || ");
  }
  if(empty($aCut))
  {
    //echo("You didn't select anything to queue.");
  }
  else
  {
    $N = count($aCut);
    $NN = count($nBidAmt);
    //echo ("===|||||||||||||||| $N and $NN |||||||||||||||||||===");
    if ($N <> $NN)
    {
      //echo ("We have a serious problem, you entered bids for unselected songs. || ");
    }
    else
    {
      //echo ("In rivqueue-form");

      //echo("You selected $N cut(s): ");
      for($i=0; $i < $N; $i++)
      {
	//echo($aCut[$i] . " ");
	//echo($aBidAmt[$i] . " ");
	$mycut=$aCut[$i];
	$myBidAmt=$nBidAmt[$i];
	//echo " mycut is $mycut ";
	//echo " myBidAmt is $myBidAmt ";
	$query="SELECT * FROM CUTS WHERE CUT_NAME=\"$mycut\"";
	$result=mysql_query($query, $rivconn);
	//echo "just did the query for result";
	if($result === FALSE) {
      		  //echo " if we got here we are about to die on a bad result  ";
    		  die(mysql_error()); // TODO: better error handling
	}
	//echo " query is $query - got a good result...  ";
	while($r=mysql_fetch_array($result))
	{
      		  $mycart=$r["CART_NUMBER"];
		  //echo "mycart is $mycart";
		  $query2="SELECT * FROM CART WHERE NUMBER=\"$mycart\"";
		  //echo "query2 is $query2";
		  $result2=mysql_query($query2, $rivconn);
		  if($result2 === FALSE) {
			  //echo " if we got here we are about to die on a bad result2  ";
    			  die(mysql_error()); // TODO: better error handling
		  }
		  //echo " query2 is $query2 - got a good result2...  ";
		  while($r2=mysql_fetch_array($result2))
		  {
			  $myartist=$r2["ARTIST"];
			  $mytitle=$r2["TITLE"];
			  $myalbum=$r2["ALBUM"];
			  //echo "myartist is $myartist";
		  }
	  }

	//$output = shell_exec("/usr/bin/rmlsend PX\ 1\ \"$mycart\"\!");
	//echo "<pre>$output</pre>";
	// escape strings
	$mycutf = mysql_real_escape_string($mycut);
	// echo ( "mycutf is -> " . $mycutf . " @@@   ");
	$mycart = mysql_real_escape_string($mycart);
	$myartist = mysql_real_escape_string($myartist);
	$mytitle = mysql_real_escape_string($mytitle);
	$myBidAmt = mysql_real_escape_string($myBidAmt);
	$myBidTime = date ("Y-m-d H:i:s");
	$myBidTime = mysql_real_escape_string($myBidTime);
	//echo ("Strings escaped, ready to insert!_+_+_+_+_+_+_");
	// try inserting the chosen song into the rivque table in ajax01 db
	$query3 = "INSERT INTO rivque (BidId, MainBid, CUT_NAME, CART_NUMBER, ARTIST, TITLE, BidAmt, OBidAmt, BidTime) VALUES ( '', '1', '$mycutf', '$mycart', '$myartist', '$mytitle', '$myBidAmt', '$myBidAmt', '$myBidTime' )";
	//echo "query3 is: ";
	//echo "<pre>$query3</pre>";
	$result3=mysql_query($query3, $rivqueconn);
	if($result3 === FALSE) {
          echo " if we got here we are about to die on a bad result3  ";
	  die(mysql_error()); // TODO: better error handling
	}
	//echo "Passed supposed insert ";

      }
    }
  }
  //echo "lpage=$lp";
header("Location: rivclient4.php?lpage=$lp");
?>
