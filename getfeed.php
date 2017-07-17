<?php

include "classes.php";

header('Content-Type: application/json');

$numberOfPosts = $_GET["n"];

foreach ($userAccount->getFeed($numberOfPosts) as $review) {
	echo $review->toJson();
}

?>
