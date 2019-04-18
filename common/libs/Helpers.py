# -*- coding: utf-8 -*-
# @Time    : 2019-04-17 20:51
# @Author  : henry lin
from flask import g, render_template
import datetime

'''
统一渲染页面的方法
'''

def ops_render(template, context={}):
    if 'current_user' in g:
        context['current_user'] = g.current_user
    return render_template(template, **context)


'''
获取当前时间
'''
def getCurrentDate( format = "%Y-%m-%d %H:%M:%S"):
    #return datetime.datetime.now().strftime( format )
    return datetime.datetime.now()

'''
获取格式化的时间
'''
def getFormatDate( date = None ,format = "%Y-%m-%d %H:%M:%S" ):
    if date is None:
        date = datetime.datetime.now()
    return date.strftime( format )


