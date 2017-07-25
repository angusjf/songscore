// when the site loads
$(document).ready(function () {
	requestNewReviews(32); // get 32 new reviews as JSON

	var newReviewSubjectBox = document.getElementById("#"); // form textbox
	var newReviewSubjectDropdown = document.getElementById("#");
	newReviewSongBox.onchange = function () {
		if (newReviewSongBox.value.length > 0) {
			newReviewSubjectDropdown.visible = true;
			var resultsJson = getResultsJson(newReviewSongBox.value);
			resultsJson.results.trackmatches.track.forEach(
				function (track) {
					//newReviewSubjectDropdown.
				}
			);
		} else {
			newReviewSubjectDropdown.visible = false;
		}
	};
});

// send a request from client to server
function requestNewReviews(numberOfReviews) {
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function () {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) appendNewReviews(JSON.parse(xmlhttp.responseText));
	};
	xmlhttp.open("GET","getfeed.php?n=" + numberOfReviews, true);
	xmlhttp.send();
}

// called when the request responds
function appendNewReviews(responseJSON) {
	var reviewsDiv = document.getElementById("reviews");
	var html = '';
	responseJSON.forEach(function (review) {
		html += `
			<div class='review'>
				<img class='userPicture' src='${review.user.image}'>
				<div class='Name'>${review.user.name}</div>
				<div class='userName'><a href='/user.php?username=${review.user.username}'>${review.user.username}</a></div>
				<img class='subjectPicture' src='${review.subject.image}'>
				<div class='subjectName'>${review.subject.name}</div>
				<div class='subjectName'>${review.subject.artist}</div>
				<div class='rating'>${review.rating}</div>
				<div class='text'>${review.text}</div>
				<div class='date'>${review.date}</div>
			</div>
		`;
	});
	reviewsDiv.innerHTML += html;
}

function submitNewReview(song, rating, text) {
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function () {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) appendNewReviews(JSON.parse(xmlhttp.responseText));
	};
	xmlhttp.open("POST","submit.php", true);
	xmlhttp.send("?song=" + song + "&rating=" + rating + "&text=" + text);
}

function getResultsJson(text) {
	return JSON.Parse("{}");
}
