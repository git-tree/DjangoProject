/**
 * Created by shusen.cui on 2021/1/9.
 */
$(function(){
      $.ajax({
        type: 'GET',
        //traditional:true,// 传数组
        //data: {
        //    'week': week
        //},
        dataType: 'json',
        url: '/getuserInfo/',
        success: function (data) {
            $.each(data, function (i, item) { //response为返回结果，是一个array，然后对该array进行遍历，fields属性中包含所有查询内容，pk为每条结果的主键字段
                var f = item.fields;
                //alert(f.username);
                //分发用户信息到页面中

                //头像
                //var oldsrc = $('#user_photo').attr('src');
                //var newsrc = oldsrc + f['photo_file'];
                //$("#user_photo").attr('src', newsrc)
                //alert($("#user_photo").attr('src'));

                //姓名
                $("#username").val(f.username);
                //邮箱
                $("#email").val(f.email);
                //性别
                $("#sex").val(f.sex);

            });
        }
    });
});