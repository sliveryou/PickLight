# -*- coding: UTF-8 -*-
from . import web
from flask import render_template

@web.app_errorhandler(404)
def page_not_found(error):
    '''处理404页面。'''
    return render_template('web/404.html'), 404