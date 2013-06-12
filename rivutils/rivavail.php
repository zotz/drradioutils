<?

// rivavail.php
// copyright 2007, drew Roberts
// Licensed under the GPL v2.

// this file will pull the data from rivendell needed to calculate the available commercial
// and time sponsor times.
// from the rivendell grids/clocks/events data

// for this to work properly, you need events in rivendell rdlogmanager called "Commercial" and "Timetemp"
// you can leave "Timetemp" out of the mix if you do not want to use that functionality

?>
<a href="index.html">Back To Start</a>
<HR>
<P>
<?

include("rivdbinfo.inc.php");
include("rivopendb.php");

$dispcomclk = 1;			//	display commercial clock info
$disptatclk = 1;			//	display timetemp clock info

// ------------------------ first for commercials -------------------------------------------------

$myhour = 0;
$hrs=0;
$day=0;
$week=0;
if ($dispcomclk) {echo "<BR><HR><BR>";}
while($myhour <= 167)
{
	{
		$nowclk = 'CLOCK'. $myhour;
		$hourofday = ($myhour % 24);
		if ($dispcomclk) {echo "<BR><H1>Hour of Day is $hourofday</H1><BR>";}
		$query="SELECT $nowclk FROM SERVICES WHERE NAME='Production'";
		$result=mysql_query($query);
		$clockn=mysql_result($result,0,"$nowclk");
		if ($dispcomclk) {echo "<H2>Clock is: $clockn</H2><BR>";}
		$mytable = $clockn . "_CLK";
		$query="SELECT * FROM $mytable WHERE EVENT_NAME='Commercial' ORDER BY START_TIME";
		if ($dispcomclk) {echo "<BR>Query = $query<BR>";}
		$result=mysql_query($query);
		while($r=mysql_fetch_array($result))
		{
			$elength=$r["LENGTH"];
			if ($dispcomclk) {echo "Event length: - $elength<BR>";}
			$hrs = $hrs + $elength;
		}
		if ($dispcomclk) {echo "Commercial time for Hour$myhour: - $hrs msecs <BR>";}
		$elsecs = ($hrs/1000);
		if ($dispcomclk) {echo "Commercial time for Hour$myhour: - $elsecs secs <BR>";}
		$elmins = ($elsecs/60);
		if ($dispcomclk) {echo "Commercial time for Hour$myhour: - $elmins mins <BR>";}
		$elhours = ($elmins/60);
		if ($dispcomclk) {echo "Commercial time for Hour$myhour: - $elhours hours <BR>";}
		$myhour++;
		$day = ($day + $hrs);
		$week = ($week + $hrs);
		$daymins = (($day/1000)/60);
		$weekmins = (($week/1000)/60);
		$dayhours = ((($day/1000)/60)/60);
		$weekhours = ((($week/1000)/60)/60);
		if ($dispcomclk) {echo "Commercial time for the day: - $daymins mins <BR>";}
		if ($dispcomclk) {echo "Commercial time for the day: - $dayhours hours <BR>";}
		if ($dispcomclk) {echo "Commercial time for the week: - $weekmins mins <BR>";}
		if ($dispcomclk) {echo "Commercial time for the week: - $weekhours hours <BR>";}
		if ($dispcomclk) {echo "<BR><HR><BR>";}
	}
	$hrs = 0;
	if (($myhour % 24) == 0)
	{
		$day=0;
		if ($dispcomclk) {echo "<BR><HR><BR>";}
	}
}

//	------------------------ nor for time sponsors ------------------------------

$myhour = 0;
$thrs=0;
$tday=0;
$tweek=0;
if ($dispcomclk) {echo "<BR><HR><BR>";}
while($myhour <= 167)
{
	{
		$nowclk = 'CLOCK'. $myhour;
		$hourofday = ($myhour % 24);
		if ($dispcomclk) {echo "<BR><H1>Hour of Day is $hourofday</H1><BR>";}
		$query="SELECT $nowclk FROM SERVICES WHERE NAME='Production'";
		$result=mysql_query($query);
		$clockn=mysql_result($result,0,"$nowclk");
		if ($dispcomclk) {echo "<H2>Clock is: $clockn</H2><BR>";}
		$mytable = $clockn . "_CLK";
		$query="SELECT * FROM $mytable WHERE EVENT_NAME='Timetemp' ORDER BY START_TIME";
		if ($dispcomclk) {echo "<BR>Query = $query<BR>";}
		$result=mysql_query($query);
		while($r=mysql_fetch_array($result))
		{
			$elength=$r["LENGTH"];
			if ($dispcomclk) {echo "Event length: - $elength<BR>";}
			$thrs = $thrs + $elength;
		}
		if ($dispcomclk) {echo "Commercial time for Hour$myhour: - $thrs msecs <BR>";}
		$elsecs = ($thrs/1000);
		if ($dispcomclk) {echo "Commercial time for Hour$myhour: - $elsecs secs <BR>";}
		$elmins = ($elsecs/60);
		if ($dispcomclk) {echo "Commercial time for Hour$myhour: - $elmins mins <BR>";}
		$elhours = ($elmins/60);
		if ($dispcomclk) {echo "Commercial time for Hour$myhour: - $elhours hours <BR>";}
		$myhour++;
		$tday = ($tday + $thrs);
		$tweek = ($tweek + $thrs);
		$daymins = (($tday/1000)/60);
		$weekmins = (($tweek/1000)/60);
		$dayhours = ((($tday/1000)/60)/60);
		$weekhours = ((($tweek/1000)/60)/60);
		if ($dispcomclk) {echo "Commercial time for the day: - $daymins mins <BR>";}
		if ($dispcomclk) {echo "Commercial time for the day: - $dayhours hours <BR>";}
		if ($dispcomclk) {echo "Commercial time for the week: - $weekmins mins <BR>";}
		if ($dispcomclk) {echo "Commercial time for the week: - $weekhours hours <BR>";}
		if ($dispcomclk) {echo "<BR><HR><BR>";}
	}
	$thrs = 0;
	if (($myhour % 24) == 0)
	{
		$tday=0;
		if ($dispcomclk) {echo "<BR><HR><BR>";}
	}
}

$totweekminsc = ((($week)/1000)/60);
$totweekminst = ((($tweek)/1000)/60);
$totweekmins = ((($week+$tweek)/1000)/60);
$totweekhrsc = (((($week)/1000)/60)/60);
$totweekhrst = (((($tweek)/1000)/60)/60);
$totweekhrs = (((($week+$tweek)/1000)/60)/60);

if ($dispcomclk) {echo "<BR><HR><BR>";}
if ($dispcomclk) {echo "<H1>Total Mins for the week Commercial: $totweekminsc</H1><BR>";}
if ($dispcomclk) {echo "<H1>Total Mins for the week Time Sponsor: $totweekminst</H1><BR>";}
if ($dispcomclk) {echo "<H1>Total Mins for the week Commercial and Time Sponsor: $totweekmins</H1><BR>";}
if ($dispcomclk) {echo "<H1>Total Hours for the week Commercial: $totweekhrsc</H1><BR>";}
if ($dispcomclk) {echo "<H1>Total Hours for the week Time Sponsor: $totweekhrst</H1><BR>";}
if ($dispcomclk) {echo "<H1>Total Hours for the week Commercial and Time Sponsor: $totweekhrs</H1><BR>";}
if ($dispcomclk) {echo "<BR><HR><BR>";}
