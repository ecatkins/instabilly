$(document).ready(function(){
    console.log('hello')
    $("#sync").on("click", function(){
        console.log("clicked")
        $.getJSON("sync/", function(data){
            console.log(data)
        })
    })
})