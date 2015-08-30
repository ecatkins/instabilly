$(document).ready(function() {
	
	$("#number_songs").val(10)
	
	$("#generate_button").on('click', function() {

		
		
		
		var number_songs = $("#number_songs").val()
		var follow = $('#follow').val()
		var recency_effect =$('#recency').val()
		var rating_effect = $('#rating').val()
		var duplicate_artist = $("#duplicateartist").val()
		var existing_playlist = $("#existingplaylist").val()
		var post_data = {"type":"engine","number_songs":number_songs, "follow":follow, "recency_effect":recency_effect,"rating_effect":rating_effect,"duplicate_artist":duplicate_artist, "existing_playlist": existing_playlist}
		
		$.post('playlist', post_data, function(data) {
			var uris = data['track_uris']
			var cover_art = data['cover_art']
			$("#engineplaylist_image").append('<img id="engineplaylist_image_image" src="'+ cover_art +'">')
			
			var iw = $('#playlist_player').width();
			$('#engineplaylist_image_image').css({'width':iw+'px'});
			$('#engineplaylist_image_image').css({'height':iw+'px'});
			$('#engineplaylist_image_image').css({'z-index':'1'});


			string = ""
			for (song in uris) {
				string += uris[song] + ','
			}
			string = string.substring(0, string.length - 1);
			$('#playlist_player').html('<iframe src="https://embed.spotify.com/?uri=spotify:trackset:PREFEREDTITLE:' + string + '" width="450" height="450" frameborder="0" allowtransparency="true"></iframe>')
			$('#playlist_player').css(({'z-index':'-1'}))

			
			 $('#engineplaylist_image_image').on('click', function() {
                $(this).fadeOut(2000)
                $("#playlist_player").css(({"border-color":"transparent",'z-index':'1'}));
              	   
            

              	$("#like").on("click", function() {
				$.post("rating", {"uris": uris, "decision": "like"}, function(data){
	
					console.log('liked')
				})
					})
				

				$("#dislike").on("click", function() {
						
						$.post("rating", {"uris": uris, "decision": "dislike"}, function(data){
							console.log('disliked')
						})
				})

				$("#save").on("click", function() {
						
						$.post("saveplaylist", {"uris": uris}, function(data){
							if (data['status'] === "success") {
								console.log("Success")

							}
						})
				})	


		   	})


// $("#playlist_player").append('<span id="like" class="glyphicon glyphicon-ok" aria-hidden="true"></span><span id="dislike" class="glyphicon glyphicon-remove" aria-hidden="true">')


			

					
		

		})
	})

	

	$('.fa-info').popover()



	// $(document).ajaxStart(function(){
 //        $('#playlist_player').append('<img src="/static/spotify/spiffygif.gif"/>')  
 //    });


    var pw = $('#playlist_player').width();
	$('#playlist_player').css({'height':pw+'px'});


	// With JQuery
	
	$('.engineslider').slider()

	$('.engineslider').slider({
		formatter: function(value) {
		return 'Current value: ' + value;
		}
	});
})

