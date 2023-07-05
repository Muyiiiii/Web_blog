// 悬浮窗的显现与消失
$(document).ready(function () {
    $('.fly_button').mouseenter(function () {
        $('.fly_info').removeClass('hide');
    }).mouseleave(function () {
        $('.fly_info').addClass('hide');
    });
});
