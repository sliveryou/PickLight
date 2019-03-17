# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from app.models.base import db

mail = Mail()
login_manger = LoginManager()


def create_app():
    app = Flask(__name__)

    # 读取配置文件
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')

    # 注册蓝图
    register_blueprint(app)

    # 注册 SQLAlchemy 模块
    db.init_app(app)
    db.create_all(app=app)

    # 注册 Login 模块
    login_manger.init_app(app)
    login_manger.login_view = 'web.login'
    login_manger.login_message = '请先登录或注册'

    # 注册 Mail 模块
    mail.init_app(app)

    return app


def register_blueprint(app):
    from app.web import web as web_blueprint
    app.register_blueprint(web_blueprint)
