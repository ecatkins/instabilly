$(document).ready(function(){

    var d = new Date();
    var timeZoneOffset = d.getTimezoneOffset();

    $.post("timezone", {"timeZoneOffset": timeZoneOffset}, function() {
    });

});