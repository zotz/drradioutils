<?

// rivreport.php
// copyright 2007, drew Roberts
// Licensed under the GPL v2.

// this file will pull the data from rivendell needed to calculate the time allocated
// to the various events in the
// rivendell grids/clocks/events data


?>
<a href="index.html">Back To Start</a>
<HR>
<P>
<?

include("rivdbinfo.inc.php");
include("rivopendb.php");

$dispcomclk = 1;			//	display commercial clock info
$disptatclk = 1;			//	display timetemp clock info

$myhour = 0;
$hrs=0;
$day=0;
$week=0;

$query="SELECT * FROM SERVICES ORDER BY NAME";
$result=mysql_query($query);
while($r=mysql_fetch_array($result))
{
	// service stuff
	$myservice=$r["NAME"];
	$query="SELECT * FROM EVENTS ORDER BY NAME";
	//$query="SELECT * FROM EVENTS";
	$result1=mysql_query($query);
	while($r1=mysql_fetch_array($result1))
	{
		// event stuff
		$myevent=$r1["NAME"];
		$myprops=$r1["PROPERTIES"];
		$myschgrp=$r1["SCHED_GROUP"];
		$myhour = 0;
		$hrs=0;
		$day=0;
		$week=0;
		echo "IN Event loop: myevent = $myevent : myprops = $myprops";
		while($myhour <= 167)
		{
			// pull info for this event.
			$nowclk = 'CLOCK'. $myhour;
			$hourofday = ($myhour % 24);
			$query="SELECT $nowclk FROM SERVICES WHERE NAME='$myservice'";
			$result=mysql_query($query);
			$clockn=mysql_result($result,0,"$nowclk");
			if ($dispcomclk) {echo "<H2>Clock is: $clockn</H2><BR>";}
			$mytable = $clockn . "_CLK";
			$query="SELECT * FROM $mytable WHERE EVENT_NAME='$myevent' ORDER BY START_TIME";
			if ($dispcomclk) {echo "<BR>Query = $query<BR>";}
			$result2=mysql_query($query);
			while($r2=mysql_fetch_array($result2))
			{
				// stuff for each event in an hour?
				$elength=$r2["LENGTH"];
				if ($dispcomclk) {echo "Event length: - $elength<BR>";}
				$hrs = $hrs + $elength;
			}
			if ($dispcomclk) {echo "Commercial time for Hour$myhour: - $hrs msecs <BR>";}
			$elsecs = ($hrs/1000);
			if ($dispcomclk) {echo "Commercial time for Hour$myhour: - $elsecs secs <BR>";}
			$myhour++;
		}
	
	
	
	}


}
