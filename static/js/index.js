$(document).ready(function () {
    // 在页面加载完成后调用 changeColor() 函数
    changeColor();
});

function changeColor() {
    console.log('changeColor function called');
    $('.fb-button').on('click', function () {
        var momentId = $(this).data('moment-id'); // 获取当前点击按钮的 momentId

        // 切换图标颜色
        $(this).find('i').addClass('active');

        // 发送请求或执行其他逻辑以记录点赞状态
        // ...

        // 示例：输出被点击的 momentId
        console.log('Moment ID:', momentId);
    });
}
