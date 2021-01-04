/**
 * Created by shusen.cui on 2020/11/26.
 */
layui.use('form', function(){
  var form = layui.form;
    form.render();
  //监听提交
  form.on('submit(formDemo)', function(data){
      save_rigist();
    //layer.msg(JSON.stringify(data.field));
    return false;
  });
});

function save_rigist() {

    layer.confirm('是否确认注册？', {
        btn: ['确定', '取消']
    }, function () {
        //if ($("#begintime").val() == '' || $("#endtime").val() == '') {
        //    layer.msg("开始/结束时间不能为空!", {icon: 2});
        //    return;
        //}
        $.ajax({
            cache: false,
            type: "POST",
            url: "/save_regist/",
            //traditional: true, //加上此项可以传数组
            dataType: 'json',
            data: $('#registform').serialize(),// 你的formid
            success: function (data) {
                if (data['msg'] == 'ok') {
                    parent.layer.msg('注册成功', {icon: 1});
                    var index = parent.layer.getFrameIndex(window.name); // 获取窗口索引
                    parent.layer.close(index);
                } else {
                    layer.msg(data['msg'], {icon: 2});
                }
            }
        });
    });
}
function checkexist() {
    //alert($("#username").val())
    var tmp=$("#username").val()
    if($("#username").val()==""){
        return;
    }
    $.ajax({
        type: 'POST',
        //traditional:true,// 传数组
        url: '/checkexist/',
        data:{
            'username':$("#username").val()
        },
        success: function (data) {
            if (data['msg'] == 'y') {
                //layer.msg('名字重复', {icon: 1});
                //reLoad();
                $("#isexist").html("");
                $("#username").val("");
                $("#isexist").html("<span class='layui-icon layui-icon-face-cry  layui-anim layui-anim-scaleSpring' style='color: #FF5722;'>名字["+tmp+"]重复，换一个试试呢!</span>");
            }else{
                $("#isexist").html("");
                $("#isexist").html("<span class='layui-icon layui-icon-face-smile  layui-anim layui-anim-scaleSpring' style='color: #5FB878'>恭喜,名字可用!</span>");

            }
        }
    });
}