# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

from . import web
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, current_app, flash

from app.models.base import db
from app.models.gift import Gift
from app.models.drift import Drift

from app.view_models.gift import MyGifts
from app.libs.enums import PendingStatus


@web.route('/my/gifts')
@login_required
def my_gifts():
    '''处理礼物清单页面。'''
    uid = current_user.id
    gifts_of_mine = Gift.get_user_gifts(uid)
    isbn_list = [gift.isbn for gift in gifts_of_mine]
    wish_count_list = Gift.get_wish_counts(isbn_list)
    view_model = MyGifts(gifts_of_mine, wish_count_list)
    return render_template('web/my_gifts.html', gifts=view_model.gifts)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    '''将想要赠送的书籍添加到礼物清单。'''
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
    else:
        flash('这本书已添加至你的赠送清单或已存在于你的心愿清单，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    '''从礼物清单撤销礼物。'''
    gift = Gift.query.filter_by(id=gid, uid=current_user.id, launched=False).first_or_404()
    drift = Drift.query.filter_by(
        gift_id=gid, pending=PendingStatus.Waiting).first()
    if drift:
        flash('这个礼物正处于交易状态，请先完成这个交易哦')
    else:
        with db.auto_commit():
            current_user.beans -= current_app.config['BEANS_UPLOAD_ONE_BOOK']
            gift.delete()
    return redirect(url_for('web.my_gifts'))
