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
				<div class="section-content">
					<h2 class="capital">Write a review</h2>
					<form>
						<div class="form-group">
							<input class="text-input" placeholder="Type what song/album you're reviewing..." type="text" required>
							<span class="highlight"></span>
							<span class="bar"></span>
						</div>
						<div class="form-group">
							<input class="text-input" placeholder="Expand on your review with up to 200 characters..." type="text" required>
							<span class="highlight"></span>
							<span class="bar"></span>
						</div>
						<input type="submit">
					</form>
				</div>
			</div>
			<div class="section shadow-1">
				<div id="reviews" class="section-content">
					<!-- use script.js to add to this -->
				</div>
			</div>
		</div>
	</body>
</html>
