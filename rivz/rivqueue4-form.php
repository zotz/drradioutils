<?php

// rivqueue4-form.php
// copyright 2014, drew Roberts
// Licensed under the GPL v2.

// this file will allow queued files to be bid up the queue for play by rdairplay

?>
<a href="index.html">Back To Start</a>
<HR>
<P>
<?php

include("rivdbinfo.inc.php");
include("twoopendb.php");

  $aBidId = $_POST['rivBidUp'];
  $aBidAmt = $_POST['incBidAmt'];
  $nBidAmt = array();
  for($j=0; $j < 20; $j++)
  {
    echo ($j . " || ");
    echo($aBidAmt[$j] . " || ");
    echo($aBidId[$j] . " || "); 
    if ($aBidAmt[$j] != NULL ) 
    {
     echo "aBidAmt is not null! || ";
      $nBidAmt[] = $aBidAmt[$j];
      $nBidId[] = $aBidId[$j];
      echo (" == " . $aBidAmt[$j] . " == ");
      echo (" == " . $aBidId[$j] . " == ");
    }
  }

  $aBidId = $_POST['rivBidUp'];
  $N = count($aBidId);
  echo "N is: ";
  echo $N;
  echo "||";
  for($i=0; $i < $N; $i++)
  {
    echo ($i);
    echo " - BidId: ";
    echo($aBidId[$i] . " || ");
    echo($nBidAmt[$i] . " || ");
  }
  if(empty($aBidId))
  {
    echo("You didn't select anything to Bid Up.");
  }
  else
  {
    $N = count($aBidId);
    $NN = count($nBidAmt);
    echo ("===|||||||||||||||| $N and $NN |||||||||||||||||||===");
    if ($N <> $NN)
    {
      echo ("We have a serious problem, ......... || ");
    }
    else
    {
      echo ("In rivclient2-form");

      echo("You selected $N Bid Up(s): ");
      for($i=0; $i < $N; $i++)
      {
	echo($aBidId[$i] . " ");
	echo($aBidAmt[$i] . " ");
	
	$myBidId=$aBidId[$i];
	$myBidAmt=$nBidAmt[$i];
	echo " myBidId is $myBidId ";
	echo " myBidAmt is $myBidAmt ";
	
	$query2="SELECT * FROM rivque WHERE BidId=\"$myBidId\"";
	echo "query2 is $query2";
	$result2=mysql_query($query2, $rivqueconn);
	if($result2 === FALSE) {
		echo " if we got here we are about to die on a bad result2  ";
		die(mysql_error()); // TODO: better error handling
	}
	echo " query2 is $query2 - got a good result2...  ";
	while($r2=mysql_fetch_array($result2))
	{
		$myCutName=$r2["CUT_NAME"];
		$mycart=$r2["CART_NUMBER"];
		$myartist=$r2["ARTIST"];
		$mytitle=$r2["TITLE"];
	}


	$myBidId = mysql_real_escape_string($myBidId);
	// echo ( "mycutf is -> " . $mycutf . " @@@   ");
	$mycart = mysql_real_escape_string($mycart);
	$myartist = mysql_real_escape_string($myartist);
	$mytitle = mysql_real_escape_string($mytitle);
	$myBidAmt = mysql_real_escape_string($myBidAmt);
	$myBidTime = date ("Y-m-d H:i:s");
	$myBidTime = mysql_real_escape_string($myBidTime);
	echo ("Strings escaped, ready to insert!_+_+_+_+_+_+_");
	// try inserting the chosen song into the rivque table in ajax01 db
	$query3 = "INSERT INTO rivque (BidId, MainBid, ParentBid, CUT_NAME, CART_NUMBER, ARTIST, TITLE, BidAmt, OBidAmt, BidTime) VALUES ( '', '', '$myBidId', '$mycutf', '$mycart', '$myartist', '$mytitle', '$myBidAmt', '$myBidAmt', '$myBidTime' )";
	echo "query3 is: ";
	echo "<pre>$query3</pre>";
	$result3=mysql_query($query3, $rivqueconn);
	if($result3 === FALSE) {
          echo " if we got here we are about to die on a bad result3  ";
	  die(mysql_error()); // TODO: better error handling
	}
	$query4 = "UPDATE rivque SET BidAmt = BidAmt + $myBidAmt WHERE BidId = $myBidId";
	echo "query4 is: ";
	echo "<pre>$query4</pre>";
	$result4=mysql_query($query4, $rivqueconn);
	if($result4 === FALSE) {
          echo " if we got here we are about to die on a bad result4  ";
	  die(mysql_error()); // TODO: better error handling
	}
	echo "Passed supposed insert ";

      }
    }
  }
header("Location: rivclient4.php");
?>
