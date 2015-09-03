$(document).ready(function() {
	
	$("#number_songs").val(10)
	
	/// Setting the size of the box and image and player based on the generator width
	var generator_height = $("#generator_options").height()
	$("#engineplaylist_image").css("width",generator_height)
	$("#engineplaylist_image_image").css("width",generator_height)
	$("#engineplaylist_image_image").css("height",generator_height)
	$('#playlist_player').css("width",generator_height)
	$('#playlist_player').css("height",generator_height)
	$('#playlist').css("height",generator_height)


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
			$("#engineplaylist_image").html('<img id="engineplaylist_image_image" src="'+ cover_art +'">')
			
			var iw = $('#playlist_player').width();
			$('#engineplaylist_image_image').css({'width':iw+'px'});
			$('#engineplaylist_image_image').css({'height':iw+'px'});
			$('#engineplaylist_image_image').css({'z-index':'1'});

			

			/// Setting the size of the buttons
			// $(".engine_choice").css(({"height":generator_height/3}))





			string = ""
			for (song in uris) {
				string += uris[song] + ','
			}
			string = string.substring(0, string.length - 1);
			$('#playlist_player').html('<iframe src="https://embed.spotify.com/?uri=spotify:trackset:PREFEREDTITLE:' + string + '" width="'+generator_height+'" height="'+generator_height+'" frameborder="0" allowtransparency="true"></iframe>')
			$('#playlist_player').css(({'z-index':'-1'}))
			$('iframe').css(({'border-color':'white','border-width':'0.2em','border-style':'solid'}))

			/// When the user clicks on the image of the playlist ///
			 $('#engineplaylist_image_image').on('click', function() {
                $(this).fadeOut(2000);
                setTimeout(function() {
                	$("#playlist_player").css("z-index",1)
                	$("#engine_buttons").css({"display":"inline"})
                	var glyphicon_size = $('#playlist_player').height() / 10

                	$(".engine_choice").css(({"display":"inline","width":"100%","font-size":""+glyphicon_size+"px"}))
                	// $(".engine_choice span").css("top","5em")
                	var playlistheight = $('#playlist_player').height()
                	var button_height = $("#engine_like").height()

                	$("#engine_like").css("top",1/4 * playlistheight - 1/2 * button_height)
                	$("#engine_dislike").css("top",1/2 * playlistheight - 1/2 * button_height)
                	$("#engine_save").css("top",3/4 * playlistheight - 1/2 * button_height)
                

                },2000)




              	$("#like").on("click", function() {
              		$("#like").prop("disabled",true);
              		$("#dislike").prop("disabled",true);
					$.post("rating", {"uris": uris, "decision": "like"}, function(data){
						$("#like span").css("color","#ffd700")
					})
				})
				

				$("#dislike").on("click", function() {
					$("#like").prop("disabled",true);
              		$("#dislike").prop("disabled",true);	
					$.post("rating", {"uris": uris, "decision": "dislike"}, function(data){
						$("#dislike span").css("color","#ffd700")
						})
				})

				$("#save").on("click", function() {
						$("#save").prop("disabled",true);
						$.post("saveplaylist", {"uris": uris}, function(data){
							 $("#save span").css("color","#ffd700")
							 console.log("saved")
					})
				})	
		   	})		
		})
	})


	$('.fa-info').popover()



	// $(document).ajaxStart(function(){
 //        $('#playlist_player').append('<img src="/static/spotify/spiffygif.gif"/>')  
 //    });


    var pw = $('#playlist_player').width();
	$('#playlist_player').css({'height':pw+'px'});



	$('.engineslider').slider({
		formatter: function(value) {
		return 'Current value: ' + value;
		}
	});
})

