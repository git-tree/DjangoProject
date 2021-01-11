/**
 * Created by shusen.cui on 2021/1/9.
 */
$(function(){
});
layui.use('form', function(){
  var form = layui.form;
    form.render();
  //监听提交
  form.on('submit(formDemo)', function(data){
      upDate();
    //layer.msg(JSON.stringify(data.field));
    return false;
  });
});
function upDate(){
    var isfresh=false;
    $.ajax({
		cache : false,
		type : "POST",
		url : "/update_userinfo/",
		data : $('#editform').serialize(),// 你的formid
		async : false,
		error : function(request) {
			parent.layer.alert("Connection error");
		},
		success : function(data) {
			if (data['msg']=='ok') {
				parent.layer.msg("更新成功");
				var index = parent.layer.getFrameIndex(window.name); // 获取窗口索引
				parent.layer.close(index);
                parent.location.reload();
			} else {
				var index = parent.layer.getFrameIndex(window.name); // 获取窗口索引
				parent.layer.close(index);
				//parent.reLoad();
				parent.layer.alert(data['msg'])
			}
		}
	});
}