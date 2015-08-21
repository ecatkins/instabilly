$(document).ready(function(){
    
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-66616301-1', 'auto');
  ga('send', 'pageview');



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
    $(".follow_buttons").on("click", function() {
        var username = $(this).parent().attr('username')
        $.post("/follow", {'username': username}, function(data) {
            console.log(data)
        })
    })
})