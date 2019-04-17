# encoding: utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
import os


class Application(Flask):
    def __init__(self, import_name, template_folder=None,static_url_path=None,root_path=None,static_folder=None):
        super(Application, self).__init__(import_name,template_folder=template_folder,static_url_path=static_url_path,root_path=root_path,static_folder=static_folder)
        self.config.from_pyfile('config/base_setting.py')
        db.init_app(self)

db = SQLAlchemy()

app = Application(__name__,template_folder=os.getcwd() + '/web/templates/',root_path = os.getcwd())
manager = Manager(app)

from common.libs.UrlManager import UrlManager

app.add_template_global(UrlManager.buildUrl, 'buildUrl')
app.add_template_global(UrlManager.buildStaticUrl, 'buildStaticUrl')