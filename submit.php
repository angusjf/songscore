<?php
	include "classes.php";

	$subjectMBID = $_POST["subjectMBID"];
	$userId = $_POST["userId"];
	$rating = $_POST["rating"];
	$text = $_POST["text"];

	if (isset($subjectMBID) && isset($userId) && isset($rating) && isset($text)) {
		Review::addToDatabase($subjectMBID, $userId, $rating, $text);
	} else {
		echo "yo like post some data";
	}
?>
