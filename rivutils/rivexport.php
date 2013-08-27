<?php

// rivexport.php
// copyright 2013, drew Roberts
// Licensed under the GPL v2.

// this file will allow files to be exported and compressed with metadata included from database

function searchForFile($fileToSearchFor){
	$numberOfFiles = count(glob($fileToSearchFor));
	if($numberOfFiles == 0){ return(FALSE); } else { return(TRUE);}
}

?>
<a href="index.html">Back To Start</a>
<HR>
<P>
<?php

include("rivdbinfo.inc.php");
include("rivopendb.php");

if (isset($_GET["page"])) { $page  = $_GET["page"]; } else { $page=1; };
//$page=1;
//echo $page;
$start_from = ($page-1) * 20;


$query="SELECT * FROM CUTS ORDER BY CUT_NAME ASC LIMIT $start_from, 20";
$result=mysql_query($query);


?>
<form action="rivexport-form.php" method="post">
<table>
<tr><td>Export?</td><td>Cut Name</td><td>Cart Number</td><td>Artist</td><td>Song Title</td></tr>
<?php

$myartist="None";
//<input type="checkbox" name="rivExport[]" value=$boxi />
$boxi=1;
while($r=mysql_fetch_array($result))
{
	$mycart=$r["CART_NUMBER"];
	echo $mycart;
	$query2="SELECT * FROM CART WHERE NUMBER=$mycart ";
	$result2=mysql_query($query2);
	while($r2=mysql_fetch_array($result2))
	{
		$myartist=$r2["ARTIST"];
		//echo $myartist;
	}
	?>
	<tr>
	<td><input type="checkbox" name="rivExport[]" value=<?php echo $r["CUT_NAME"]; ?> /></td>
        <td><?php echo $r["CUT_NAME"]; ?></td>
        <td><?php echo $r["CART_NUMBER"]; ?></td>
	<td><?php echo $myartist; ?></td>
	<td><?php echo $r["DESCRIPTION"]; ?></td>
        </tr>
<?php
$boxi=$boxi+1;
};
?>
</table>
<input type="submit" name="formSubmit" value="Submit" />
 
</form>

<?php
$sql = "SELECT COUNT(CUT_NAME) FROM CUTS";
$rs_result = mysql_query($sql);
//echo $rs_result;
$row = mysql_fetch_row($rs_result);
$total_records = $row[0];
$total_pages = ceil($total_records / 20);
  
for ($i=1; $i<=$total_pages; $i++) {
            echo "<a href='rivexport.php?page=".$i."'>".$i."</a> ";
};
?>
