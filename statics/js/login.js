//点击登陆

CanvasParticle();

function regist_user(){
    //alert();
    layer.open({
        type: 2,
        title: '用户注册',
        maxmin: true,
        shadeClose: false, // 点击遮罩关闭层
        area: ['500px', '400px'],
        //content: '/edit/' + id // iframe的url
        content: ['/regist/', 'no']
    });
}

layui.use('form', function(){
  var form = layui.form;
    form.render();
  //监听提交
  form.on('submit(formDemo)', function(data){
      var articleFrom = data.field;
      $.ajax({
        type:"POST",
        url:"/login/",
        data:articleFrom,
        dataType:"JSON",
        success:function (data) {
        }
    });
    //layer.msg(JSON.stringify(data.field));
    return true;
  });
});