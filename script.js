// when the site loads
window.onload = function () {
	requestNewReviews(10);
}

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
	var html = `
		<div class='review'>
			<img class='userPicture' src='${responseJSON.user.image}'>
			<div class='userName'>${responseJSON.user.name}</div>
			<img class='subjectPicture' src='${responseJSON.subject.image}'>
			<div class='subjectName'>${responseJSON.subject.name}</div>
			<div class='rating'>${responseJSON.rating}</div>
			<div class='text'>${responseJSON.text}</div>
		</div>
	`;
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
