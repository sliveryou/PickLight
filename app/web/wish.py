# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

from . import web
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, flash

from app.models.base import db
from app.models.wish import Wish
from app.models.gift import Gift

from app.view_models.wish import MyWishes
from app.libs.email import send_email


@web.route('/my/wishes')
@login_required
def my_wish():
    '''处理心愿清单页面。'''
    uid = current_user.id
    wishes_of_mine = Wish.get_user_wishes(uid)
    isbn_list = [wish.isbn for wish in wishes_of_mine]
    gift_count_list = Wish.get_gift_counts(isbn_list)
    view_model = MyWishes(wishes_of_mine, gift_count_list)
    return render_template('web/my_wishes.html', wishes=view_model.wishes)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    '''将想要获得的书籍添加到心愿清单。'''
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            db.session.add(wish)
    else:
        flash('这本书已添加至你的赠送清单或已存在于你的心愿清单，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
@login_required
def satisfy_wish(wid):
    '''发起赠送礼物请求。'''
    wish = Wish.query.get_or_404(wid)
    gift = Gift.query.filter_by(uid=current_user.id, isbn=wish.isbn).first()
    if not gift:
        flash('你还没有上传此书，'
              '请点击“加入到赠送清单”添加此书。添加前，请确保自己可以赠送此书')
    else:
        send_email(wish.user.email,
                  '有人想送你一本书', 'email/satisify_wish.html',
                   wish=wish, gift=gift)
        flash('已向 Ta 发送了一封邮件，如果 Ta 愿意接受你的赠送，你将收到一个时光漂流邀请')
    return redirect(url_for('web.book_detail', isbn=wish.isbn))


@web.route('/wish/book/<isbn>/redraw')
@login_required
def redraw_from_wish(isbn):
    '''从心愿清单撤销心愿。'''
    wish = Wish.query.filter_by(isbn=isbn, uid=current_user.id, launched=False).first_or_404()
    with db.auto_commit():
        wish.delete()
    return redirect(url_for('web.my_wish'))
