"""DjangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from COH import views,tests
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/',views.hello),
    path('tmp/',views.htmlout),
    path('loadpic/',views.loadpic),
    path('ex/',views.ex),
    path('addtest/',tests.testdb),
    path('get/',tests.testget),
    path('gethtml/',tests.gethtml),
    path('post/',tests.testpost),

    path('save_regist/',views.save_regist),
    path('checkexist/',views.checkexist),
    path('login/',views.login),
    path('index/',views.index),
    path('getuserInfo/',views.getuserInfo),
    path('logout/',views.logout),
    path('regist/',views.regist),
    path('up_head/',views.up_head),
    path('save_user_photo/',views.save_user_photo),
    path('counthours/',views.counthours),
    path('listall/',views.listall),
    path('getnowweek/',views.getnowweek),
    path('summonthhour/',views.summonthhour),
    path('delcount/',views.delcount),
    path('batchRemove/',views.batchRemove),
    path('sendemail/',views.sendemail),
    re_path(r'^edit/(.+)/$',views.edit),
    path('edit/',views.edit),
    path('update/',views.update),
    path('loaddown/',views.loaddown),
    path('editdown/',views.editdown),
    path('updateDown/',views.updateDown),
    path('sendsearchemail/',views.sendsearchemail),
    path('upuserInfo/',views.upuserInfo)









]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
