from django.db import models
# 更新数据库的命令
# python manage.py makemigrations
# python manage.py migrate

# Create your models here.
class Test(models.Model):
    name=models.CharField(max_length=20)

class User(models.Model):
    """
    用户表，账号密码
    """
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    gender = (
        ('男', "男"),
        ('女', "女"),
    )
    sex = models.CharField(max_length=32, choices=gender, default="男")
    email = models.EmailField(unique=False,max_length=128,default='deer_cui@163.com')
    photo_name = models.CharField(max_length=64,default='default.jpg')
    photo_file = models.ImageField(upload_to='photos', default='photos/default.jpg')
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"

class Overtime(models.Model):
    """
    加班表
    """
    #哪一天
    day=models.CharField(max_length=128)
    #开始时间
    begintime=models.CharField(max_length=256)
    # 结束时间
    endtime=models.CharField(max_length=256)
    #时间
    hours=models.CharField(max_length=20)
    # pid是谁的数据，存登陆人id
    pid=models.CharField(max_length=20)
    # 第几周
    week=models.CharField(max_length=20)
    # 月份
    month=models.CharField(max_length=20)
    # 年份
    year=models.CharField(max_length=20)

class Countdown(models.Model):
    """
    存不同用户设置的倒计时
    """
    # 倒计时文本
    downtxt=models.CharField(max_length=256)
    # 倒计时时间
    downdate=models.CharField(max_length=128)
    # 谁设置的倒计时，存用户id
    pid=models.CharField(max_length=20)
    # 字体颜色
    color_downtxt=models.CharField(max_length=20,default='#1E9FFF')
    # 时间颜色
    color_downdate=models.CharField(max_length=20,default='#FF5722')
    # 主题颜色
    color_theme=models.CharField(max_length=20,default='#393D49')