
$(document).ready(function(){
    
    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

    ga('create', 'UA-66616301-1', 'auto');
    ga('send', 'pageview');

    $.getJSON("/getfollowing", function(data){
        var followlist = data['JSON_follow_list'];
        var buttonIDs = [];
        $(".followButton").each(function(idx, button){
            for (item in followlist) {
                if (button.parentNode.innerText.indexOf(followlist[item]) != -1) {
                    $(this).addClass('following');
                    $(this).text('Following');
                }
            }       
        });
    });

    $.getJSON("/get_minifeed", function(data){
        var all_posts = data['all_posts'];
        var count = 0;
        for (post in all_posts) {
            $("#mini-feed").append("<div id=minifeed" + count + "><p>posted by: " + all_posts[post].user + "</p><p>" + all_posts[post].content + "</p><p><iframe src='https://embed.spotify.com/?uri=" + all_posts[post].track_uri + "'width=265 height=80 frameborder=0 allowtransparency=true></iframe></p>");
            count += 1;
        }
    })

    $(document).ajaxStart(function(){
        $('#loading').html('<img src="/static/spotify/ajax-loader.gif"/>')  
    });
    $(document).ajaxComplete(function(){
        $("#loading").empty();
    });
    $("#sync").on("click", function(){
        $.getJSON("/seed", function(data){
            console.log(data);
        })
    })

    $('button.followButton').on('click', function(event){
        event.preventDefault();
        console.log('clicked');
        $button = $(this);
        var id = $(this).parent().attr('id')
        var strippedID = id.replace("-button","") // ADAM'S NOTE TO SELF: COME BACK AND DO THIS PROPERLY
        if($button.hasClass('following')){
            
            
            $.post("/unfollow", {"id": strippedID}, function(data){
                console.log(data);
                $button.removeClass('following');
                $button.removeClass('unfollow');
                $button.text('Follow');
            })       
        } else {
                $.post("/follow", {'id': strippedID}, function(data) {
                console.log(data);
                $button.addClass('following');
                $button.text('Following');
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
            console.log(data['track_uri']);
            var track_uri = data['track_uri'];
        $("#song-reference").empty().append("<iframe src='https://embed.spotify.com/?uri=" + track_uri + "'width=300 height=80 frameborder=0 allowtransparency=true></iframe>");
        $("#song-comment").append($("#comment").val());
        });
    })
    $("#modal-button").on("click", function() {
        var comment = $("#song-comment").text();
        var src = $("#song-reference")[0].firstChild.src;
        var track_uri = src.replace("https://embed.spotify.com/?uri=","")
        $.post("create_post", {"comment": comment, "track_uri": track_uri}, function(data) {
            console.log(data);
        })
        $("#comment").val('');
        $("[name=search_query]").val('');
    })
})

