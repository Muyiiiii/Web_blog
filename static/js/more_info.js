document.getElementById('imageUpload').addEventListener('change', function (event) {
    var input = event.target;
    var reader = new FileReader();

    reader.onload = function () {
        var image = new Image();
        image.src = reader.result;

        image.onload = function () {
            var canvas = document.createElement("canvas");
            var ctx = canvas.getContext("2d");

            var maxSide = 100;
            var width = image.width;
            var height = image.height;

            if (width > maxSide || height > maxSide) {
                var ratio = Math.min(maxSide / width, maxSide / height);
                width *= ratio;
                height *= ratio;
            }

            canvas.width = width;
            canvas.height = height;

            ctx.drawImage(image, 0, 0, width, height);

            var previewImage = document.getElementById('previewImage');
            previewImage.src = canvas.toDataURL("image/jpeg");
            previewImage.classList.remove('hide'); // 移除 hide 类，显示预览图像
        };
    };

    if (input.files && input.files[0]) {
        reader.readAsDataURL(input.files[0]);
    }
});
