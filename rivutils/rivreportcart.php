<?

// rivreportcart.php
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


$query="SELECT * FROM CART ORDER BY NUMBER";
$result=mysql_query($query);
while($r=mysql_fetch_array($result))
{
        // cart stuff
        $mycart1=$r["NUMBER"];
	$mycart = str_pad($mycart1, 6, "0", STR_PAD_LEFT);
	//echo "IN Event loop: mycart = $mycart <BR>";
	//echo $mycart;
	//echo "<BR>";
	$mylook = "/var/snd/".$mycart."_???.wav";
	//echo "Looking for $mylook <BR>";
	$myfound = searchForFile($mylook);
	//echo $myfound;
	//echo "<BR>";
	if ($myfound < 1)
		echo "****** Problem with CART $mycart <BR>";

}

