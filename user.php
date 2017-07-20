<?php
include "classes.php";

$username = isset($_GET["name"]) ? $_GET["name"] : 0;

$user = Account::getByUsername($username);
?>
