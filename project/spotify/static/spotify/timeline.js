function updateFollowButtons(){
    $.getJSON("/getfollowing", function(data){
        var followlist = data['JSON_follow_list'];
        console.log(followlist)
        $(".followButton").each(function(){
            for (item in followlist) {
                if ($(this).closest('tr').attr('id') === followlist[item]) {
                    $(this).addClass('following');
                    $(this).text('Following');
                }
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
                $("#followers").html(followers_count)
                $("#following").html(following_count)
                console.log('ers', followers_count, 'ing', following_count)
              }
        })
    } 


               

function check_song_count() {
    var num_songs = $("#profile_songs").text()
    if (num_songs === "0")    {
         $("#syncModal").modal('show')
         $("#sync_button").on('click', function() {
            $.getJSON("/seed", function(data){
                if (data['status'] === "redirect") {
                    $(location).attr('href', '/')
                }
                else {
                    update_user_profile()

                }            
            })
        })
    }
}


$(document).ready(function(){
    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

    ga('create', 'UA-66616301-1', 'auto');
    ga('send', 'pageview');
    
    

    /// On page load checks if the user has any songs, and makes sure they sync ///
    check_song_count()


    /// Sets the size of the profile text
    var profile_height = $("#profile").height()
    $("#profile_stats td").css(({"font-size":5*profile_height/10,"height":5*profile_height/10}))
    $("#profile_stats_names td").css(({"font-size":3*profile_height/10,"height":3*profile_height/10}))
   


    // console.log(profile_height)



    
    $("#following").on("click", function(event){
        event.preventDefault();
        $("#following-button").addClass("disabled").prop('disabled', true);
        $("#followers-button").addClass("active").prop('disabled', false);
        $("#followers-list").hide();
        updateFollowButtons();
    });

    $("#followers").on("click", function(event){
        event.preventDefault();
        $("#following-button").addClass("active").prop('disabled', false);
        $("#followers-button").addClass("disabled").prop('disabled', true);
        $("#following-list").hide();
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
        console.log(data)
        var all_posts = data['all_posts'];
        var count = 0;
        for (post in all_posts) {
            $("#mini-feed").append("<tr id=" + all_posts[post].user + " data-track=" + all_posts[post].track_uri + " class=minifeed-post><td><p>posted by: " + all_posts[post].user + "</p><p><button class='btn followButton'>Follow</button></p></td><td>" + all_posts[post].content + "</td><td><iframe src='https://embed.spotify.com/?uri=" + all_posts[post].track_uri + "'width=250 height=80 frameborder=0 allowtransparency=true></iframe></td><td><button id=song" + count + " type=button class='btn btn-default savesong'><span class='glyphicon glyphicon-floppy-disk' aria-hidden=true></span></button></tr>");
            count += 1;
        }
        updateFollowButtons();
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
            else {
                update_user_profile()
            }
        })
    })


    $("#mini-feed").on("click", '.savesong', function() {
        var track_uri = $(this).closest('tr').attr('data-track');
        $.post("save_song", {"track_uri": track_uri}, function(data){
            console.log(data)
            $(".savesong span").css("color","#ffd700")
        });
    });

    $("#mini-feed, #user-search-results, #following-list, #followers-list").on('click', 'button.followButton', function(event){
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
                update_user_profile();
            })       
        } else {
                $.post("/follow", {'id': id}, function(data) {
                var following = data["following"]
                $button.addClass('following');
                $button.text('Following');
                console.log(following)
                $("#following-list").append("<tr id=" + following + "><td>" + following + "</td><td><button class='btn followButton following'>Following</button></td></tr>")      
                update_user_profile();
                });
            }
        });
    $("#mini-feed, #user-search-results, #following-list, #followers-list").on("mouseenter", "button.followButton", function(){
        console.log("got it")
        $button = $(this)
        if($button.hasClass('following')) {
            $button.addClass('unfollow');
            $button.text('Unfollow');
        }
    });

    $("#mini-feed, #user-search-results, #following-list, #followers-list").on("mouseleave", "button.followButton", function(){
        if($button.hasClass('following')) {
            $button.removeClass('unfollow');
            $button.text('Following');
        }
    });

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
            console.log(userList)
            if (userList === "No results found..." || userList === "Please input a username.") {
                $("#user-search-results").append("<tr><td>" + userList + "</td></tr>")
            }
            else {
                var $searchdiv = $("#user-search");
                // <table id="user-search-results"></table>
                for (var i in userList) {
                    $("#user-search-results").append("<tr id=" + userList[i] +"><td>" + userList[i] + "</td><td><button class='btn followButton'>Follow</button></td></tr>");
                }
            }
        });
        updateFollowButtons();
    });



    /////// Generates playlists ///////
        /// Sets the initial size of the playlist div
    $(".timelineplaylist").css("height","20em")

    var num_songs = parseInt($("#profile_songs").text())

    if (num_songs > 0) {
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
                    /// On successful, disables relevant button and changes colors of to relevant colors
                    $("#yourplaylist_like").on("click", function() {
                         $("#yourplaylist_like").prop("disabled",true);
                         $("#yourplaylist_dislike").prop("disabled",true);
                        $.post("rating", {"uris": your_uris, "decision": "like"}, function(data){
                            $("#yourplaylist_like span").css("color","#ffd700")

                        })
                    })
                    $("#yourplaylist_dislike").on("click", function() {
                        $("#yourplaylist_like").prop("disabled",true);
                        $("#yourplaylist_dislike").prop("disabled",true);
                        $.post("rating", {"uris": your_uris, "decision": "dislike"}, function(data){
                            $("#yourplaylist_dislike span").css("color","#ffd700")

                        })
                    })
                    $("#yourplaylist_save").on("click", function() {
                        $("#yourplaylist_save").prop("disabled",true);
                        $.post("saveplaylist", {"uris": your_uris}, function(data){
                            $("#yourplaylist_save span").css("color","#ffd700")
                        })
                    })
                })       
            })
        }

    

    /// Friends ///
    var num_following = parseInt($("#following").text())

    if (num_following > 0) {
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
                    /// On successful, disables relevant button and changes colors of to relevant colors
                    $("#friendsplaylist_like").on("click", function() {
                        $("#friendsplaylist_like").prop("disabled",true)
                        $("#friendsplaylist_dislike").prop("disabled",true)
                        $.post("rating", {"uris": friends_uris, "decision": "like"}, function(data){
                            $("#friendsplaylist_like span").css("color","#ffd700")

                        })
                    })
                    $("#friendsplaylist_dislike").on("click", function() {
                        $("#friendsplaylist_like").prop("disabled",true)
                        $("#friendsplaylist_dislike").prop("disabled",true)
                        $.post("rating", {"uris": friends_uris, "decision": "dislike"}, function(data){
                            $("#friendsplaylist_dislike span").css("color","#ffd700")
                        })
                    })
                    $("#friendsplaylist_save").on("click", function() {
                        $("#friendsplaylist_save").prop("disabled",true)
                        $.post("saveplaylist", {"uris": friends_uris}, function(data){
                             $("#friendsplaylist_save span").css("color","#ffd700")
                        })
                    })

                })
             
            })

    }

    else {
        $("#friendsplaylist").html("<i class='fa fa-frown-o fa-5'></i>")
        $("#friendsplaylist i").css("height","50px")
        $("#friendsplaylist i").css("width","50px")
        $("#friendsplaylist i").css("z-index","1")
        $("#friendsplaylist i").css("font-size","50px")
        $("#friendsplaylist i").css("color","white")
        // $("#friendsplaylist").html("You have NO friends. Click the Find Other Users button in the menu bar to follow other people and see a playlist based on their songs (then refresh the page)")

    }


  


$('#testpopover').popover({
    html:true,
    title:"header",
    content: function() {
        return '<span id="like" class="glyphicon glyphicon-ok" aria-hidden="true"></span>'  
    }

})

})

