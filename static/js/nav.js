// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        document.getElementById("myBtn").style.display = "block";
    } else {
        document.getElementById("myBtn").style.display = "none";
    }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}


  $(document).ready(function() {
    $(".nav-link").click(function() {
        const t = $(this).attr("href");
        $('.active').removeClass('active');
        $("html, body").animate({
            scrollTop: $(t).offset().top - 50
        }, {
            duration: 1e3,
        });

        $('body').scrollspy({ target: '#navbar',offset: $(t).offset().top });
        $(this).parent().addClass('active');

        return false;
    });

});




