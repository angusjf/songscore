<html>
	<head>
		<script src="script.js"></script>
		<link rel="stylesheet" type="text/css" href="stylesheet.css">
		<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
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
				<form>
					<div>
						WRITE A REVIEW
					</div>
					<div>
						<input type="text" placeholder="Song name...">
						<input type="button" value="*">
						<input type="button" value="*">
						<input type="button" value="*">
						<input type="button" value="*">
						<input type="button" value="*">
					</div>
					<div>
						<input type="text" placeholder="why did you give this rating? (optional)">
						<input type="submit">
					</div>
				</form>
			</div>
			<div class="section shadow-1">
				<div id="reviews">
					<!-- use script.js to add to this -->
				</div>
			</div>
		</div>
	</body>
</html>
