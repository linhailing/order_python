# -*- coding: utf-8 -*-
# @Time    : 2019-04-17 20:51
# @Author  : henry lin
from flask import g, render_template

'''
统一渲染页面的方法
'''

def ops_render(template, context={}):
    if 'current_user' in g:
        context['current_user'] = g.current_user
    return render_template(template, **context)


