$(document).ready(function(){
    console.log("eeeeee");
    "use strict";

    // Animate loader off screen
    $('.se-pre-con').fadeOut(2500);

    // Smooth Scrolling
    $('html').smoothScroll(800);
    //Image Light Box Popup
    $('.image-link').magnificPopup({type: 'image'});
    $('.video-link').magnificPopup({type: 'iframe'});
});
