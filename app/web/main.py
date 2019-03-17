# -*- coding: UTF-8 -*-
from . import web
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from app.models.user import User
from app.models.gift import Gift
from app.view_models.book import BookViewModel


@web.route('/')
def index():
    '''处理最近上传页面。'''
    recent_gifts = Gift.recent()
    books = [BookViewModel(gift.book) for gift in recent_gifts]
    return render_template('web/index.html', recent=books)


@web.route('/personal')
@login_required
def personal_center():
    '''处理个人中心页面。'''
    return render_template('web/personal.html', user=current_user.summary)


@web.route('/user/<nickname>')
@login_required
def user_detail(nickname):
    '''处理用户资料页面。'''
    user = User.query.filter_by(nickname=nickname).first_or_404()
    return render_template('web/user_detail.html', user=user.summary)
