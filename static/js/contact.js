$(document).ready(function () {
    var targetElement = $(".page-wrapper");
    var targetPosition = targetElement.offset().top;
    var offset = 90; // 偏移量

    $('html, body').animate({
        scrollTop: targetPosition - offset
    }, 1000);
});
