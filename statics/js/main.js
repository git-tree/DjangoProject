/**
 * Created by shusen.cui on 2020/11/24.
 */
$(function () {
    load();
    loaddatetime();
    getuserInfo();
    loaddaojishi();
    loadNowWeek();
    //加载月份下拉框值
    loadSelectMonth();
});
function loadNowWeek() {
    var nowweek;
    $.ajax({
        type: 'GET',
        //traditional:true,// 传数组
        //data: {
        //    'week': week,
        //    toemail: toemail,
        //},
        url: '/getnowweek/',
        async: false,
        success: function (data) {
            if (data['msg'] == 'ok') {
                //layer.msg('发送成功', {icon: 1});
                //reLoad();
                var YearWeek = data['week'];
                nowweek = YearWeek;
                $("#week").val(YearWeek);
                $("#nowweekhours").text("本周(" + YearWeek + ")加班时长");
            } else {
                layer.msg(data['msg']);
                //reLoad()
            }
        }
    });
    return nowweek;
}
function getuserInfo() {
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
                var oldsrc = $('#user_photo').attr('src');
                var newsrc = oldsrc + f['photo_file'];
                $("#user_photo").attr('src', newsrc)
                //alert($("#user_photo").attr('src'));

                //邮箱
                $("#useremail").val(f.email);

            });
        }
    });
}
layui.use('form', function () {
    var form = layui.form;
    form.render();
    //监听提交
    form.on('submit(formDemo)', function (data) {
        submsg();
        //layer.msg(JSON.stringify(data.field));
        return false;
    });
});
function loaddatetime() {
    //日期时间选择器
    layui.use('laydate', function () {
        var laydate = layui.laydate;
        var now = new Date();
        //执行一个laydate实例
        laydate.render({
            elem: '#begintime', //指定元素
            type: 'datetime',
            theme: '#393D49',
            calendar: true,
            value: now.getFullYear() + "-" + (now.getMonth() + 1) + "-" + now.getDate() + " " + "18:00:00"
        });
        laydate.render({
            elem: '#endtime', //指定元素
            type: 'datetime',
            value: now,
            theme: '#393D49',
            calendar: true

        });
        //年选择器
        laydate.render({
            elem: '#year'
            , type: 'year',
            value:now,
            theme: '#393D49',
        });
        laydate.render({
            elem: '#year_email'
            , type: 'year',
            value:now,
            theme: '#393D49',
        });
    });
}
function load() {
    $('#tb')
        .bootstrapTable(
            {
                method: 'GET', // 服务器数据的请求方式 get or post
                url: "/listall/", // 服务器数据的加载地址
                //	showRefresh : true,
                //	showToggle : true,
                //	showColumns : true,
                iconSize: 'outline',
                toolbar: '#exampleToolbar',
                striped: true, // 设置为true会有隔行变色效果
                dataType: "json", // 服务器返回的数据类型
                pagination: true, // 设置为true会在底部显示分页条
                // queryParamsType : "limit",
                // //设置为limit则会发送符合RESTFull格式的参数
                singleSelect: false, // 设置为true将禁止多选
                // contentType : "application/x-www-form-urlencoded",
                // //发送到服务器的数据编码类型
                pageSize: 7, // 如果设置了分页，每页数据条数
                pageNumber: 1, // 如果设置了分布，首页页码
                //search : true, // 是否显示搜索框
                showColumns: false, // 是否显示内容下拉框（选择显示的列）
                sidePagination: "server", // 设置在哪里进行分页，可选值为"client" 或者 "server"
                queryParams: function (params) {
                    return {
                        //说明：传入后台的参数包括offset开始索引，limit步长，sort排序列，order：desc或者,以及所有列的键值对
                        rows: params.limit,                         //页面大小
                        page: (params.offset / params.limit) + 1,   //页码
                        week: $("#week").val() == '' ? loadNowWeek() : $("#week").val(),
                        year:$("#year").val()==''?new Date().getFullYear():$("#year").val(),
                        //companyName:$('#companyName').val(),
                        //companySocialCreditCode:$('#companySocialCreditCode').val()
                    };
                },
                onDblClickRow: function (row, $element) {
                    var id = row.id;
                    upDate(id);
                },
                // //请求服务器数据时，你可以通过重写参数的方式添加一些额外的参数，例如 toolbar 中的参数 如果
                // queryParamsType = 'limit' ,返回参数必须包含
                // limit, offset, search, sort, order 否则, 需要包含:
                // pageSize, pageNumber, searchText, sortName,
                // sortOrder.
                // 返回false将会终止请求
                columns: [
                    {
                        checkbox: true
                    },
                    {
                        field: 'id',
                        title: '序号'
                    },
                    {
                        field: 'year',
                        title: '年份'
                    },
                    {
                        field: 'begintime',
                        title: '开始时间'
                    },
                    {
                        field: 'endtime',
                        title: '结束时间'
                    }
                    ,
                    {
                        field: 'week',
                        title: '第几周'
                    }
                    //{
                    //    field: 'pid',
                    //    title: '父id'
                    //},
                    ,
                    {
                        field: 'day',
                        title: '周几',
                        formatter: function (value, row, index) {
                            if (value == "周六") {
                                return '<span class="badge badge-success">' + value + '</span>'
                            }
                            return value;
                        }
                    },
                    {
                        field: 'hours',
                        title: '加班小时数',
                        formatter: function (value, row, index) {
                            if (row.day == "周六") {
                                return '<span class="badge badge-success">调休假+' + value + '</span>'
                            }
                            return value;
                        }
                    }
                    ,
                    {
                        field: 'month',
                        title: '月份'
                    },
                    {
                        title: '操作',
                        field: 'id',
                        align: 'center',
                        formatter: function (value, row, index) {
                            var u = '<a class="btn btn-outline-info btn-sm" href="#" title="修改"  onclick="upDate(\''
                                + row.id
                                + '\')"><i class="layui-icon layui-icon-edit"></i>修改</a> ';
                            var d = '<a class="btn btn-outline-dark btn-sm" href="#" title="删除"  onclick="deLete(\''
                                + row.id
                                + '\')"><i class="layui-icon layui-icon-close"></i>删除</a> ';
                            return u + d;
                        }
                    }]
            });
}
function loaddaojishi() {
    $.ajax({
        cache: false,
        type: "GET",
        url: "/loaddown/",
        //traditional: true, //加上此项可以传数组
        dataType: 'json',
        //data: $('#signupForm').serialize(),// 你的formid
        success: function (data) {
            if (data['msg'] == 'ok') {
                //layer.msg('添加成功', {icon: 1});
                //reLoad()
                layui.use('util', function () {
                    var util = layui.util;

                    //示例
                    var endTime = new Date(data['downdate']).getTime() //假设为结束日期
                        , serverTime = new Date().getTime(); //假设为当前服务器时间，这里采用的是本地时间，实际使用一般是取服务端的
                    util.countdown(endTime, serverTime, function (date, serverTime, timer) {
                        var str = date[0] + '天' + date[1] + '时' + date[2] + '分' + date[3] + '秒';
                        layui.$('#daojishi').html('<span style="color: ' + data['color_downtxt'] + ';cursor: pointer;"  onclick="editdowntxt()" class="layui-icon layui-icon-time "  title="倒计时" >&nbsp;' + data['downtxt'] + '&nbsp;</span><span  style="color: ' + data['color_downdate'] + '">' + str + '</span>');
                        //动画 layui-anim layui-anim-scaleSpring
                    });
                });
                //    加载主题
                $("#nav").css('background-color', data['color_theme'])

            } else {
                layer.msg(data['msg'], {icon: 2});
            }
        }
    });


}
function reLoad() {
    //$("#tb").bootstrapTable('selectPage', 1);
    $('#tb').bootstrapTable('refresh');
}
function submsg() {

    layer.confirm('是否确认提交加班数据？', {
        btn: ['确定', '取消']
    }, function () {
        if ($("#begintime").val() == '' || $("#endtime").val() == '') {
            layer.msg("开始/结束时间不能为空!", {icon: 2});
            return;
        }
        $.ajax({
            cache: false,
            type: "POST",
            url: "/counthours/",
            //traditional: true, //加上此项可以传数组
            dataType: 'json',
            data: $('#signupForm').serialize(),// 你的formid
            success: function (data) {
                if (data['msg'] == 'ok') {
                    layer.msg('添加成功', {icon: 1});
                    reLoad()
                } else {
                    layer.msg(data['msg'], {icon: 2});
                }
            }
        });
    });
}
function deLete(id) {
    layer.confirm('是否确认删除？', {
        btn: ['确定', '取消']
    }, function () {
        $.ajax({
            cache: false,
            type: "POST",
            url: "/delcount/",
            //traditional: true, //加上此项可以传数组
            dataType: 'json',
            data: {id: id},
            success: function (data) {
                if (data['msg'] == 'ok') {
                    layer.msg('删除成功', {icon: 1});
                    reLoad()
                } else {
                    layer.msg('删除失败', {icon: 2});
                    reLoad()
                }
            }
        });
    })

}
function upDate(id) {
    //alert(id);
    layer.open({
        type: 2,
        title: '修改',
        anim: 1,
        maxmin: true,
        shadeClose: false, // 点击遮罩关闭层
        area: ['500px', '660px'],
        //content: '/edit/' + id // iframe的url
        content: ['/edit/' + id, 'no']
    });
}
function batchRemove() {
    var rows = $('#tb').bootstrapTable('getSelections'); // 返回所有选择的行，当没有选择的记录时，返回一个空数组
    if (rows.length == 0) {
        layer.msg("请选择要删除的数据");
        return;
    }
    layer.confirm("确认要删除选中的'" + rows.length + "'条数据吗?", {
        btn: ['确定', '取消']
        // 按钮
    }, function () {
        var ids = new Array();
        // 遍历所有选择的行数据，取每条数据对应的ID
        $.each(rows, function (i, row) {
            ids[i] = row['id'];
        });
        $.ajax({
            type: 'POST',
            traditional: true,// 传数组
            data: {
                'ids': ids
            },
            url: '/batchRemove/',
            success: function (data) {
                if (data['msg'] == 'ok') {
                    layer.msg('删除成功', {icon: 1});
                    reLoad();
                } else {
                    layer.msg(data['msg']);
                    reLoad()
                }
            }
        });
    }, function () {

    });
}
function logout() {
    layer.confirm('是否确认退出系统？', {
        btn: ['确定', '取消']
    }, function () {
        window.location.href = '/logout/'
    })
}
function sendemail() {
    toemail = $("#useremail").val();
    layer.confirm('是否确认发送加班时长邮件到' + toemail + '?', {
        btn: ['确定', '取消']
    }, function () {
        $.ajax({
            type: 'GET',
            //traditional:true,// 传数组
            data: {
                'toemail': toemail
            },
            url: '/sendemail/',
            success: function (data) {
                if (data['msg'] == 'ok') {
                    layer.msg('发送成功', {icon: 1});
                    //reLoad();
                } else {
                    layer.msg(data['msg']);
                    //reLoad()
                }
            }
        });
        //window.location.href='/sendemail/'
    })
}
function editdowntxt() {
//alert();
    layer.open({
        type: 2,
        title: '修改倒计时、主题等设置',
        maxmin: true,
        shadeClose: false, // 点击遮罩关闭层
        area: ['500px', '550px'],
        //content: '/edit/' + id // iframe的url
        content: ['/editdown/', 'no']
    });
}
function tipnowWeek() {
    layer.tips('本周是第' + getYearWeek(new Date()) + '周', '#searchweek', {
        tips: 3
    });
}
function sendsearchEmail() {
    toemail = $("#useremail").val();
    var week = $("#week").val();
    var year=$("#year").val();
    layer.confirm('是否确认发送'+year+'年第' + week + '周加班时长邮件到' + toemail + '?', {
        btn: ['确定', '取消']
    }, function () {
        $.ajax({
            type: 'GET',
            //traditional:true,// 传数组
            data: {
                'week': week,
                year:year,
                toemail: toemail,
            },
            url: '/sendsearchemail/',
            success: function (data) {
                if (data['msg'] == 'ok') {
                    layer.msg('发送成功', {icon: 1});
                    //reLoad();
                } else {
                    layer.msg(data['msg']);
                    //reLoad()
                }
            }
        });
        //window.location.href='/sendemail/'
    })
}
function changeweek() {
    var searchweek = $("#week").val();
    $("#sendemail_search").text("发送" + searchweek + "周时长到邮件")
}
function up_head() {
    layer.open({
        type: 2,
        title: '修改头像',
        maxmin: true,
        shadeClose: false, // 点击遮罩关闭层
        area: ['500px', '550px'],
        //content: '/edit/' + id // iframe的url
        content: ['/up_head/', 'no']
    });
}
function loadSelectMonth() {
    //加载月份加班时长下拉框
    $("#month").empty();
    $("#month").append('<option value="">请选择月份</option>');
    for (var i = 1; i <= 12; i++) {
        $("#month").append('<option value=' + i + '>' + i + '</option>');
    }
}
function summonthhour() {
    month = $("#month").val();
    year =$("#year_email").val()
    if (month == "") {
        //alert(month);
        layer.tips('请选择月份', '#month', {
            tips: 3
        });
        return;
    }
      if (year == "") {
        //alert(month);
        layer.tips('请选择年份', '#year_email', {
            tips: 3
        });
        return;
    }
    $.ajax({
        type: 'GET',
        //traditional:true,// 传数组
        data: {
            'month': month,
            'year':year
        },
        url: '/summonthhour/',
        success: function (data) {
            if (data['msg'] == 'ok') {
                //layer.msg('发送成功', {icon: 1});
                //reLoad();
                var hour = data['hour'];
                var hour_TX = data['hour_TX'];
                if (data['hour'] == null || data['hour'] == '') {
                    hour = 0;
                }
                if (data['hour_TX'] == null || data['hour_TX'] == '') {
                    hour_TX = 0;
                }
                $("#summonthhour").text('' + month + '月加班总时间:' + hour + '其中调休假' + hour_TX)
            } else {
                layer.msg(data['msg']);
                //reLoad()
            }
        }
    });
}