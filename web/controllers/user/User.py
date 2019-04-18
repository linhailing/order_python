# encoding: utf-8
from flask import Blueprint, request, jsonify,make_response, redirect, g
import json
from common.models.User import User
from common.libs.Utils import Utils
from application import app, db
from common.libs.Helpers import *
from common.libs.UrlManager import UrlManager

route_user = Blueprint('user_page', __name__)


@route_user.route('/login', methods=['POST','GET'])
def login():
    if request.method == "GET":
        return render_template('/user/login.html')
    resp = {'code': 200, 'msg': '登录成功~~', 'data': {}}
    req = request.values
    login_name = req['login_name'] if 'login_name' in req else None
    login_pwd = req['login_pwd'] if 'login_pwd' in req else None

    if login_name is None or len(login_name) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入正确的用户名'
        return jsonify(resp)

    if login_pwd is None or len(login_pwd) < 1:
        resp['msg'] = '请输入正确的用户mim'
        return jsonify(resp)

    user_info = User.query.filter_by(login_name=login_name).first()
    if user_info is None:
        resp['code'] = -1
        resp['msg'] = '请输入正确的用户名或密码'
        return jsonify(resp)

    if user_info.login_pwd != Utils.getPassWord(login_pwd, user_info.login_salt):
        resp['code'] = -1
        resp['msg'] = Utils.getPassWord(login_pwd, user_info.login_salt) +" || " + user_info.login_pwd
        return jsonify(resp)

    response = make_response(json.dumps(resp))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'],"%s#%s"%(Utils.geneAuthCode(user_info), user_info.uid))
    return response

@route_user.route('/edit', methods=['POST', 'GET'])
def edit():
    if request.method == "GET":
        return ops_render('/user/edit.html')
    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values
    name = req['name'] if 'name' in req else None
    email = req['email'] if 'email' in req else None
    if name is None or len(name) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入正确的用户名'
        return jsonify(resp)
    if email is None or len(email) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入正确的邮箱'
        return jsonify(resp)
    user_info = g.current_user
    user_info.login_name = name
    user_info.email = email
    db.session.add(user_info)
    db.session.commit()
    return jsonify(resp)

@route_user.route('/reset-pwd', methods = ["POST", "GET"])
def reset_pwd():
    if request.method == "GET":
        return ops_render('/user/reset_pwd.html')
    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values
    old_password = req['old_password'] if 'old_password' in req else None
    new_password = req['new_password'] if 'new_password' in req else None
    if old_password is None or len(old_password) < 6:
        resp['code'] = -1
        resp['msg'] = '请输入正确的旧密码'
        return jsonify(resp)
    if new_password is None or len(new_password) < 6:
        resp['code'] = -1
        resp['msg'] = '请输入正确的新密码'
        return jsonify(resp)

    if old_password == new_password:
        resp['code'] = -1
        resp['msg'] = "请重新输入一个吧，新密码和原密码不能相同哦~~"
        return jsonify(resp)

    user_info = g.current_user
    # if g.login_pwd != Utils.getPassWord(old_password,user_info.login_salt):
    #     resp['code'] = -1
    #     resp['msg'] = '请输入正确的旧密码'
    #     return jsonify(resp)
    user_info.login_pwd = Utils.getPassWord(new_password, user_info.login_salt)
    db.session.add(user_info)
    db.session.commit()
    return jsonify(resp)


@route_user.route('/logout')
def logout():
    response = make_response(redirect(UrlManager.buildUrl('/user/login')))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
    return response