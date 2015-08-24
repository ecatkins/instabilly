$(document).ready(function() {
	
	$("#number_songs").val(10)
	

	$("#neighbors").val(3)
	$("#recency").val(10)
	$("#rating").val(5)
	$("#duplicateartist").val(0)
	$("#existingplaylist").val(0)


	$("#generate_button").on('click', function() {
	
		var number_songs = $("#number_songs").val()
		var neighbors = $('#neighbors').attr('data-slider')
		var recency_effect =$('#recency').attr('data-slider')
		var rating_effect = $('#rating').attr('data-slider')
		var duplicate_artist = $("#duplicateartist").attr('data-slider')
		var existing_playlist = $("#existingplaylist").attr('data-slider')
		var post_data = {"number_songs":number_songs, "neighbors":neighbors, "recency_effect":recency_effect,"rating_effect":rating_effect,"duplicate_artist":duplicate_artist, "existing_playlist": existing_playlist}
		console.log(post_data)

		$.post('playlist', post_data, function(data) {
			console.log(data['track_uris'])
			var uris = data['track_uris']
			string = ""
			for (song in uris) {
				string += uris[song] + ','
			}
			string = string.substring(0, string.length - 1);
			console.log(string)
			

			$('#playlist_player').append('<iframe src="https://embed.spotify.com/?uri=spotify:trackset:PREFEREDTITLE:' + string + '" width="300" height="380" frameborder="0" allowtransparency="true"></iframe>')

			

		})

	})

	

	$('.fa-question').popover()

	$(document).foundation();
	$(document).foundation('slider', 'reflow');
})

