$(document).ready(function () {
    var targetElement = $(".page-wrapper");
    var targetPosition = targetElement.offset().top;
    var offset = 90; // 偏移量

    $('html, body').animate({
        scrollTop: targetPosition - offset
    }, 1000);
});

document.getElementById('imageUpload').addEventListener('change', function (event) {
    var input = event.target;
    var reader = new FileReader();

    reader.onload = function () {
        var previewImage = document.getElementById('previewImage');
        previewImage.src = reader.result;
        previewImage.classList.remove('hide'); // 移除 hide 类，显示预览图像
    };

    if (input.files && input.files[0]) {
        reader.readAsDataURL(input.files[0]);
    }
});

