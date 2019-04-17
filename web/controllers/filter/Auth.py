# encoding : utf-8
from flask import request,g,redirect
from application import app
import re
from common.models.User import User
from common.libs.UrlManager import UrlManager
from common.libs.Utils import Utils

@app.before_request
def auth_login():
    ignore_urls = app.config['IGNORE_URLS']
    ignore_check_login_urls = app.config['IGNORE_CHECK_LOGIN_URLS']
    path = request.path

    # 如果是静态文件就不要查询用户信息了
    pattern = re.compile('%s' % "|".join(ignore_check_login_urls))
    if pattern.match(path):
        return

    # 判断是否为登陆页面
    pattern = re.compile('%s' % "|".join(ignore_urls))
    if pattern.match(path):
        return

    # 判断用户是否登陆
    user_info = check_login()
    if user_info:
        g.current_user = user_info

    if not user_info:
        return redirect(UrlManager.buildUrl('/user/login'))
    return


"""
判断用户是否已经登录
"""
def check_login():
    # 获取cookie
    cookies = request.cookies
    auth_cookie = cookies[app.config['AUTH_COOKIE_NAME']] if app.config['AUTH_COOKIE_NAME'] in cookies else None
    if auth_cookie is None:
        return False

    auth_info = auth_cookie.split('#')
    if len(auth_info) != 2:
        return False
    try:
        user_info = User.query.filter_by(uid=auth_info[1]).first()
    except Exception:
        return False

    if user_info is None:
        return False

    if auth_info[0] != Utils.geneAuthCode(user_info):
        return False

    return user_info