$(document).ready(function(){
    console.log('hello js')
    $("#sync").on("click", function(){
        console.log("clicked")
        $.getJSON("seed", function(data){
            console.log(data)
        })
    })
})