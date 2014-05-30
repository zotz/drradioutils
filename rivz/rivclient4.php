<?php

// rivclient4.php
// copyright 2014, drew Roberts
// Licensed under the GPL v2.

// this file will allow files to be queued for play by rdairplay


?>
<html>
  <head>
    <meta http-equiv="refresh" content="15" >
    <title>Riv Client 4 Combo. Bid up songs already bid on OR Add new songs to Bid Queue.</title>
  </head>
  <body>
<a href="index.html">Back To Start</a>
<HR>
<table border="1">
<tr><td> Playing: </td><td> Ogg Stream </td><td> MP3 Stream </td><td> Next Up: </td></tr>
<tr><td><B>
<?php
include("/tmp/nowplayz.txt");
?></B></td><td> <a href="http://192.168.86.224:8002/rockriv.ogg.m3u">Ogg </a> </td><td> <a href="http://192.168.86.224:8002/rockriv-low.mp3.m3u">MP3 </a> </td><td>
<B><?php
include("/tmp/nextplayz.txt");
?></B></td></tr>
</table>




<HR>
<P>
This is the Bid Queue section. Here you can see the songs that have already been bid on and put into a queue to be played when it is their turn. You can Bid them Up so that they move up the queue and play sooner. Just tick the BidUp column and enter the amount to bid in the Bid Amount column and then click the BidUp button. You can BidUp more than one song at a time. Click the numbers below the BidUp button to see other pages in the queue.
<P>

    
    <div id="Queue_Section">Queue_Section


<?php

include("rivdbinfo.inc.php");
include("twoopendb.php");

if (isset($_GET["qpage"])) { $qpage  = $_GET["qpage"]; } else { $qpage=1; };
if (isset($_GET["lpage"])) { $lpage  = $_GET["lpage"]; } else { $lpage=1; };

$qperpage = 10;
$qstart_from = ($qpage-1) * $qperpage;

$query="SELECT * FROM rivque WHERE MainBid ORDER BY BidAmt DESC, BidId ASC LIMIT $qstart_from, $qperpage";
$result=mysql_query($query, $rivqueconn);


?>


<form action="rivqueue4-form.php" method="post">
<table border="1">
<tr><td>CurrentBidAmt</td><td>BidId</td><td>Artist</td><td>Song Title</td><td> <B>BidUp?(tick)</B></td><td><B>Bid Amount</B></td><td>Cut Name</td><td>Cart Number</td><td>Last Bid Time</td></tr>
<?php

$myartist="None";

while($r=mysql_fetch_array($result))
{
	$mycart=$r["CART_NUMBER"];
	//echo $mycart;

	?>
	<tr>
	<td><?php echo $r["BidAmt"];?> </td>
	<td><?php echo $r["BidId"]; ?> </td>
	<td><?php echo $r["ARTIST"]; ?> </td>
	<td><?php echo $r["TITLE"]; ?> </td>
	<td><input type="checkbox" name="rivBidUp[]" value=<?php echo $r["BidId"]; ?> /></td>
	<td><input type="text" name="incBidAmt[]" value=></td>
        <td><?php echo $r["CUT_NAME"]; ?> </td>
        <td><?php echo $r["CART_NUMBER"]; ?> </td>
	<td><?php echo $r["BidTime"]; ?> </td>	
        </tr>
<?php
};
?>
<input type="hidden" name="qpg" value="<?php echo $qpage;?>" />
</table>
<input type="submit" name="formSubmit" value="BidUp" />
 
</form>

<?php
$qsql = "SELECT COUNT(CUT_NAME) FROM rivque";
$qrs_result = mysql_query($qsql, $rivqueconn);
//echo $rs_result;
$qrow = mysql_fetch_row($qrs_result);
$qtotal_records = $qrow[0];
$qtotal_pages = ceil($qtotal_records / $qperpage);
  
for ($qi=1; $qi<=$qtotal_pages; $qi++) {
	    echo "<a href='rivclient4.php?qpage=".$qi.",lpage=".$lpage."'>".$qi."</a> ";
};


##################################################################################################################
?>
</div>
<HR>
<P>This is our Library Section. Here you can see all the songs in our library and place a bid on them to put them in the queue to be played. You will enter the queue above songs with lower bids but after songs already in the queue that were there before you. Just tick the BidOn column and place your bid in the Bid Amount column and then click on the BidOn button. You can BidOn more than once song at a time. Click the numbers below the BidOn button to see other pages in our library.
<P>

    
    <div id="Library_Section">Library_Section

<?php

// from rivqueue.php
// copyright 2014, drew Roberts
// Licensed under the GPL v2.

// this file will allow files to be queued for play by rdairplay

# Display first page (or correct page) of songs at 10 per page
# have to set the lpage at the top now instead of just below
#if (isset($_GET["lpage"])) { $lpage  = $_GET["lpage"]; } else { $lpage=1; };

$perpage = 10;
$lstart_from = ($lpage-1) * $perpage;



$lquery="SELECT * FROM rivendellmain WHERE GROUP_NAME = 'MUSIC' ORDER BY ARTIST ASC, NUMBER ASC LIMIT $lstart_from, $perpage";
$lresult=mysql_query($lquery, $rivqueconn);

?>
<form action="rivlib4-form.php" method="post">
<table border="1">
<tr><td>Artist</td><td>Song Title</td><td><B>BidOn?(tick)</B></td><td><B>Bid Amount</B></td><td>Cut Name</td><td>Cart Number</td></tr>
<?php


// display first page of songs in a form to allow selecting and bidding
while($lr=mysql_fetch_array($lresult))
{
	?>
	<tr>
	<td><?php echo $lr["ARTIST"]; ?></td>
	<td><?php echo $lr["TITLE"]; ?></td>
	<td><input type="checkbox" name="rivExport[]" value=<?php echo $lr["CUT_NAME"]; ?> </td>
	<td><input type="text" name="lrivBidAmt[]" value=></td>
        <td><?php echo $lr["CUT_NAME"]; ?></td>
        <td><?php echo $lr["NUMBER"]; ?></td>	
        </tr>
<?php
};
?>
<input type="hidden" name="lpg" value="<?php echo $lpage;?>" />
</table>
<input type="submit" name="lformSubmit" value="BidOn" />
 
</form>

<?php
// calculatge number of pages of songs and make links
$lsql = "SELECT COUNT(CUT_NAME) FROM CUTS";
$lrs_result = mysql_query($lsql, $rivconn);
//echo $lrs_result;
$lrow = mysql_fetch_row($lrs_result);
$ltotal_records = $lrow[0];
$ltotal_pages = ceil($ltotal_records / $perpage);
  
for ($li=1; $li<=$ltotal_pages; $li++) {
            echo "<a href='rivclient4.php?lpage=".$li.",qpage=".$qpage."'>".$li."</a> ";
};
?>
</div>

    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
    <script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/jquery-ui.min.js"></script>



</body>
</html>
