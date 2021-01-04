from django.test import TestCase
from django.http import HttpResponse
from COH.models import Test
from django.shortcuts import render,redirect
# Create your tests here.

def testdb(req):
    test=Test(name="王雯雯")
    test.save()
    return HttpResponse("添加成功")

def gethtml(req):
    return render(req,'get.html')
def testget(request):
    request.encoding='utf-8'
    print(request)
    if 'g' in request.GET and request.GET['g']:
        msg='你搜索的内容为%s'%request.GET['g']
    else:
        msg='搜索为空'
    return HttpResponse(msg)

def testpost(request):
    ctx ={}
    if request.POST:
        ctx['rlt'] = request.POST['p']
    return render(request, "post.html", ctx)


