<?php

include "classes.php";

$numberOfPosts = $_GET["n"];

foreach ($userAccount->getFeed($numberOfPosts) as $review) {
	echo $review->toHtml();
}

?>
