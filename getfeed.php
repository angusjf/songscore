<?php

include "classes.php";

header('Content-Type: application/json');

$numberOfPosts = $_GET["n"] ?: 0;

echo json_encode($userAccount->getFeed($numberOfPosts));

?>
