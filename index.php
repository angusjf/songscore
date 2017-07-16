<html>
	<head>
		<script src="script.css"></script>
		<link rel="stylesheet" type="text/css" href="stylesheet.css">
		<title>WhatMonitorShouldI[Get/Buy]????</title>
		<?php include "classes.php" ?>
	</head>
	<body>
		<div id="container">
			<div class="section header">
				<h1>WhatMonitorShouldI[Get/Buy]????</h1>
			</div>
			<div class="section">
				<form>
					<select name="brand">
							<option value="dell">Dell</option>
					</select>
					<input type="submit">
				</form>
			</div>
			<div class="section">
				<div id="results">
					<?php foreach (Monitor::getAll() as $monitor) { ?>
						<div class="monitor">
							<img class="monitorImage" src="<?php echo $monitor->image; ?>">
							<div class="monitorName"><?php echo $monitor->name; ?></div>
							<div class="monitorPrice"><?php echo "$" . $monitor->price; ?></div>
						</div>
					<?php } ?>
				</div>
			</div>
			<div class="section footer">
				<p>whatever</p>
			</div>
		</div>
	</body>
</html>
