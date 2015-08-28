$(document).ready(function() {
	
	$("#number_songs").val(10)
	
	$("#generate_button").on('click', function() {

		
		
		var number_songs = $("#number_songs").val()
		var follow = $('#follow').attr('data-slider')
		var recency_effect =$('#recency').attr('data-slider')
		var rating_effect = $('#rating').attr('data-slider')
		var duplicate_artist = $("#duplicateartist").attr('data-slider')
		var existing_playlist = $("#existingplaylist").attr('data-slider')
		var post_data = {"type":"engine","number_songs":number_songs, "follow":follow, "recency_effect":recency_effect,"rating_effect":rating_effect,"duplicate_artist":duplicate_artist, "existing_playlist": existing_playlist}
		

		$.post('playlist', post_data, function(data) {
			var uris = data['track_uris']
			var cover_art = data['cover_art']
			$("#engineplaylist_image").append('<img id="engineplaylist_image_image" src="'+ cover_art +'">')
			
			var iw = $('#playlist_player').width();
			$('#engineplaylist_image_image').css({'width':iw+'px'});
			$('#engineplaylist_image_image').css({'height':iw+'px'});
			$('#engineplaylist_image_image').css({'z-index':'1'});



			// $("#engineplaylist_image").css('background-image',cover_art)
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
              	 $("#playlist_player").append('<span id="like" class="glyphicon glyphicon-ok" aria-hidden="true"></span><span id="dislike" class="glyphicon glyphicon-remove" aria-hidden="true">')  
            })



			// <span id="like" class="glyphicon glyphicon-ok" aria-hidden="true"></span><span id="dislike" class="glyphicon glyphicon-remove" aria-hidden="true">

			$("#like").on("click", function() {
				$.post("rating", {"uris": uris, "decision": "like"}, function(data){
			
					console.log('hello')
				})
			})
			$("#dislike").on("click", function() {
				$.post("rating", {"uris": uris, "decision": "dislike"}, function(data){
					console.log('hello')
				})
			})			
		})
	})

	

	$('.fa-info').popover()


	$(document).foundation();
	$(document).foundation('slider', 'reflow');
	// $('#playlist_player').append('<img src="/static/spotify/spiffygif.png"/>') 

	$(document).ajaxStart(function(){
        $('#playlist_player').append('<img src="/static/spotify/spiffygif.gif"/>')  
    });


    var pw = $('#playlist_player').width();
	$('#playlist_player').css({'height':pw+'px'});


    // $(document).ajaxComplete(function(){
    //     $("#playlist_player").empty();
})

