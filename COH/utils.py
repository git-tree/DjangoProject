# -*- coding: utf-8 -*-

'''
@Time    : 2021/1/4 11:05
@Author  : 崔术森
@FileName: utils.py
@Software: PyCharm
 
'''
import datetime
def dateStr2Date(datestr):
    dateTime_p = datetime.datetime.strptime(datestr,'%Y-%m-%d %H:%M:%S')
    return dateTime_p

if __name__=='__main__':
    print(dateStr2Date('2020-12-12 18:11:20'))