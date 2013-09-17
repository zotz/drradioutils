<?php

// rivlogs-form.php
// copyright 2013, drew Roberts
// Licensed under the GPL v2.

// this file will allow logs to be printed.

?>
<a href="index.html">Back To Start</a>
<HR>
<P>
<?php

include("rivdbinfo.inc.php");
include("rivopendb.php");


  $aLog = $_POST['rivlogPrint'];

  if(empty($aLog))
  {
    echo("You didn't select anything to export.");
  }
  else
  {
    $N = count($aLog);
    echo "In rivlogs-form";
 
    echo("You selected $N log(s): ");
    if($N>1)
    {
    	echo ("$N is greater than 1.");
    }
    else
    {
    	echo ("$N equals 1.");
	echo("... passed in log = $aLog[0]...");
	$getLog = $aLog[0] . "_LOG";
	echo("... getLog is $getLog ...");
	$query="SELECT * FROM $getLog";
	$result=mysql_query($query);
	if($result === FALSE) {
		echo " if we got here we are about to die on a bad result  ";
		die(mysql_error()); // TODO: better error handling
	}
	?>
	<table>
	<tr>
	<td><?php echo "ID"; ?></td>
	<td><?php echo "START TIME"; ?></td>
	<td><?php echo "CART NUMBER"; ?></td>
	<td><?php echo "TITLE"; ?></td>
	<td><?php echo "ARTIST"; ?></td>
	<td><?php echo "ALBUM"; ?></td>
	<td><?php echo "COUNT"; ?></td>
	<td><?php echo "TYPE"; ?></td>
	<td><?php echo "SOURCE"; ?></td>
	<td><?php echo "TIME TYPE"; ?></td>
	</tr>
	<?php
	while($r=mysql_fetch_array($result))
	{
		$mycart=$r["CART_NUMBER"];
		$query2="SELECT * FROM CART WHERE NUMBER=\"$mycart\"";
		$result2=mysql_query($query2);
		if($result2 === FALSE) {
			echo " if we got here we are about to die on a bad result2  ";
			die(mysql_error()); // TODO: better error handling
		}
		while($r2=mysql_fetch_array($result2))
		{
			$myartist=$r2["ARTIST"];
			$mytitle=$r2["TITLE"];
			$myalbum=$r2["ALBUM"];
		}
		?>
		<tr>
		<td><?php echo $r["ID"]; ?></td>
		<td><?php echo $r["START_TIME"]; ?></td>
        	<td><?php echo $r["CART_NUMBER"]; ?></td>
		<td><?php echo $mytitle; ?></td>
		<td><?php echo $myartist; ?></td>
		<td><?php echo $myalbum; ?></td>
		<td><?php echo $r["COUNT"]; ?></td>
		<td><?php echo $r["TYPE"]; ?></td>
		<td><?php echo $r["SOURCE"]; ?></td>
		<td><?php echo $r["TIME_TYPE"]; ?></td>
        	</tr>
		<?php
	}
	
    }

  }
?>
