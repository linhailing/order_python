# encoding: utf-8
SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1/food_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
AUTH_COOKIE_NAME = 'henry_food'
##过滤url
IGNORE_URLS = [
    "^/user/login"
]

IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico"
]