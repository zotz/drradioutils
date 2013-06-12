<?

// based on select1.php by Robert Orr
//
//	I need to try and figure out the logic here as something is not working
//	the way I think it should.

// error_reporting(0);

include("opendb.php");			// open the trafficgenny database

$date=$tdate;				// this is the date passed in from the form
$lyr=substr($date,0,4);			// get the year part of the date
$lmn=substr($date,5,2);			// get the month part of the date
$ldy=substr($date,8,2);			// get the day part of the date

$query = "SELECT DAYNAME('$date')"; 	// figure the doy of the week of the date
$result = mysql_query($query);		// see above
if (!$result)
{
    die('Could not query1:' . mysql_error());
}
$dayoweek = mysql_result($result,$i,"DAYNAME('$date')");	// see above $dayoweek is the word form

echo "<center><H1>Traffic Schedule for $dayoweek, $date.</H1></center><BR><HR><BR>";

$ctr=1;								// I need to figure exactly what this counter is supposed to do
$query = "SELECT * FROM sheet";			// get all the ads from the sheet table
$result = mysql_query($query);			// see above
$num_rows = mysql_num_rows($result);		// the number of ads in the sheet table
//$rowlimit = $num_rows + '1';			// I added this - not sure why yet...
$rowlimit = $num_rows + '0';			// I added this - not sure why yet... try this way


$myFLoc = "/var/sndtraf/";						// location for traffic log file - perhaps move to inc file
$myFile = $myFLoc . "tr" . $lyr . $lmn . $ldy . ".log";		// traffic log file name - includes location
$fh = fopen($myFile, 'w') or die("Error!!");			// open log file as a test??? to clear it out???
fclose($fh);							// close log file

//while ( $ctr <=$num_rows ) {
//I wanted to do the above line but it won't generate correctly if any ads have been taken out of the database so I set the line below to a value high enough for my purposes (520)... ugly huh

while ( $ctr <= $rowlimit )					// do this once for each ad??? - yes... this processes ads from the sheet table one by one
{
	$query="SELECT * from sheet WHERE id=$ctr";		// select the ad from the sheet table
	$result = mysql_query($query);
	if (!$result)
	{
		die('Could not query0:' . mysql_error());
	}
	$r=mysql_fetch_array($result);
	$id=$r["id"];
	$advertiser=$r["advertiser"];
	$cartnumber=$r["cartnumber"];
	$startdate=$r["startdate"];
	$enddate=$r["enddate"];
	$starttime=$r["starttime"];
	$endtime=$r["endtime"];
	$flight=$r["flight"];
	$tempspnsr=$r["tempspnsr"];
	$monday=$r["monday"];
	$tuesday=$r["tuesday"];
	$wednesday=$r["wednesday"];
	$thursday=$r["thursday"];
	$friday=$r["friday"];
	$saturday=$r["saturday"];
	$sunday=$r["sunday"];
	if ($dayoweek == "Monday")				// should be a better way to do this next bit
	{							// but the attempt that follows doesnt seem
		$numperday = $monday;				// to work
	}
	if ($dayoweek == "Tuesday")
	{
		$numperday = $tuesday;
	}
	if ($dayoweek == "Wednesday")
	{
		$numperday = $wednesday;
	}
	if ($dayoweek == "Thursday")
	{
		$numperday = $thursday;
	}
	if ($dayoweek == "Friday")
	{
		$numperday = $friday;
	}
	if ($dayoweek == "Saturday")
	{
		$numperday = $saturday;
	}
	if ($dayoweek == "Sunday")
	{
		$numperday = $sunday;
	}
	//$numperday = $r['$dayoweek'];				// this is the easier bit that doesnt want to work

	$ctr2=0;
	while ( $ctr2 < $numperday )				// do this loop once for each time an ad is supposed to run this day for this ad
	{
		// have to figure out this stuff...
		// MOD(A,B) returns the remainder of A divided by B
		// DATEDIFF(expr1,expr2) gives the number of days between the dates expr1 and expr2
		
		$query="SELECT MOD(DATEDIFF('$date','$startdate'),(7*'$flight')) as remain";
		$result = mysql_query($query);
		if (!$result)
		{
               	    die('Could not query3:' . mysql_error());
               	}
		$remain0 = mysql_result($result,$i,"remain");
		$query="SELECT MOD(DATEDIFF('$date',ADDDATE('$startdate',INTERVAL 1 DAY)),(7*'$flight')) as remain";
		$result = mysql_query($query);                           
		$remain1 = mysql_result($result,$i,"remain");
		$query="SELECT MOD(DATEDIFF('$date',ADDDATE('$startdate',INTERVAL 2 DAY)),(7*'$flight')) as remain";
		$result = mysql_query($query);
		$remain2 = mysql_result($result,$i,"remain");
		$query="SELECT MOD(DATEDIFF('$date',ADDDATE('$startdate',INTERVAL 3 DAY)),(7*'$flight')) as remain";
		$result = mysql_query($query);
		$remain3 = mysql_result($result,$i,"remain");
		$query="SELECT MOD(DATEDIFF('$date',ADDDATE('$startdate',INTERVAL 4 DAY)),(7*'$flight')) as remain";
		$result = mysql_query($query);
		$remain4 = mysql_result($result,$i,"remain");
		$query="SELECT MOD(DATEDIFF('$date',ADDDATE('$startdate',INTERVAL 5 DAY)),(7*'$flight')) as remain";
		$result = mysql_query($query);
		$remain5 = mysql_result($result,$i,"remain");
		$query="SELECT MOD(DATEDIFF('$date',ADDDATE('$startdate',INTERVAL 6 DAY)),(7*'$flight')) as remain";
		$result = mysql_query($query);
		$remain6 = mysql_result($result,$i,"remain");
		$query="SELECT * from timeslots WHERE ('$starttime' <= times AND '$endtime' >= times AND used = 0 AND close = 0 AND '$startdate' <= '$date' AND '$enddate' >= '$date') AND $tempspnsr = 0 AND ('$remain0' = 0 OR '$remain1' = 0 OR  '$remain2' = 0 OR '$remain3' = 0 OR '$remain4' = 0 OR '$remain5' = 0 OR '$remain6' = 0) ORDER BY RAND() LIMIT 0,1";
		$result = mysql_query($query);
		if (!$result)
		{
			die('Could not query3:' . mysql_error());
		}
		$r1=mysql_fetch_array($result);
		if ($firsttime=$r1["times"])
		{
			echo "$firsttime $cartnumber $advertiser <br>";
			$fh = fopen($myFile, 'a') or die("Error!!");
			fwrite($fh, "$firsttime $cartnumber $advertiser\r\n");
			fclose($fh);
			//echo "Recorded!!";
			//I didn't get writing to a file (the above 5 lines working)
		}
		$tid=$r1["tsid"];
		$query="UPDATE timeslots SET used=1 WHERE tsid='$tid'";
		$result = mysql_query($query);
		if (!$result)
		{
			die('Could not query4:' . mysql_error());
		}
               	$query="UPDATE timeslots SET close=1 WHERE times < (SELECT ADDTIME('$firsttime','$offset')) AND times > (SELECT SUBTIME('$firsttime','$offset'))";
               	$result = mysql_query($query);
		if (!$result)
		{
	       		die('Could not query5:' . mysql_error());
               	}
		$query="SELECT * from tempspnsrtimeslots WHERE ('$starttime' <= times AND '$endtime' >= times AND used = 0 AND close = 0 AND '$startdate' <= '$date' AND '$enddate' >= '$date') AND $tempspnsr = 1 AND ('$remain0' = 0 OR '$remain1' = 0 OR  '$remain2' = 0 OR '$remain3' = 0 OR '$remain4' = 0 OR '$remain5' = 0 OR '$remain6' = 0) ORDER BY RAND() LIMIT 0,1";
		$result = mysql_query($query);
		if (!$result)
		{
			die('Could not query3:' . mysql_error());
               	}
		$r2=mysql_fetch_array($result);
		if ($firsttime=$r2["times"])
		{
               		echo "$firsttime $cartnumber $advertiser <br>";
                       	$fh = fopen($myFile, 'a') or die("Error!!");
                       	fwrite($fh, "$firsttime $cartnumber $advertiser\r\n");
                       	fclose($fh);
                       	//echo "Recorded!!";
               	}
		$tid=$r2["tsid"];
               	$query="UPDATE tempspnsrtimeslots SET used=1 WHERE tsid='$tid'";
               	$result = mysql_query($query);
               	if (!$result)
		{
               		die('Could not query4:' . mysql_error());
               	}
               	$query="UPDATE tempspnsrtimeslots SET close=1 WHERE times < (SELECT ADDTIME('$firsttime','$offset')) AND times > (SELECT SUBTIME('$firsttime','$offset'))";
               	$result = mysql_query($query);
               	if (!$result)
		{
               		die('Could not query5:' . mysql_error());
               	}
		$ctr2++;
	}
	$query="UPDATE timeslots SET close=0";
        $result = mysql_query($query);
        if (!$result)
	{
		die('Could not query6:' . mysql_error());
	}
	$query="UPDATE tempspnsrtimeslots SET close=0";
	$result = mysql_query($query);
	if (!$result)
	{
		die('Could not query6:' . mysql_error());
	}
	$ctr++;
}

$query="UPDATE timeslots SET used=0";
$result = mysql_query($query);
if (!$result)
{
	die('Could not query5:' . mysql_error());
}
$query="UPDATE tempspnsrtimeslots SET used=0";
$result = mysql_query($query);
if (!$result)
{
	die('Could not query5:' . mysql_error());
}

echo "<BR><HR><BR>";
echo "You can cut and paste from here, of find this info in: $myFile ...";
echo "<BR><HR><BR>";

?>
