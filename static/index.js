// when the site loads
$(document).ready(function () {
	$.get("getfeed", {'n' : 32}, (data) => appendNewReviews(JSON.parse(data)));
});

// called when the request responds
function appendNewReviews(responseJSON) {
	var feed = document.getElementById("feed");
	var html = '';
	console.log(responseJSON);
	responseJSON.forEach(function (review) {
		html += `
			<div class='review section shadow-1'>
				<div class="section-content review-content">
					<div class='subject-group'>
						<div class="subjectPictureDiv">
							<img class='subjectPicture' src='${getAlbumArt(review.subject_name)}'>
						</div>
						<div class='subjectName'>${review.subject_name}</div>
						<div class='subjectName'>${getArtistName(review.subject_name)}</div>
					</div>

					<div class="review-right">
						<div class="top-group">
							<a href='/user/${review.user.username}'><div class='Name'>${review.user.name}</div>
							<img class='userPicture' src='${review.user.image}'>
							<div class='userName'>${review.user.username}</div></a>
							<div class='rating'>${review.rating}</div>
						</div>
						<div class="text-group"
						<div class='text'>${review.text}</div>
						<div class='date'>${review.date}</div>
					</div>
				</div>
			</div>
		`;
	});
	feed.innerHTML += html;
}

function getAlbumArt(subject_name) {
	return "static/images/subject.png"
}

function getArtistName(subject_name) {
	return "ARTIST_NAME"
}
