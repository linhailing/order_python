# encoding: utf-8
from flask import Blueprint, request, jsonify
from common.libs.Helpers import ops_render,getCurrentDate
from common.libs.Utils import Utils
from common.models.User import User
from application import app, db

route_account = Blueprint('account_page', __name__)

@route_account.route('/index')
def index():
    resp_data = {}
    list = User.query.order_by( User.uid.desc() ).all()

    resp_data['list'] = list
    return ops_render('account/index.html', resp_data)


@route_account.route('/info')
def info():
    return ops_render('/account/info.html')


@route_account.route('/set', methods = ["GET","POST"])
def set():
    default_pwd = '******'
    if request.method == "GET":
        resp_data = {}
        req = request.args
        uid = int(req.get("id", 0))
        info = None
        if uid:
            info = User.query.filter_by(uid=uid).first()
        resp_data['info'] = info
        return ops_render('/account/set.html',resp_data)

    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else 0
    nickname = req['nickname'] if 'nickname' in req else None
    mobile = req['mobile'] if 'mobile' in req else None
    email = req['email'] if 'email' in req else None
    login_name = req['login_name'] if 'login_name' in req else None
    login_pwd = req['login_pwd'] if 'login_pwd' in req else None

    if nickname is None or len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的姓名~~"
        return jsonify(resp)

    if mobile is None or len(mobile) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的手机号码~~"
        return jsonify(resp)

    if email is None or len(email) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的邮箱~~"
        return jsonify(resp)

    if login_name is None or len(login_name) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的登录用户名~~"
        return jsonify(resp)

    if login_pwd is None or len(email) < 6:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的登录密码~~"
        return jsonify(resp)

    has_in = User.query.filter(User.login_name == login_name, User.uid != id).first()
    if has_in:
        resp['code'] = -1
        resp['msg'] = "该登录名已存在，请换一个试试~~"
        return jsonify(resp)

    user_info = User.query.filter_by(uid=id).first()
    if user_info:
        model_user = user_info
    else:
        model_user = User()
        model_user.created_time = getCurrentDate()
        model_user.login_salt = Utils.geneSalt()

    model_user.nickname = nickname
    model_user.mobile = mobile
    model_user.email = email
    model_user.login_name = login_name
    if login_pwd != default_pwd:
        if user_info and user_info.uid == 1:
            resp['code'] = -1
            resp['msg'] = "该用户是演示账号，不准修改密码和登录用户名~~"
            return jsonify(resp)

        model_user.login_pwd = Utils.getPassWord(login_pwd, model_user.login_salt)

    model_user.updated_time = getCurrentDate()
    db.session.add(model_user)
    db.session.commit()
    return jsonify(resp)




