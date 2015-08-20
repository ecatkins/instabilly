$(document).ready(function(){
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