$(document).ready(function () {
    var targetElement = $("#introduction_us");
    var targetPosition = targetElement.offset().top;
    var offset = 90; // 偏移量

    $('html, body').animate({
        scrollTop: targetPosition - offset
    }, 1000);
});
