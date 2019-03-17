# -*- coding: UTF-8 -*-
import os

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://用户名:密码@IP地址(如127.0.0.1):端口号(如3306)/数据库(如book)'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'XXXXXXXX' # 随机字符串即可

MAIL_DEBUG = False
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = os.environ.get('MAIL_USERNAME') # 关键信息可记录于 Shell 的环境变量中
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') # 如 zsh 中，在 .zshrc 文件里加入 
                                                # export MAIL_USERNAME='邮箱'
                                                # export MAIL_PASSWORD='校验码' 
MAIL_SUBJECT_PREFIX = '[拾光]'
MAIL_SENDER = '拾光 <picklight@sliveryou.cn>'