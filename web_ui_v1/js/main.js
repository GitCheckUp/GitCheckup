$(document).ready(function(){
    
    "use strict";

    // Animate loader off screen
    $('.se-pre-con').fadeOut('slow');

    // Smooth Scrolling
    $('html').smoothScroll(800);
    //Image Light Box Popup
    $('.image-link').magnificPopup({type: 'image'});
    $('.video-link').magnificPopup({type: 'iframe'});
});