from django.http import HttpResponseRedirect
from django.views.decorators import csrf
from django.shortcuts import render,redirect
from django.http import  HttpResponse
from . import models
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import datetime
import time
import json
from django.conf import settings
from django.core import serializers
from django.forms.models import model_to_dict
from django.core.mail import send_mail
from .utils import dateStr2Date
# Create your views here.

def hello(request):
    return HttpResponse("你好，崔术森")

def htmlout(request):
    # viewlist=[1,2,3]
    # viewdict={'name':'崔术森abc'}
    # viewdict=1024
    # viewdict='<a href="https://www.baidu.com" target="_blank">百度</a>'
    # viewdict=99
    viewdict=[1,9,9,8,0,9,2,3]
    return render(request,'test.html',{'dict':viewdict})

def loadpic(requert):
    name="崔术森微信头像"
    return render(requert,'test.html',{'name':name})

def ex(req):
    return render(req,"child.html")


def u2dict(obj):
    a={}
    a.update(obj.__dict__)
    return a
def login(request):
    """
    登陆
    :param request:
    :return:
    """
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == "GET":
        return render(request, "login.html")
    username = request.POST.get("username")
    password = request.POST.get("password")
    print(username,password)
    tips=''
    if username=='' or password=='':
        tips="账号或密码不能为空"
        return render(request,'login.html',{'tips':tips})
    else:
        user_obj = models.User.objects.filter(username=username, password=password).first()
        if not user_obj:
            # return redirect("/login/")
            tips="账号或密码错误"
            return render(request,'login.html',{'tips':tips})
        # request.session.set_expiry(10*60)#10分钟后过期
        # request.session.set_expiry(5)#5s后过期
        request.session.set_expiry(0)#关闭浏览器过期

        request.session['is_login'] = True
        request.session['id'] = user_obj.id
        request.session['username'] = user_obj.username
        # request.session['useremail'] = user_obj.email

        # user=json.dumps(user_obj,default=u2dict)
        # user=json.loads(user)
        # request.session['user']=user
        # return render(request,'index.html',{'userinfo':user_obj})
        return redirect('/index/')
def getuserInfo(request):
    """
    登陆成功后获取用户信息
    :param request:
    :return:
    """
    data={}
    id=request.session.get('id')
    user = models.User.objects.filter(id=id)
    user=serializers.serialize("json",user)
    return HttpResponse(user, content_type='application/json')

def index(request):
    """
    主页
    :param request:
    :return:
    """
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request,'index.html')

def regist(request):
    """
    用户注册
    :param request:
    :return:
    """
    return render(request,'regist.html')

def save_regist(request):
    """
    保存注册信息
    :param request:
    :return:
    """
    data={}
    if request.method=='POST':
        try:
            username=request.POST.get('username')
            password=request.POST.get('password')
            email=request.POST.get('email')
            sex=request.POST.get('sex')
            # print(username,password,email,sex)
        except:
            data={'msg':'获取信息错误!'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        models.User.objects.create(username=username,password=password,email=email,sex=sex)
        data={'msg':'ok'}
        return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def checkexist(request):
    """
    检查是否重名
    :return:
    """
    if request.method=='POST':
        data={'msg':'n'}
        # print(request.POST.get('username'))
        username=request.POST.get('username')
        res=models.User.objects.filter(username=username)
        if len(res)>0:
            # 重复
            data={'msg':'y'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def logout(request):
    """
    退出登录
    :param request:
    :return:
    """
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login/")

def getnowweek(request):
    """
    获取当前时间是一年的第几周
    :param request:
    :return:
    """
    data={}
    try:
        sql='select WEEK(now())'
        res=executesql(sql)[0]
        print('当前周是',res)
        data['msg']="ok"
        data['week']=res
    except:
        data['msg']='查询周失败，请联系管理员！'
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def listall(request):
    """
    查询所有数据
    :param request:
    :return:
    """
    if request.method == 'GET':
        pid=request.session.get('id')
        page = request.GET.get('page')
        num = request.GET.get('rows')
        week=request.GET.get('week')
        year=request.GET.get('year')
        print('weekwekwekwek',week,year)
        total = models.Overtime.objects.filter(pid=pid,week=week,year=year).count()
        hours = models.Overtime.objects.filter(pid=pid,week=week,year=year).order_by('id')[int(num)*(int(page)-1):int(page)*int(num)]
        rows = []
        print("hours",len(hours))

        # if(len(hours))==0:
        #     data={'msg':'未查询到信息'}
        #     return HttpResponse(json.dumps(data), content_type='application/json')
        for h in hours:
            rows.append({
                'id': h.id,
                'day': h.day,
                'begintime': h.begintime,
                'endtime': h.endtime,
                'hours': h.hours,
                'pid': h.pid,
                'week':h.week,
                'month':h.month,
                'year':h.year,
            })
        data = {'total': total, 'rows': rows}
        return HttpResponse(json.dumps(data,cls=DateEncoder), content_type='application/json')

@csrf_exempt
def counthours(request):
    """
    添加一条数据
    :param request:
    :return:
    """
    tips=''
    try:
        begin=request.POST.get('begintime')
        end=request.POST.get('endtime')
        # begin=parse(begintime)
        # end=parse(endtime)
        if begin=='' or begin is None or end== '' or end is None:
            tips={'msg':'异常，请选择时间!'}
            return HttpResponse(json.dumps(tips), content_type='application/json')
    except:
        tips={'msg':'时间异常，请选择时间!'}
        # return render(request,'index.html',{"msg":tips})
        return HttpResponse(json.dumps(tips), content_type='application/json')

    print(begin,end,'**********************')
    # 获取今天周几、几个小时、存入数据库
    hour_sql="SELECT TIMESTAMPDIFF(MINUTE,'%s','%s')"%(begin,end)
    # 小时
    hour=(float)(executesql(hour_sql)[0]/60)
    hour='%.2f'%hour
    week_sql=" SELECT DAYOFWEEK('%s')"%begin
    # 周几
    week=formartweek(executesql(week_sql)[0])
    # pid
    try:
        pid=request.session.get('id')
    except:
        tips={'msg':'获取session id 失败!'}
        # return render(request,'index.html',{"msg":tips})
        return HttpResponse(json.dumps(tips), content_type='application/json')

    # 一年的第几周
    year_week_sql='''
    SELECT WEEK('%s',1)
    '''%begin
    year_week= executesql(year_week_sql)[0]
    print('rear_week sssssssss',year_week)
    # 月份
    month_sql='''
    SELECT MONTH('%s')
    '''%begin
    month=executesql(month_sql)[0]
    # 年份year
    dateTime_p = datetime.datetime.strptime(begin,'%Y-%m-%d %H:%M:%S')
    year=dateTime_p.year
    try:
        overtime=models.Overtime.objects.create(day=week,begintime=begin,endtime=end,hours=hour,pid=pid,week=year_week,month=month,year=year)
        print(overtime,type(overtime))
        tips={'msg':'ok'}
    except:
        tips={'msg':'添加异常'}
        # return render(request,'index.html',{"msg":tips})
    # return render(request,'index.html',{"msg":tips})
    return HttpResponse(json.dumps(tips), content_type='application/json')

@csrf_exempt
def delcount(request):
    """
    删除单个数据
    :param request:
    :return:
    """
    if request.method=='POST':
        id=request.POST.get('id')
        print(id)
        res=models.Overtime.objects.filter(id=id).delete()
        print(res)
        data=''
        if res[0] >0:
            data={'msg':'ok'}
        else:
            data={'msg':'no'}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def batchRemove(request):
    """
    批量删除
    :param request:
    :return:
    """
    if request.method=='POST':
        ids=request.POST.getlist('ids')#接数组用getlist
        ids=','.join(ids)
        data=''
        try:
            models.Overtime.objects.extra(where=[' id  IN ( '+ids+')']).delete()
            data={'msg':'ok'}
        except:
            data={'msg':'删除失败'}
    return HttpResponse(json.dumps(data), content_type='application/json')

# @csrf_exempt
def edit(request,id):
    """
    点击编辑按钮转发一条信息到编辑界面
    :param request:
    :param id:
    :return:
    """
    #通过id查询这个信息
    hour=models.Overtime.objects.filter(id=id)
    # print('hour查询出来是',hour[0].id)
    hour=hour[0]
    data={}
    data['id']=hour.id
    data['day']= hour.day
    data['begintime']=hour.begintime
    data['endtime']= hour.endtime
    data['hours']= hour.hours
    data['pid']= hour.pid
    data['week']=hour.week
    data['month']=hour.month
    data['year']=hour.year
    print(data)
    return render(request,'edit.html',{'data':data})

@csrf_exempt
def update(request):
    """
    更新保存一条信息
    :param request:
    :return:
    """
    if request.method=='POST':
        # print('form id d d ',request.POST.get('id'))
        data={}
        try:
            id=request.POST.get('id')
            pid=request.POST.get('pid')
            begintime=request.POST.get('begintime')
            endtime=request.POST.get('endtime')
            # hours=request.POST.get('hours')
            hour_sql="SELECT TIMESTAMPDIFF(MINUTE,'%s','%s')"%(begintime,endtime)
            # 小时
            hours=(float)(executesql(hour_sql)[0]/60)
            hours='%.2f'%hours

            # 一年的第几周
            year_week_sql="SELECT WEEK('%s',1)"%begintime
            year_week= executesql(year_week_sql)[0]
            # week=request.POST.get('week')
            # day=request.POST.get('day')
            week_sql=" SELECT DAYOFWEEK('%s')"%begintime
            # 周几
            day=formartweek(executesql(week_sql)[0])
            # 月份
            month_sql="SELECT MONTH('%s')"%begintime
            month=executesql(month_sql)[0]
            # 年份year
            year=dateStr2Date(begintime).year
        except:
            data={'msg':'获取异常!'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        try:
            # res=executesql(sql)
            models.Overtime.objects.filter(id=id).update(pid=pid,begintime=begintime,endtime=endtime,hours=hours,week=year_week,day=day,month=month,year=year)
            data={'msg':'修改成功!'}
        except:
            data={'msg':'修改失败!'}
        return HttpResponse(json.dumps(data), content_type='application/json')




class DateEncoder(json.JSONEncoder):
    """
        转换数据库里面datetime字段，不转换会出现异常
    """
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self,obj)

def executesql(sql):
    """
    执行sql mysql
    :param sql:
    :return:
    """
    ex=connection.cursor()
    ex.execute(sql)
    res=ex.fetchone()
    ex.close()
    return res

def formartweek(week_num):
    """
    格式化周期数，如1是周日
    :param week_num: 数值
    :return: 返回中文周
    """
    week=['周日','周一','周二','周三','周四','周五','周六']
    return  week[week_num-1]

def sendemail(request):
    """
    发邮件
    :param request:
    :return:
    """
    data=''
    if request.method=='GET':
        #获取当前周
        year_week= int(time.strftime("%W"))+1
        #获取当前session id
        try:
            pid=request.session.get('id')
        except:
            data={'msg':'获取id失败!'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        # 获取邮箱
        try:
            toemail=request.GET.get("toemail")
            print('toemail',toemail)
        except:
            data={'msg':'发送中出现异常，未知地址...'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        #查询当前用户本周加班时长
        sql="SELECT SUM(c.hours) from coh_overtime c WHERE c.pid='%s' AND c.`week`='%s'"%(pid,year_week)
        try:
            res=executesql(sql)
            print(res)
        except:
            data={'msg':'查询失败!'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        # 本周加班时长
        now_week_hours=res[0]
        # 调休假
        sql_TX="SELECT SUM(c.hours) from coh_overtime c WHERE c.pid=%d AND c.`week`='%s' and c.`day`='周六'"%(int(pid),year_week)
        now_week_hours_TX=executesql(sql_TX)[0]
        print(now_week_hours_TX)
        if now_week_hours is None:
            now_week_hours=0
        if now_week_hours_TX is None:
            now_week_hours_TX=0
        try:
            send_mail(
                    '%s周的加班时长'%year_week,
                    '%s周加班时长为:%s小时\n其中调休假%s小时,普通加班%s小时。'%(year_week,now_week_hours,now_week_hours_TX,(now_week_hours-now_week_hours_TX)),
                    'shusen.cui@tinno.com',
                    ['%s'%toemail],
            )
            data={'msg':'发送邮件成功，请注意查收!'}
        except:
            data={'msg':'发送失败!'}
    return HttpResponse(json.dumps(data), content_type='application/json')

def sendsearchemail(request):
    """
    发送指定周的邮件
    :param request:
    :return:
    """
    week=request.GET.get('week')
    year=request.GET.get('year')
    print('wewkewekwkwkekk',year,week)
    #获取当前session id
    try:
        pid=request.session.get('id')
    except:
        data={'msg':'获取id失败!'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    # 获取邮箱
    try:
        toemail=request.GET.get('toemail')
        print('toemail',toemail)
    except:
        data={'msg':'发送中出现异常，未知地址...'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    #查询当前用户本周加班时长
    sql="SELECT SUM(c.hours) from coh_overtime c WHERE c.pid='%s' AND c.`week`='%s' AND c.`year`=%s"%(pid,week,year)
    try:
        res=executesql(sql)
        print(res)
    except:
        data={'msg':'查询失败!'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    # 本周加班时长
    now_week_hours=res[0]
    # 调休假
    sql_TX="SELECT SUM(c.hours) from coh_overtime c WHERE c.pid=%d AND c.`week`='%s' AND c.`year`=%s  and c.`day`='周六'"%(int(pid),week,year)
    now_week_hours_TX=executesql(sql_TX)[0]
    if now_week_hours is None:
        now_week_hours=0
    if now_week_hours_TX is None:
        now_week_hours_TX=0

    try:
        send_mail(
                '%s年第%s周的加班时长'%(year,week),
                '%s年第%s周加班时长为:%s小时\n其中调休假为%s小时,普通加班时长为%s小时。'%(year,week,now_week_hours,now_week_hours_TX,(now_week_hours-now_week_hours_TX)),
                'shusen.cui@tinno.com',
                ['%s'%toemail],
        )
        data={'msg':'发送邮件成功，请注意查收!'}
    except:
        data={'msg':'发送失败!'}
    return HttpResponse(json.dumps(data), content_type='application/json')

def summonthhouremail(request):
    '''
    发送月度邮件
    :return:
    '''
    if request.method=='GET':
        print('aaaaaa')
        # 获取邮箱
        try:
            toemail=request.GET.get('toemail')
            print('toemail',toemail)
        except:
            data={'msg':'发送中出现异常，未知地址...'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        data={}
        year=request.GET.get("year")
        month=request.GET.get("month")
        # print('month',month,year)
        pid=request.session.get("id")
        # print('pidss',pid)
        sql='SELECT SUM(hours) FROM coh_overtime WHERE pid=%d AND month=%d AND year=%s'%(int(pid),int(month),int(year))
        # print('sqlresult',executesql(sql))
        sql_TX='SELECT SUM(hours) FROM coh_overtime WHERE pid=%d AND month=%d AND year=%s and day="周六"'%(int(pid),int(month),int(year))
        try:
            counthours_month=executesql(sql)[0]

            counthours_month_TX=executesql(sql_TX)

            data['msg']='ok'
            data['hour']=counthours_month
            data['hour_TX']=counthours_month_TX[0]
        except :
            data['msg']='查询出现异常'
        try:
            send_mail(
                    '%s年%s月加班时长'%(year,month),
                    '%s年%s月加班时长为:%s小时\n其中调休假%s小时,普通加班%s小时。'%(year,month,data['hour'],data['hour_TX'],(data['hour']-data['hour_TX'])),
                    'shusen.cui@tinno.com',
                    ['%s'%toemail],
            )
            data={'msg':'发送邮件成功，请注意查收!'}
        except:
            data={'msg':'发送失败!'}
        return HttpResponse(json.dumps(data), content_type='application/json')

def summonthhour(request):
    """
    查询指定月的总共加班小时
    :param request:
    :return:
    """
    if request.method=='GET':
        data={}
        year=request.GET.get("year")
        month=request.GET.get("month")
        # print('month',month,year)
        pid=request.session.get("id")
        # print('pidss',pid)
        sql='SELECT SUM(hours) FROM coh_overtime WHERE pid=%d AND month=%d AND year=%s'%(int(pid),int(month),int(year))
        # print('sqlresult',executesql(sql))
        sql_TX='SELECT SUM(hours) FROM coh_overtime WHERE pid=%d AND month=%d AND year=%s and day="周六"'%(int(pid),int(month),int(year))
        try:
            counthours_month=executesql(sql)[0]

            counthours_month_TX=executesql(sql_TX)

            data['msg']='ok'
            data['hour']=counthours_month
            data['hour_TX']=counthours_month_TX[0]
        except :
            data['msg']='查询出现异常'

        return HttpResponse(json.dumps(data), content_type='application/json')
def loaddown(requset):
    """
    加载倒计时
    :param requset:
    :return:
    """
    pid=requset.session.get('id')
    res=models.Countdown.objects.filter(pid=pid)
    data={}
    if len(res)==1:
        res=res[0]
        data['id']=res.id
        data['pid']=res.pid
        data['downtxt']=res.downtxt
        data['downdate']=res.downdate
        data['color_downdate']=res.color_downdate
        data['color_downtxt']=res.color_downtxt
        data['msg']='ok'
        data['color_theme']=res.color_theme
        print('user,s theme:',res.color_theme)

    else:
        # 这个人没有设置倒计时，加载默认的
        res=models.Countdown.objects.filter(pid=0)
        res=res[0]
        data['id']=res.id
        data['pid']=requset.session.get('id')
        data['downtxt']=res.downtxt
        data['downdate']=res.downdate
        data['color_downdate']=res.color_downdate
        data['color_downtxt']=res.color_downtxt
        data['msg']='ok'
        data['color_theme']=res.color_theme
        print('defaul theme:',res.color_theme)
    return HttpResponse(json.dumps(data), content_type='application/json')



def editdown(request):
    """
    点击编辑倒计时
    :param request:
    :return:
    """
    pid=request.session.get('id')
    downinfo=models.Countdown.objects.filter(pid=pid)
    if len(downinfo)==1:
        downinfo=downinfo[0]
    else:
        downinfo=models.Countdown.objects.filter(pid=0)
        downinfo=downinfo[0]
        downinfo.pid=request.session.get('id')
    return render(request,'edit_down.html',{'data':downinfo})

@csrf_exempt
def updateDown(request):
    """
    更新倒计时
    :param request:
    :return:
    """
    data={}
    if request.method=='POST':
        id=request.POST.get('id')
        pid=request.POST.get('pid')
        downtxt=request.POST.get('downtxt')
        downdate=request.POST.get('downdate')
        color_downtxt=request.POST.get('color_downtxt')
        color_downdate=request.POST.get('color_downdate')
        color_theme=request.POST.get('color_theme')
        # 先看看这个人有没有设置倒计时，没有就是添加，有就是更新
        re=models.Countdown.objects.filter(pid=pid)
        if len(re)==0:
            models.Countdown.objects.create(pid=pid,downtxt=downtxt,downdate=downdate,color_downdate=color_downdate,color_downtxt=color_downtxt,color_theme=color_theme)
            data={'msg':'ok'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            try:
                res=models.Countdown.objects.filter(id=id).update(pid=pid,downdate=downdate,downtxt=downtxt,color_downdate=color_downdate,color_downtxt=color_downtxt,color_theme=color_theme)
                if res>0:
                    data={'msg':'ok'}
            except:
                data={'msg':'修改失败'}
        return HttpResponse(json.dumps(data), content_type='application/json')


def up_head(request):
    """
    点击修改头像，跳转修改头像界面
    :param request:
    :return:
    """
    print("修改头像")
    return render(request,'edit_user_photo/edit_user_photo.html')

@csrf_exempt
def save_user_photo(request):
    if request.method == 'POST':
        uid=request.session.get('id')
        print(uid)

        file = request.FILES.get('file') #获取前端上传的文件
        print(file.name)
        fix = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')+'1' #给文件加前缀防止文件名重复
        print(fix)
        #202012041458598871471
        newName=fix+'.'+str(file.name).split('.')[1]
        user=models.User.objects.filter(id=uid).first()
        user.photo_name=newName
        user.photo_file='photos/'+newName
        user.save()
        rootname = settings.MEDIA_ROOT+ "\\" +"photos/"+ newName
        print(rootname)
        with open(rootname,'wb') as pic:
                    for c in file.chunks():
                        pic.write(c)
        pic.close()
        data={}
        data['msg']="ok"
        data['img']='photos/'+newName
        return HttpResponse(json.dumps(data), content_type='application/json')

def upuserInfo(request):
    '''
    转发用户信息，编辑时用
    :param request:
    :return:
    '''
    pid=request.session.get("id")
    user_mode=models.User.objects.filter(id=pid)
    user_mode=serializers.serialize("json",user_mode)
    # user=user['fields']
    # print(type(user))
    user_mode=json.loads(user_mode)
    print(user_mode)
    user=user_mode[0]['fields']
    id=user_mode[0]['pk']
    user['id']=id
    user_list=['男','女','保密']
    print(user)
    return render(request, 'edit_userInfo/edit_user_info.html',{"user":user,"user_list":user_list})

@csrf_exempt
def update_userinfo(request):
    '''
    更新用户信息
    :param request:
    :return:
    '''
    id=request.POST.get('id')
    username=request.POST.get('username')
    email=request.POST.get('email')
    sex=request.POST.get('sex')
    print(id,username,sex,email)
    data={}
    try:
        models.User.objects.filter(id=id).update(username=username,sex=sex,email=email)
        data['msg']="ok"
    except:
        data['msg']='更新失败！'
    return HttpResponse(json.dumps(data), content_type='application/json')

