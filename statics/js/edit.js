/**
 * Created by shusen.cui on 2020/11/25.
 */
$(function(){
    loaddatetime()
    load();
});
function loaddatetime() {
    //日期时间选择器
    layui.use('laydate', function () {
        var laydate = layui.laydate;

        //执行一个laydate实例
        laydate.render({
            elem: '#begintime', //指定元素
            type: 'datetime',
			theme: '#393D49',
            calendar: true
        });
        laydate.render({
            elem: '#endtime', //指定元素
            type: 'datetime',
			theme: '#393D49',
            calendar: true

            //value: new Date()
        });
    });
}
function upDate(){
    $.ajax({
		cache : false,
		type : "POST",
		url : "/update/",
		data : $('#editform').serialize(),// 你的formid
		//async : false,
		error : function(request) {
			parent.layer.alert("Connection error");
		},
		success : function(data) {
			if (data['msg']=='ok') {
				parent.layer.msg("更新成功");
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
$('#hours').on('click', function(){
  layer.tips('不可编辑,修改时间后自动计算。', '#hours', {
  tips: 3
});
});
$('#week').on('click', function(){
  layer.tips('不可编辑,修改时间后自动计算。', '#week', {
  tips: 3
});
});
$('#day').on('click', function(){
  layer.tips('不可编辑,修改时间后自动计算。', '#day', {
  tips: 3
});
});
$('#month').on('click', function(){
  layer.tips('不可编辑,修改时间后自动计算。', '#month', {
  tips: 3
});
});
$('#year').on('click', function(){
  layer.tips('不可编辑,修改时间后自动计算。', '#year', {
  tips: 3
});
});