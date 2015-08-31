
function create_playlist (number_songs,follow,recency_effect,rating_effect,duplicate_artist,existing_playlist) {
	var post_data = {"type":"your_home","number_songs":number_songs, "follow":follow, "recency_effect":recency_effect,"rating_effect":rating_effect,"duplicate_artist":duplicate_artist, "existing_playlist": existing_playlist}

	
}



 var number_songs = 10
    var follow = 0
    var recency_effect = 10
    var rating_effect = 10
    var duplicate_artist = 10
    var existing_playlist = 10
    var post_data = {"type":"your_home","number_songs":number_songs, "follow":follow, "recency_effect":recency_effect,"rating_effect":rating_effect,"duplicate_artist":duplicate_artist, "existing_playlist": existing_playlist}

    $.post('playlist', post_data, function(data) {
            var uris = data['track_uris']
            var cover_art = data['cover_art']
            $("#yourplaylist_image").append('<img src="'+ cover_art +'">')
            var string = ""
            for (var song in uris) {
                string += uris[song] + ','
            }
            string = string.substring(0, string.length - 1);
            $('#yourplaylist_playlist').html('<iframe src="https://embed.spotify.com/?uri=spotify:trackset:PREFEREDTITLE:' + string + '" width="300" height="300" frameborder="0" allowtransparency="true"></iframe>')

            $('#yourplaylist img').on('click', function() {
                $(this).fadeOut(2000)
            })


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
