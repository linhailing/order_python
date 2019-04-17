# encoding: utf-8
from flask import Blueprint,render_template, request, jsonify,make_response
import json
from common.models.User import User
from common.libs.Utils import Utils
from application import app

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