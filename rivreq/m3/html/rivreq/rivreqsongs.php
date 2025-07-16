<!DOCTYPE html>
<html>
<body>

	<?php

		$lines = file('chosensongs.txt');
		$vote_file = 'songrequests.txt'; // your text file

	if(isset($_POST["songreq"])) { 
		$ip = $_SERVER['REMOTE_ADDR'];
		$can_vote = true;
		#$cookie_name = 'voted_this_hour';
		$current_hour = date('Y-m-d H');
		$user_req = test_input($_POST["songreq"]);


		// Check the cookie first
		#if (isset($_COOKIE[$cookie_name])) {
		#	echo "You have already voted this hour!\n";
		#	exit;
		#}

		list($xid, $xtitle, $xartist) = explode("\t", $user_req);
		// Read the vote file
		$vlines = file($vote_file, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);

		foreach ($vlines as $vline) {
			list($id, $vtitle, $vartist, $timestamp, $vote_ip) = explode("\t", $vline);
			$vote_hour = date('Y-m-d H', strtotime($timestamp));

			if ($vote_ip == $ip && $vote_hour == $current_hour) {
				echo "this is where can vote goes false.\n";
				#$can_vote = false;
				#break;
			}
		}

		if ($can_vote) {
			$timestamp = date('Y-m-d H:i:s');
			#$entry = "$user_req\t$timestamp\t$ip\n";
			$entry = "$xid\t$xtitle\t$xartist\t$timestamp\t$ip";
			$myfile = file_put_contents($vote_file, $entry.PHP_EOL , FILE_APPEND);
			
			// Set cookie to block further votes
			#setcookie($cookie_name, '1', time() + 3600); // expires in 1 hour
			echo "Vote recorded.\n";
			echo "HEY! You have chosen song: $xtitle by $xartist\n";
			#echo "Broken down: $xid, $xtitle, $xartist\n";
		} else {
		    echo "You can only vote once per hour.\n";
		}
	 	#$mytime = time();
	 	#$txt = "$user_req\t$mytime";
	 	#$txt = $user_req;
	 	#$myfile = file_put_contents('songrequests.txt', $txt.PHP_EOL , FILE_APPEND | LOCK_EX);
	 	chmod("songrequests.txt", 0666);

		#echo "HEY! You have chosen song $user_req";
    } else {
	?>
	<a href="./songrequests.txt">Votes so far this hour.</a>
	<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
	  <br>  
	  <p>Please select your song request and click submit:</p>

	<?php

	$myloopindex = 0;
	foreach ($lines as $x) {
		#echo "$x <br>";
		#echo "$x";
		echo "<input type='radio' id='sr<?$myloopindex?>' name='songreq' value='$x'/>";
		echo "<label for='sr$myloopindex'> $x </label><br>";

	}


	?>

	<br>

	  <input type="submit" value="Submit">

	</form>
	<?php
	    }

function test_input($data) {
	$data = trim($data);
	$data = stripslashes($data);
	$data = htmlspecialchars($data);
	return $data;
}
    ?>
</body>
</html>
