<?php
// This is twoopendb.php
// it incorporates rivopen and also will open ajax01
// eventually move rivque table to rivquedatabas



//$rivconn = mysql_connect($dbhost,$rivusername,$rivpassword) or die ('Error connecting to mysql');
//@mysql_select_db($rivdatabase, $rivconn) or die ( "Unable to select database");
//$rivqueconn = mysql_connect($dbhost,$rivusername,$rivpassword) or die ('Error connecting to mysql');
//@mysql_select_db($rivquedatabase, $rivqueconn) or die ( "Unable to select database");
$rivconn = mysql_connect($dbhost,$rivusername,$rivpassword) or die ('Error connecting to mysql');
mysql_select_db($rivdatabase, $rivconn) or die ( "Unable to select rivdatabase");
$rivqueconn = mysql_connect($dbhost,$rivusername,$rivpassword, true) or die ('Error connecting to mysql');
mysql_select_db($rivquedatabase, $rivqueconn) or die ( "Unable to select rivquedatabase");
?>
