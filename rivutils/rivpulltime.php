<?

// this file will pull the data needed to populate the trafficgenny timeslots table
// from the rivendell grids/clocks/events data and for the tempspnsrtimeslots table

// for this to work properly, you need events in rivendell rdlogmanager called "Commercial" and "Timetemp"
// you can leave "Timetemp" out of the mix if you do not want to use that functionality

?>
<a href="index.html">Back To Start</a>
<HR>
<P>
<?


include("dbinfo.inc.php");
include("opendb.php");

$dispcomclk = 0;			//	display commercial clock info
$disptatclk = 0;			//	display timetemp clock info

//	you can pull commercial timeslots and timespnsr timeslots from rivendell and update the trafficgenny tables with them
//	set $pullcommriv $pulltimeriv and $updatetg all to 1 to do this.
//	if you set $pullcommriv and $pulltimeriv  to 1 but set $updatetg to 0 
//	and set $showtginsert to 1 then it will show you the insert statements but not execure them.

$pullcommriv = 1;			//	pull commercial timeslots from rivendell?
$pulltimeriv = 1;			//	pull timespnsr timeslots from rivendell?
$updatetg = 1;				//	update the trafficgenny tables or just print? 1 = update
$showtginsert = 1;			//	show trafficgenny insert statements

$query0="TRUNCATE timeslots";
if ($updatetg & $pullcommriv) {$result=mysql_query($query0);}

include("rivdbinfo.inc.php");
include("rivopendb.php");

$offset=$_POST['offset'];
$tdate=$_POST['tdate'];
// $tdate='2007-10-06';


$mn=substr($tdate,5,2);
$dy=substr($tdate,8,2);
$yr=substr($tdate,0,4);

$dow = date("l", mktime(0, 0, 0, $mn, $dy, $yr));


// ok monday adjust = 0, tuesday adjust = 24, etc.


if ($dow=='Monday')
{
	$clkadj='0';
}

if ($dow=='Tuesday')
{
	$clkadj='24';
}

if ($dow=='Wednesday')
{
	$clkadj='48';
}

if ($dow=='Thursday')
{
	$clkadj='72';
}

if ($dow=='Friday')
{
	$clkadj='96';
}

if ($dow=='Saturday')
{
	$clkadj='120';
}

if ($dow=='Sunday')
{
	$clkadj='144';
}

// echo "Clock Adjust = $clkadj";

// ok outer loop


$myhour = 0;

$mytype = 0;			// 0 = 'Commercial' || 1 = 'Timetemp'
$evn = 'Commercial';		// before going in
if ($pullcommriv == 0)
{
	$mytype = 1;
	$evn = 'Timetemp';
	echo " dont pull commercials from Rivendell <BR> ";
}
if ($pulltimeriv == 0 & $pullcommriv == 0)
{
	$mytype = 2;
	echo " dont pull time sponsors from Rivendell <BR> ";
}
while ($mytype <= 1)
{
	// echo "mytype = $mytype || evn = $evn <BR>";
	while($myhour <= 23)
	{
		// echo "myhour = $myhour <BR>";
		$clkabs = $myhour + $clkadj;
		$nowclk = 'CLOCK' . $clkabs;
		
		// echo "clockabs = $clkabs || nowclock = $nowclk <BR>";
		$query1="SELECT $nowclk FROM SERVICES WHERE NAME='Production'";
		if ($dispcomclk) {echo "<BR>Query1 = $query1<BR>";}
		$result1=mysql_query($query1) or die(mysql_error());
		if ($dispcomclk) {echo "<H1>$dow Clock $clkabs test : $myhour </H1>";}
		$clockn=mysql_result($result1, 0,"$nowclk");
		if ($dispcomclk) {echo "clockn = $clockn <BR>";}
		$mytable = $clockn . "_CLK";
		// echo "mytable = $mytable <BR> ";
		$query2="SELECT * FROM $mytable WHERE EVENT_NAME='$evn' ORDER BY START_TIME";
		if ($dispcomclk) {echo "<BR>Query2 = $query2<BR>";}
		$result2=mysql_query($query2);
		while($r1=mysql_fetch_array($result2))
		{
			$myhradj = substr(('0' . $myhour), -2);
			$START_TIME=substr_replace($r1["START_TIME"],$myhradj,0,2);
			if ($dispcomclk) {echo "Start Time: - $START_TIME";}
			include("opendb.php");
			if ($mytype == 0)
			{
				$query3 = "INSERT INTO timeslots VALUES (NULL,'0','0','$START_TIME')";
			}
			if ($mytype == 1)
			{
				$query3 = "INSERT INTO tempspnsrtimeslots VALUES (NULL,'0','0','$START_TIME')";
			}
			if ($showtginsert) {echo "<BR> $query3 <BR>";}
			if ($updatetg) {mysql_query($query3);}
			if ($dispcomclk) {echo "<br>";}
			include("rivopendb.php");
		}
		$myhour++;
	}
	$mytype++;
	$evn = 'Timetemp';
	$myhour=0;
	if ($pulltimeriv == 0)
	{
		$mytype = 2;
		echo " dont pull time sponsors from Rivendell <BR> ";
	}
	$query0="TRUNCATE tempspnsrtimeslots";
	if ($updatetg & $pulltimeriv) {$result=mysql_query($query0);}
}

include("rivclosedb.php");

//-------------------- below is from select1.php -----------------------------

echo "<BR><HR><BR>";

include("select2.php");

include("closedb.php");
?>
