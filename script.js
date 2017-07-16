// when the site loads
window.onload = function () {
	requestNewReviews(10);
}

// send a request from client to server
function requestNewReviews(numberOfReviews) {
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function () {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) appendNewReviews(xmlhttp.responseText);
	};
	xmlhttp.open("GET","getfeed.php?n=" + numberOfReviews, true);
	xmlhttp.send();
}

// called when the request responds
function appendNewReviews(responseText) {
	var reviewsDiv = document.getElementById("reviews");
	reviewsDiv.innerHTML += responseText;
}
