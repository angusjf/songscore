// when the site loads
$(document).ready(function () {
	var character_limit = 200;
	$('#character_count').html(character_limit + '/' + character_limit);

	$('#expansion-input').keyup(function() {
		var text_length = $('#expansion-input').val().length;
		var text_remaining = character_limit - text_length;

		$('#character_count').html(text_remaining + '/' + character_limit);
	});
});

$('#newReview').submit(function (e) {
	$.ajax({
		type: 'POST',
		url: '/submit',
		data: $(this).serialize(),
		success: function (data) {
			alert($(this).serialize());
		}
	});
	e.preventDefault();
});
