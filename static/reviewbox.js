// when the site loads
$(document).ready(function () {
	var character_limit = 200;
	$('#character_count').html(character_limit + '/' + character_limit);

	$('#expansion-input').keyup(function() {
		var text_length = $('#expansion-input').val().length;
		var text_remaining = character_limit - text_length;

		$('#character_count').html(text_remaining + '/' + character_limit);
	});

	$('#subject-input').keyup(function() {
		if ($('#expansion-input').val().length > 0) {
			$.get(
				"http://ws.audioscrobbler.com/2.0/",
				{
					'method' : "track.search",
					'album' : query,
					'api_key' : "b392916683d0336a30882ff34ff114f7",
					'format' : "json",
					'limit' : 5
				},
				data => {
					/*
					data.results.albummatches.album.forEach(album => {
                        results.innerHTML += `
                                <div>
                                        <img src='${album.image[0]["#text"]}'/>
                                        <span style="display: inline-block;">
                                                <div>${album.name}</div>
                                                <div>${album.artist}</div>
										*/
					// $('#subject-search').add( new html lelements)
				}
			);
		} else {
			// $('#subject-search').html(); . hide() ?
		}
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
