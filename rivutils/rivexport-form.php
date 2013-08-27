<?php

// rivexport-form.php
// copyright 2013, drew Roberts
// Licensed under the GPL v2.

// this file will allow files to be exported and compressed with metadata included from database

?>
<a href="index.html">Back To Start</a>
<HR>
<P>
<?php

include("rivdbinfo.inc.php");
include("rivopendb.php");


  $aCut = $_POST['rivExport'];
  if(empty($aCut))
  {
    echo("You didn't select anything to export.");
  }
  else
  {
    $N = count($aCut);
    echo "In rivexport-form";
 
    echo("You selected $N cut(s): ");
    for($i=0; $i < $N; $i++)
    {
      echo($aCut[$i] . " ");
      $mycut=$aCut[$i];
      echo " mycut is $mycut ";
      $query="SELECT * FROM CUTS WHERE CUT_NAME=\"$mycut\"";
      $result=mysql_query($query);
      echo "just did the query for result";
      if($result === FALSE) {
      		echo " if we got here we are about to die on a bad result  ";
    		die(mysql_error()); // TODO: better error handling
      }
      echo " query is $query - got a good result...  ";
      //echo "result is $result";
      while($r=mysql_fetch_array($result))
      {
      		$mycart=$r["CART_NUMBER"];
		echo "mycart is $mycart";
		$query2="SELECT * FROM CART WHERE NUMBER=\"$mycart\"";
		echo "query2 is $query2";
		$result2=mysql_query($query2);
		if($result2 === FALSE) {
			echo " if we got here we are about to die on a bad result2  ";
    			die(mysql_error()); // TODO: better error handling
		}
		echo " query2 is $query2 - got a good result2...  ";
		while($r2=mysql_fetch_array($result2))
		{
			$myartist=$r2["ARTIST"];
			$mytitle=$r2["TITLE"];
			$myalbum=$r2["ALBUM"];
			//echo "myartist is $myartist";
		}
	}
      
      echo " - myartist is $myartist - ";
      echo " - mytitle is $mytitle - ";
      echo " - myalbum is $myalbum - ";
      $copyfrom="../../snd/$aCut[$i].wav";
      $copyto="../../sndexport/$aCut[$i].wav";
      $compresstoso="../../sndexport/$myartist-$myalbum-$mytitle.mp3";
      $compressto="../../sndexport/$aCut[$i].mp3";
      
      echo " copyfrom is $copyfrom ";
      echo " copyto is $copyto ";
      echo " Compress to is $compressto ";
      echo " Compresstoso is $compresstoso ";
      $output = shell_exec("cp $copyfrom $copyto");
      echo "<pre>$output</pre>";
      $output = shell_exec("lame $copyto \"$compresstoso\"");
      echo "<pre>$output</pre>";
      $output = shell_exec("/usr/bin/id3v2 --artist \"$myartist\" --album \"$myalbum\" --song \"$mytitle\" \"$compresstoso\"");
      echo "<pre>$output</pre>";
    }
  }
?>
