from django.contrib import admin
from .models import Test,User,Overtime,Countdown
# Register your models here.
admin.site.register([Test,User,Overtime,Countdown])