$(document).ready(function() {
	$("#number_songs").val(10)
	$("#neighbors").val(3)
	$("#recency").val(10)
	$("#rating").val(5)
	$("#duplicateartist").val(0)
	$("#existingplaylist").val(0)


	$("#generate_button").on('click', function() {
		var number_songs = $("#number_songs").val()
		var neighbors = $("#neighbors").val()
		var recency_effect = $("#recency").val()
		var rating_effect = $("#rating").val()
		var duplicate_artist = $("#duplicateartist").val()
		var existing_playlist = $("#existingplaylist").val()

		var post_data = {"number_songs":number_songs, "neighbors":neighbors, "recency_effect":recency_effect,"rating_effect":rating_effect,"duplicate_artist":duplicate_artist, "existing_playlist": existing_playlist}

		$.post('playlist', post_data, function(data) {
			console.log("anything")

		})

	})



	$('.fa-question').popover()
})

