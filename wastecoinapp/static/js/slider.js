var slideIndex = 0;
showSlides();
showSlidestwo();

function showSlides() {
    var i;
    var slides = document.getElementsByClassName("mySlides");
    var dots = document.getElementsByClassName("dot");
    for (i = 0; i < slides.length; i++) {
       slides[i].style.display = "none";  
    }
    slideIndex++;
    if (slideIndex > slides.length) {slideIndex = 1}    
    slides[slideIndex-1].style.display = "block";  
    setTimeout(showSlides, 5000); // Change image every 5 seconds
}



function showSlidestwo() {
    var i;
    var slides = document.getElementsByClassName("mySlides-two");
    var dots = document.getElementsByClassName("dot");
    for (i = 0; i < slides.length; i++) {
       slides[i].style.display = "none";  
    }
    slideIndex++;
    if (slideIndex > slides.length) {slideIndex = 1}    
    slides[slideIndex-1].style.display = "block";  
    setTimeout(showSlidestwo, 5000); // Change image every 5 seconds
}


// OVERLAY FUNCTIONS
function on() {
    document.getElementById("overlay").style.display = "block";
    document.getElementById("overlay").style.width = "100%";
    // document.getElementById("home").style.display = "none";
    // document.getElementById("home").style.width = "0";
}

function off() {
    document.getElementById("overlay").style.display = "none";
    document.getElementById("overlay").style.width = "0";
    // document.getElementById("home").style.display = "block";
    // document.getElementById("home").style.width = "100%";
}

