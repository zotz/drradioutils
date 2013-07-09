<?

// rivreportcut.php
// copyright 2013, drew Roberts
// Licensed under the GPL v2.

// this file will pull the data from rivendell needed to calculate the time allocated
// to the various events in the
// rivendell grids/clocks/events data

function searchForFile($fileToSearchFor){
	$numberOfFiles = count(glob($fileToSearchFor));
	if($numberOfFiles == 0){ return(FALSE); } else { return(TRUE);}
}

?>
<a href="index.html">Back To Start</a>
<HR>
<P>
<?

include("rivdbinfo.inc.php");
include("rivopendb.php");


$query="SELECT * FROM CUTS ORDER BY CUT_NAME";
$result=mysql_query($query);
while($r=mysql_fetch_array($result))
{
        // cut stuff
        $mycut1=$r["CUT_NAME"];
	$mycut = str_pad($mycut1, 10, "0", STR_PAD_LEFT);
	//echo "IN Event loop: mycut = $mycut <BR>";
	//echo $mycut;
	//echo "<BR>";
	$mylook = "/var/snd/".$mycut.".wav";
	//echo "Looking for $mylook <BR>";
	$myfound = searchForFile($mylook);
	//echo $myfound;
	//echo "<BR>";
	if ($myfound < 1)
		echo "****** Problem with CUT $mycut <BR>";

}

