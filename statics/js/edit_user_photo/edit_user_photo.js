/**
 * Created by shusen.cui on 2020/12/4.
 */
$(function () {
    load_up_photo();
});
function load_up_photo() {
    layui.use('upload', function () {
        var $ = layui.jquery
            , upload = layui.upload;
        //拖拽上传
        upload.render({
            elem: '#test10'
            , url: '/save_user_photo/' //改成您自己的上传接口
            , done: function (res) {
                if (res['msg'] == "ok") {
                    //alert(layui.$('#uploadDemoView').find('img').attr('src'));
                    var oldsrc = layui.$('#uploadDemoView').find('img').attr('src');
                    var newsrc = oldsrc + res['img'];
                    //alert(newsrc);
                    //layui.$('#uploadDemoView').removeClass('layui-hide').find('img').attr('src', newsrc);
                    parent.$("#user_photo").attr('src', newsrc)
                    var index = parent.layer.getFrameIndex(window.name); // 获取窗口索引
                    parent.layer.close(index);
                    parent.layer.msg("更新成功!");
                }
            }
        });
    });
}