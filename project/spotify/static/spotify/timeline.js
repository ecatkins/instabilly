function updateFollowButtons(){
    $.getJSON("/getfollowing", function(data){
        var followlist = data['JSON_follow_list'];
        $(".followButton").each(function(){
            for (item in followlist) {
                if ($(this).closest('tr').attr('id') === followlist[item]) {
                    $(this).addClass('following');
                    $(this).text('Following');
                }
                // else {
                //     $(this).removeClass('following');
                //     $(this).removeClass('unfollow');
                //     $(this).text('Follow');
                // }
            }
        });    
    });
}       


/// Call this on any event that changes the number of ///
///songs, following or followers of a user ///
function update_user_profile() {  
        $.ajax({
            url:'updateprofile',
            dataType:'json',
            success:function(data) {
                var song_count = data['song_count']
                var following_count = data['following_count']
                var followers_count = data['followers_count']
                $("#profile_songs").html(song_count)
                $("#profile_followers").html(following_count)
                $("#profile_following").html(followers_count)
              }
        })
    } 


               

function check_song_count() {
    $.get('hassongs', function(data) {
        if (data['has_songs'] === false) {
            $("#syncModal").modal('show')
            $("#sync_button").on('click', function() {
                $.getJSON("/seed", function(data){
                    if (data['status'] === "redirect") {
                        $(location).attr('href', '/')
                    }            
                })
            })
        }
    })
}


$(document).ready(function(){
    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

    ga('create', 'UA-66616301-1', 'auto');
    ga('send', 'pageview');
    
    

    /// Calls the user profile update on load of page
    update_user_profile()

    /// On page load checks if the user has any songs, and makes sure they sync ///
    check_song_count()
    
    
    $("#following").on("click", function(event){
        event.preventDefault();
        $("#following-button").addClass("disabled").prop('disabled', true);
        $("#followers-button").addClass("active").prop('disabled', false);
        $("#followers-list").hide();
        updateFollowButtons();
    });
    $("#following-button").on("click", function() {
        if ($(this).hasClass("active")){
            $(this).removeClass("active");
            $(this).addClass("disabled").prop('disabled', true);
            $("#followers-button").removeClass("disabled");
            $("#followers-button").addClass("active").prop('disabled', false);
            $("#followers-list").hide();
            $("#following-list").show();
            updateFollowButtons()
        }
        else {
            $(this).removeClass("disabled");
            $(this).addClass("active").prop('disabled', false);
            $("#followers-button").removeClass("active");
            $("#followers-button").addClass("disabled").prop('disabled', true);
            updateFollowButtons()
        }
    })

    $("#followers-button").on("click", function() {
        if ($(this).hasClass("active")){
            $(this).removeClass("active");
            $(this).addClass("disabled").prop('disabled', true);
            $("#following-button").removeClass("disabled");
            $("#following-button").addClass("active").prop('disabled', false);
            $("#following-list").hide();
            $("#followers-list").show();
            updateFollowButtons();
        }
        else {
            $(this).removeClass("disabled");
            $(this).addClass("active").prop('disabled', false);
            $("#following-button").removeClass("active");
            $("#following-button").addClass("disabled").prop('disabled', true);
            updateFollowButtons();
        }
    })

    $.getJSON("/get_minifeed", function(data){
        var all_posts = data['all_posts'];
        var count = 0;
        for (post in all_posts) {
            $("#mini-feed").append("<tr id=minifeed" + count + " class=minifeed-post><td><p>posted by: " + all_posts[post].user + "</p><p>" + all_posts[post].content + "</p></td><td><iframe src='https://embed.spotify.com/?uri=" + all_posts[post].track_uri + "'width=250 height=80 frameborder=0 allowtransparency=true></iframe></td></tr>");
            count += 1;
        }
    });


    $(document).ajaxStart(function(){
        $('#loading').html('<img src="/static/spotify/ajax-loader.gif"/>')  
    });
    $(document).ajaxComplete(function(){
        $("#loading").empty();
    });


    //// Syncs the users playlist, 
    $("#sync").on("click", function(event){
        event.preventDefault();
        $.getJSON("/seed", function(data){
            if (data['status'] === "redirect") {
                $(location).attr('href', '/')
            }
        })
    })

    $('button.followButton').on('click', function(event){
        console.log("here")
        event.preventDefault();
        $button = $(this);
        var id = $(this).closest('tr').attr('id')
        if($button.hasClass('following')){
                        
            $.post("/unfollow", {"id": id}, function(data){
                $button.removeClass('following');
                $button.removeClass('unfollow');
                $button.text('Follow');
                if ($button.closest('table').attr('id') === "following-list"){
                    $button.closest('tr').remove();
                    $("#followers-list").find("#" + id).find("button").removeClass("following").text("Follow");
                }
                else {
                    $("#following-list").find("#" + id).remove();
                }
            })       
        } else {
                $.post("/follow", {'id': id}, function(data) {
                var following = data["following"]
                $button.addClass('following');
                $button.text('Following');
                $("#following-list tr:last").after("<tr id=" + following + "><td>" + following + "</td><td><button class='btn followButton following'>Following</button></tr>")
                $('button.followButton').hover(function(){
                    $button = $(this);
                    if($button.hasClass('following')){
                        $button.addClass('unfollow');
                        $button.text('Unfollow');
                    }
                }, function(){
                    if($button.hasClass('following')){
                        $button.removeClass('unfollow');
                        $button.text('Following');
                    }
                });
            })
        }
    });
    $('button.followButton').hover(function(){
        $button = $(this);
        if($button.hasClass('following')){
            $button.addClass('unfollow');
            $button.text('Unfollow');
        }
    }, function(){
        if($button.hasClass('following')){
            $button.removeClass('unfollow');
            $button.text('Following');
        }
    });

    $("#find").on("click", function() {
        event.preventDefault();
        updateFollowButtons();
    })

    $("#createpost").on("click", function() {
        $("#searchresult_list").empty();
    })
    $("#song-search-button").on("click", function(event) {
        event.preventDefault();
        $("#searchresult_list").empty();
        var query = $("[name=search_query]").val();
        $.getJSON("search", {"search_query": query}, function(data){
            var count = 0;
            for (item in data["search_result"]) {
                $("#searchresult_list").append("<li class=results id=" + count +">" +data["search_result"][item] + "<button class=select-song>select</button></li>");
                count += 1;
            }
        })
    })
    $("#searchresult_list").on("click", ".select-song", function() {
        var text = $(this).parent().text();
        var substring = text.substring(0, text.length - 6);
        $("#searchresult_list").empty();
        $("#song-search-button").hide();
        $("[name=search_query]").val(substring);
    })
    $("#songsearch").on("submit", function(event) {
        event.preventDefault();
        var track_name = $("[name=search_query]").val()
        $.getJSON("track_uri", {"track_name": track_name}, function(data){
            var track_uri = data['track_uri'];
        $("#song-reference").empty().append("<iframe src='https://embed.spotify.com/?uri=" + track_uri + "'width=300 height=80 frameborder=0 allowtransparency=true></iframe>");
        $("#song-comment").append($("#comment").val());
        });
    })
    $("#post-it-button").on("click", function() {
        var comment = $("#song-comment").text();
        var src = $("#song-reference")[0].firstChild.src;
        var track_uri = src.replace("https://embed.spotify.com/?uri=","")
        $.post("create_post", {"comment": comment, "track_uri": track_uri}, function(data) {
        })
        $("#comment").val('');
        $("[name=search_query]").val('');
    })
    $("#usersearch").on("submit", function(event) {
        event.preventDefault();
        $("#user-search-results").empty();
        var usernameQuery = $("[name=user_query]").val();
        $.getJSON("find_user", {"usernameQuery": usernameQuery}, function(data){
            var userList = data["search_result"];
            if (userList === "No results found..." || userList === "Please input a username.") {
                $("#user-search-results").append("<tr><td>" + userList + "</td></tr>")
            }
            else {
                for (i in userList) {
                    $("#user-search-results").append("<tr><td>" + userList[i] + "</td><td><button class='btn followButton'>Follow</button></td></tr>")
                }
            }
        });
    });


    //// Generate user profile ////

    






    /////// Generates playlists ///////
        /// Sets the initial size of the playlist div
    $(".timelineplaylist").css("height","20em")


    /// Personal ///
    var number_songs = 10
    var follow = 0
    var recency_effect = 10
    var rating_effect = 10
    var duplicate_artist = 10
    var existing_playlist = 10
    var post_data = {"type":"your_home","number_songs":number_songs, "follow":follow, "recency_effect":recency_effect,"rating_effect":rating_effect,"duplicate_artist":duplicate_artist, "existing_playlist": existing_playlist}

    $.post('playlist', post_data, function(data) {
            var your_uris = data['track_uris']
            var cover_art = data['cover_art']
            $("#yourplaylist_image").append('<img id="yourplaylist_image_image" src="'+ cover_art +'">')
            $("#yourplaylist_image").css("width","80%")
            $("#yourplaylist_image_image").css("width","100%");



            /// setting the position of the buttons
            var div_width = $("#yourplaylist").width()
            var imageheight =  $("#yourplaylist_image").width();
            var buttons_width = $("#yourplaylist_buttons").width()
            var buttons_centre = (div_width - imageheight) + 0.5 * imageheight - 0.5 * buttons_width 
            $("#yourplaylist_buttons").css({"top":imageheight,"left":buttons_centre})

            
            ///Resets the size of the playlist div according to the size of the image ///
            $(".timelineplaylist").css("height",imageheight*1.2)




            var string = ""
            for (var song in your_uris) {
                string += your_uris[song] + ','
            }
            string = string.substring(0, string.length - 1);
            $('#yourplaylist_playlist').css("width","80%");
            var pw = $('#yourplaylist_playlist').width();
            $('#yourplaylist_playlist').css({'height':pw+'px'});


            $('#yourplaylist_playlist').html('<iframe src="https://embed.spotify.com/?uri=spotify:trackset:PREFEREDTITLE:' + string + '" width="'+pw+'" height="'+pw+'" frameborder="0" allowtransparency="true"></iframe>')
            

            /// When the user clicks on the image of the playlist ///
            $('#yourplaylist img').on('click', function() {
                $(this).fadeOut(2000)
                $("#yourplaylist_buttons").css("display","inline")
                /// Bind the like save and dislike events to the button
                $("#yourplaylist_like").on("click", function() {
                    $.post("rating", {"uris": your_uris, "decision": "like"}, function(data){
                    })
                })
                $("#yourplaylist_dislike").on("click", function() {
                    $.post("rating", {"uris": your_uris, "decision": "dislike"}, function(data){
                    })
                })
                $("#yourplaylist_save").on("click", function() {
                    $.post("saveplaylist", {"uris": your_uris}, function(data){
                    })
                })
            })



                     
        })

    /// Friends ///
    var number_songs2 = 10
    var follow2 = 10
    var recency_effect2 = 10
    var rating_effect2 = 10
    var duplicate_artist2 = 5
    var existing_playlist2 = 9
    var post_data2 = {"type":"your_friends","number_songs":number_songs2, "follow":follow2, "recency_effect":recency_effect2,"rating_effect":rating_effect2,"duplicate_artist":duplicate_artist2, "existing_playlist": existing_playlist2}


    $.post('playlist', post_data2, function(data) {
            var friends_uris = data['track_uris']
            var cover_art = data['cover_art']
            $("#friendsplaylist_image").html('<img id=friendsplaylist_image_image src="'+ cover_art +'">');
            $("#friendsplaylist_image").css("width","80%");
            $("#friendsplaylist_image_image").css("width","100%");
            
            /// setting the position of the buttons
            var div_width = $("#friendsplaylist").width()
            var imageheight =  $("#friendsplaylist_image").width();
            var buttons_width = $("#friendsplaylist_buttons").width()
            var buttons_centre = (div_width - imageheight) + 0.5 * imageheight - 0.5 * buttons_width 
            $("#friendsplaylist_buttons").css({"top":imageheight,"left":buttons_centre})



            var string = ""
            for (var song in friends_uris) {
                string += friends_uris[song] + ','
            }
            string = string.substring(0, string.length - 1);
            $('#friendsplaylist_playlist').css("width","80%");
            var pw = $('#friendsplaylist_playlist').width();
            $('#friendsplaylist_playlist').css({'height':pw+'px'});
            $('#friendsplaylist_playlist').html('<iframe src="https://embed.spotify.com/?uri=spotify:trackset:PREFEREDTITLE:' + string + '" width="'+pw+'" height="'+pw+'" frameborder="0" allowtransparency="true"></iframe>')


            /// When the user clicks on the image of the playlist ///
            $('#friendsplaylist img').on('click', function() {
                $(this).fadeOut(2000)
                $("#friendsplaylist_buttons").css("display","inline")
                /// Bind the like save and dislike events to the button
                $("#friendsplaylist_like").on("click", function() {
                    $.post("rating", {"uris": friends_uris, "decision": "like"}, function(data){
                    })
                })
                $("#friendsplaylist_dislike").on("click", function() {
                    $.post("rating", {"uris": friends_uris, "decision": "dislike"}, function(data){
                    })
                })
                $("#friendsplaylist_save").on("click", function() {
                    $.post("saveplaylist", {"uris": friends_uris}, function(data){
                    })
                })

            })
         
        })


$('#testpopover').popover({
    html:true,
    title:"header",
    content: function() {
        return '<span id="like" class="glyphicon glyphicon-ok" aria-hidden="true"></span>'  
    }

})

})

