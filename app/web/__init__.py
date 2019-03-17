# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

from flask import Blueprint

# 使用 web 蓝图集中路由
web = Blueprint('web', __name__, template_folder='templates')

from app.web import auth
from app.web import drift
from app.web import book
from app.web import main
from app.web import gift
from app.web import wish
from app.web import note
from app.web import errors

