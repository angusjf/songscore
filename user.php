<?php
include "classes.php";

$username = $_GET["username"];

$user = Account::getByUsername($username);
?>
<html>
	<head>
		<script src="script.js"></script>
		<link rel="stylesheet" type="text/css" href="stylesheet.css">
		<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
		<link rel='stylesheet' type='text/css' href='https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,300'>
		<title>SongScore</title>
		<meta name="viewport" content="width=device-width, initial-scale=1, minimal-ui">
	</head>
	<body>
		<nav class="navBar shadow-1">
			<nav class="nav-wrapper">
				<input type="checkbox" id="menu-toggle">
				</input>
				<ul>
					<li><a href="#"><i class="material-icons">home</i></a></li>
					<li><a href="#"><i class="material-icons">notifications</i></a></li>
				</ul>
				<img class="logo" src="logo.png"></img>
				<img class="logo circle" src="user-avatar.png"></img>
				<label for="menu-toggle" class="label-toggle"></label>
			</nav>
		</nav>

		<div id="container">
			<div class="section shadow-1">
				<img class='userPicture' src='<?php echo $user->image; ?>'>
				<h1><?php echo $user->name; ?></h1>
				<h2><?php echo $user->username; ?></h2>
			</div>
		</div>
	</body>
</html>
