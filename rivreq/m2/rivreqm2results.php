#!/usr/bin/php

<?php
# rivreqm2results.php
# I thought I had this working and then it went sideways
# this is dirty but may be working
# could stand improving

#$reqresults = file('/var/rivreq/m2/data/2025_07_15-19.txt');
$reqresults = file('/var/rivreq/m2/data/songrequests.txt');
# 2025_07_15-19.txt
#print_r($reqresults);


$newArray = array();
foreach ($reqresults as $reqresult) {
	$parts = explode("\t", trim($reqresult));
	#print_r(count($parts).PHP_EOL);
	if (count($parts) >= 3) {
		$songId = $parts[0];
		$songTitle = $parts[1];
		$songArtist = $parts[2];
	}
	$newArray[] = $songId;
	#print_r($songId.PHP_EOL);
}

#$resultArray = array_count_values($reqresults);
$resultArray = array_count_values($newArray);

#print_r($resultArray);

arsort($resultArray);
#sort($resultArray);

#print_r($resultArray);

#$first_value = reset($array); // First element's value
#$first_key = key($array); // First element's key

#print_r($resultArray);

$mysongreq = key($resultArray);

#print_r("mysongreq line: ", $mysongreq);


$re = '/^[0-9]+/m';

$str = $mysongreq;


$mymatch = preg_match($re, $mysongreq, $matches);


#$mycart = var_dump($matches[0]);

#print_r(PHP_EOL);
$mycart = $matches[0];
#print_r('here comes mycart... ');
print_r($mycart);

?>
