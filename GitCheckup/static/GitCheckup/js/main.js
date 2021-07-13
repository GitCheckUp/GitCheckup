$(document).ready(function(){
    "use strict";

    console.log(document.getElementById("state").value)
    if(document.getElementById("state").value == true){
      $('#se-pre-con').display = "-moz-flex";
      $('#se-pre-con').display = "-webkit-flex";
      $('#se-pre-con').display = "-ms-flex";
      $('#se-pre-con').display = "flex";
      document.getElementById("results").scrollIntoView();
    }
    else{
      $('#se-pre-con').display = "none";
    }

    // Animate loader off screen
    $('#se-pre-con').fadeOut(500);

    // Smooth Scrolling
    $('html').smoothScroll(800);
    //Image Light Box Popup
    $('.image-link').magnificPopup({type: 'image'});
    $('.video-link').magnificPopup({type: 'iframe'});
});

//Charts slide show
var slideIndex = 1;
showDivs(slideIndex);

function plusDivs(n) {
  showDivs(slideIndex += n);
}

function showDivs(n) {
  var i;
  var x = document.getElementsByClassName("mySlides");
  if (n > x.length) {slideIndex = 1}
  if (n < 1) {slideIndex = x.length} ;
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  x[slideIndex-1].style.display = "block";
}

function onSendForm() {
  window.location.reload();
  document.getElementById('se-pre-con').style.display = "-moz-flex";
  document.getElementById('se-pre-con').style.display = "-webkit-flex";
  document.getElementById('se-pre-con').style.display = "-ms-flex";
  document.getElementById('se-pre-con').style.display = "flex";
}
