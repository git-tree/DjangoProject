# -*- coding: utf-8 -*-

'''
@Time    : 2020/11/19 16:24
@Author  : 崔术森
@FileName: my_tags.py
@Software: PyCharm
 
'''
from django import template
from django.utils.safestring import mark_safe

register=template.Library()

@register.filter
def my_filter(v1,v2):
    return v1*v2

@register.simple_tag
def my_tag1(v1,v2,v3):
    return v1*v2*v3

@register.simple_tag
def my_html(v1,v2):
    tmp_html='<input type="text" id="%s" name="%s"/>'%(v1,v2)
    return tmp_html