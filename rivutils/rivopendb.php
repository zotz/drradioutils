<?php
// This is rivopendb.php



$rivconn = mysql_connect($dbhost,$rivusername,$rivpassword) or die ('Error connecting to mysql');
@mysql_select_db($rivdatabase) or die ( "Unable to select database");
?>
