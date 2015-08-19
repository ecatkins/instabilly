$(document).ready(function(){
    console.log('hello js')
    $(document).ajaxStart(function(){
        $('#loading').html('<img src="/static/spotify/ajax-loader.gif"/>')  
    });
    $(document).ajaxComplete(function(){
        $("#loading").empty();
    });
    $("#sync").on("click", function(){
        console.log("clicked")
        $.getJSON("seed", function(data){
            console.log(data)
        })
    })
})