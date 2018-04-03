results = {
	"albums" : [],
	"songs" : []
}

// when the site loads
$(document).ready(function () {
	var character_limit = 200;
	$('#character_count').html(character_limit + '/' + character_limit);

	$('#expansion-input').keyup(function() {
		var text_length = $('#expansion-input').val().length;
		var text_remaining = character_limit - text_length;

		$('#character_count').html(text_remaining + '/' + character_limit);
	});

	$('#subject-input').keyup(search);
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

function updateResultsBoxContents() {
	// never show results box if no text in search
	if ($('#subject-input').val().length == 0) {
		$('#subject-results').hide();
	} else {
		$('#subjects-results').show();
		results.albums.forEach((album) => {
			$('#subject-results').append(`
				<div>
					<img src='${album.image}'/>
					<span style="display: inline-block;">
						<div>${album.name}</div>
						<div>${album.artist_name}</div>
					</span>
				</div>
			`);
		});
		results.songs.forEach((song) => {
			$('#subject-results').append(`
				<div>
					<img src='${song.image}'/>
					<span style="display: inline-block;">
						<div>${song.name}</div>
						<div>${song.artist_name}</div>
					</span>
				</div>
			`);
		});
	}
}

/*
 * updates the 'results' object with data from last fm,
 * based on the content of a text box with id '#subject-input',
 * and calls updateResultsBoxContents() when the results change
 */
function search () {
	var query = $('#subject-input').val();
	if ($('#subject-input').val().length > 0) {
		jQuery.get(
			"http://ws.audioscrobbler.com/2.0/",
			{
				'method' : "track.search",
				'track' : query,
				'api_key' : "b392916683d0336a30882ff34ff114f7",
				'format' : "json",
				'limit' : 3
			},
			data => {
				results.songs = [];
				data.results.trackmatches.track.forEach(track => {
					results.songs.push({
                        "name" : track.name,
                        "artist_name" : track.artist,
                        "image" : track.image[2]["#text"]
					});
				});
				updateResultsBoxContents();
			}
		);
		jQuery.get(
			"http://ws.audioscrobbler.com/2.0/",
			{
				'method' : "album.search",
				'album' : query,
				'api_key' : "b392916683d0336a30882ff34ff114f7",
				'format' : "json",
				'limit' : 3
			},
			data => {
				results.albums = [];
				data.results.albummatches.album.forEach(album => {
					results.albums.push({
                        "name" : album.name,
                        "artist_name" : album.artist,
                        "image" : album.image[3]["#text"]
					});
				});
				updateResultsBoxContents();
			}
		);
	}
}
