// when the site loads
$(document).ready(function () {
	$.get(
		"getfeed",
		{'n' : 32},
		(data) => data.forEach(review => $('.feed').append(generateReviewBox(review)))
	);
});
