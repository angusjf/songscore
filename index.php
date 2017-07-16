<html>
	<head>
		<script src="script.css"></script>
		<link rel="stylesheet" type="text/css" href="stylesheet.css">
		<title>SongScore</title>
		<?php include "classes.php" ?>
	</head>
	<body>
		<div id="container">
			<div class="section header">
				<h1>SongScore</h1>
			</div>
			<div class="section">
				<form>
					<input type="submit">
				</form>
			</div>
			<div class="section">
				<div id="reviews">
					<?php
					foreach ($userAccount->getFeed(5) as $review) {
						echo $review->toHtml();
					}
					?>
				</div>
			</div>
		</div>
	</body>
</html>
