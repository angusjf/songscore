function generateReviewBox(review) {
	return `
	<div class='review section shadow-1'>
		<div class="section-content review-content">
			<div class='subject-group'>
				<div class="subjectPictureDiv">
					<img class='subjectPicture' src='${review.subject.image}'>
				</div>
				<div class='subjectName'>${review.subject.name}</div>
				<div class='subjectName'>${review.subject.artist_name}</div>
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
}
