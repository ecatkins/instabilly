
$(document).ready(function(){
    
    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

    ga('create', 'UA-66616301-1', 'auto');
    ga('send', 'pageview');

    $.getJSON("/getfollowing", function(data){
        var followlist = data['JSON_follow_list']
        var buttonIDs = []
        $(".followButton").each(function(idx, button){
            for (item in followlist) {
                if (button.parentNode.innerText.indexOf(followlist[item]) != -1) {
                    $(this).addClass('following');
                    $(this).text('Following');
                }
            }       
        });
    });

    $(document).ajaxStart(function(){
        $('#loading').html('<img src="/static/spotify/ajax-loader.gif"/>')  
    });
    $(document).ajaxComplete(function(){
        $("#loading").empty();
    });
    $("#sync").on("click", function(){
        $.getJSON("/seed", function(data){
            console.log(data)
        })
    })

    $('button.followButton').on('click', function(event){
        event.preventDefault();
        console.log('clicked')
        $button = $(this);
        var id = $(this).parent().attr('id')
        var strippedID = id.replace("-button","")
        if($button.hasClass('following')){
            
            
            $.post("/unfollow", {"id": strippedID}, function(data){
                console.log(data)
                $button.removeClass('following');
                $button.removeClass('unfollow');
                $button.text('Follow');
            })       
        } else {
                $.post("/follow", {'id': strippedID}, function(data) {
                console.log(data)
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
    $("#songsearch").on("submit", function(event) {
        event.preventDefault();
        $("#searchresult_list").empty()
        $.getJSON("search", $("#songsearch").serialize(), function(data){
            console.log(data["search_result"])
            var count = 0
            for (item in data["search_result"]) {
                $("#searchresult_list").append("<li class=results id=" + count +">" +data["search_result"][item] + "</li>")
                count += 1
            }
        })
    })

})

