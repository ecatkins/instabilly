$(document).ready(function(){
    
    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

    ga('create', 'UA-66616301-1', 'auto');
    ga('send', 'pageview');

    $.getJSON("/getfollowing", function(data){
        console.log(data)
    })

    $(document).ajaxStart(function(){
        $('#loading').html('<img src="/static/spotify/ajax-loader.gif"/>')  
    });
    $(document).ajaxComplete(function(){
        $("#loading").empty();
    });
    $("#sync").on("click", function(){
        $.getJSON("/seed", function(data){
            console.log(data)
            $followButton = $(".followButton")
            //select all the followButtons and assign them the correct text and class based on JSON responsey
            console.log($followButton)
        })
    })

    $('button.followButton').on('click', function(event){
        event.preventDefault();
        $button = $(this);
        if($button.hasClass('following')){
            
            var username = $(this).parent().attr('username')
            $.post("/unfollow", {"username": username}, function(data){
                console.log(data)
                $button.removeClass('following');
                $button.removeClass('unfollow');
                $button.text('Follow');
            })       
        } else {
            var username = $(this).parent().attr('username')
            $.post("/follow", {'username': username}, function(data) {
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
})













$(".follow_buttons").on("click", function() {
    var username = $(this).parent().attr('username')
    $.post("/follow", {'username': username}, function(data) {
        console.log(data)
        $(this).hide()
    })
})