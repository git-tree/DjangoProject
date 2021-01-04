/**
 * Created by shusen.cui on 2020/11/26.
 */
$(function () {
    loaddatetime();
    loadcolor();
});
function loadcolor() {
    layui.use('colorpicker', function () {
        var colorpicker = layui.colorpicker;
        colorpicker.render({
            elem: '#c_downtxt', //绑定元素
            color: $("#color_downtxt").val(),
            change: function (color) {
                $("#color_downtxt").val(color);
                //alert($("#color_downtxt").val());
            }
        });
        colorpicker.render({
            elem: '#c_downdate', //绑定元素
            color: $("#color_downdate").val(),
            change: function (color) {
                //alert(color)
                $("#color_downdate").val(color);
                //alert($("#color_downdate").val());
            }
        });

        colorpicker.render({
            elem: '#theme', //绑定元素
            color: $("#color_theme").val(),
            change: function (color) {
                //alert(color)
                $("#color_theme").val(color);
                parent.$("#nav").css('background-color', color)
                //alert($("#theme_color").val());
            }
        });
    });

}
function loaddatetime() {
    //日期时间选择器
    layui.use('laydate', function () {
        var laydate = layui.laydate;

        //执行一个laydate实例
        laydate.render({
            elem: '#downdate', //指定元素
            type: 'datetime',
            theme: '#393D49',
            calendar: true
        });
    });
}

function updateDown() {
    $.ajax({
        cache: false,
        type: "POST",
        url: "/updateDown/",
        data: $('#editform').serialize(),// 你的formid
        //async : false,
        error: function (request) {
            parent.layer.alert("Connection error");
        },
        success: function (data) {
            if (data['msg'] == 'ok') {
                parent.layer.msg("更新成功,请刷新页面查看效果!");
                parent.reLoad();
                var index = parent.layer.getFrameIndex(window.name); // 获取窗口索引
                parent.layer.close(index);
            } else {
                var index = parent.layer.getFrameIndex(window.name); // 获取窗口索引
                parent.layer.close(index);
                parent.reLoad();
                parent.layer.alert(data['msg'])
            }
        }
    });
}
