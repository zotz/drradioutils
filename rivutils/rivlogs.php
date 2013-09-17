<?php

// rivlogs.php
// copyright 2013, drew Roberts
// Licensed under the GPL v2.

// this file will allow logs to be chosen for printing

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


$query="SELECT * FROM LOGS ORDER BY NAME ASC LIMIT $start_from, 20";
$result=mysql_query($query);


?>
<form action="rivlogs-form.php" method="post">
<table>
<tr><td>Print?</td><td>Log Name</td><td>Service</td><td>Description</td><td>Exists</td></tr>
<?php

$mylog="None";
//<input type="checkbox" name="rivlogPrint[]" value=$boxi />
$boxi=1;
while($r=mysql_fetch_array($result))
{
	$mylog=$r["NAME"];
	//echo $mylog;
	$query2="SELECT * FROM LOGS WHERE NUMBER=$mylog ";
	$result2=mysql_query($query2);
	while($r2=mysql_fetch_array($result2))
	{
		$mylog=$r2["NAME"];
		//echo $mylog;
	}
	?>
	<tr>
	<td><input type="checkbox" name="rivlogPrint[]" value=<?php echo $r["NAME"]; ?> /></td>
	<td><?php echo $r["NAME"]; ?></td>

        <td><?php echo $r["SERVICE"]; ?></td>
	<td><?php echo $r["DESCRIPTION"]; ?></td>
	<td><?php echo $r["EXISTS"]; ?></td>
        </tr>
<?php
$boxi=$boxi+1;
};
?>
</table>
<input type="submit" name="formSubmit" value="Submit" />
 
</form>

<?php
$sql = "SELECT COUNT(NAME) FROM LOGS";
$rs_result = mysql_query($sql);
//echo $rs_result;
$row = mysql_fetch_row($rs_result);
$total_records = $row[0];
$total_pages = ceil($total_records / 20);
  
for ($i=1; $i<=$total_pages; $i++) {
            echo "<a href='rivlogs.php?page=".$i."'>".$i."</a> ";
};
?>
