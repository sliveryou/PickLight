# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

from . import web
from sqlalchemy import desc, or_
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, flash, request

from app.models.base import db
from app.models.gift import Gift
from app.models.wish import Wish
from app.models.drift import Drift
from app.models.user import User
from app.forms.book import DriftForm

from app.libs.email import send_email
from app.libs.enums import PendingStatus

from app.view_models.book import BookViewModel
from app.view_models.drift import DriftCollection


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    '''发起一次交易请求。'''
    current_gift = Gift.query.get_or_404(gid)

    # 防止用户自己向自己发起交易
    if current_gift.is_yourself_gift(current_user.id):
        flash('这本书是你自己的，不能向自己索要书籍喔~')
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))

    # 判断拾光豆等条件是否满足
    if not current_user.can_send_drift():
        return render_template('web/not_enough_beans.html', beans=current_user.beans)

    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        save_drift(form, current_gift)
        send_email(current_gift.user.email, '有人想要一本书', 'email/get_gift.html',
                   wisher=current_user, gift=current_gift)
        return redirect(url_for('web.pending'))

    gifter = current_gift.user.summary
    return render_template('web/drift.html', gifter=gifter,
                           user_beans=current_user.beans, form=form)


@web.route('/pending')
@login_required
def pending():
    '''处理时光漂流页面。'''
    # 查询自己身为请求者或赠送者的交易信息
    drifts = Drift.query.filter(
        or_(Drift.requester_id == current_user.id, Drift.gifter_id == current_user.id)).order_by(
        desc(Drift.create_time)
    ).all()

    view_model = DriftCollection(drifts, current_user.id)
    return render_template('web/pending.html', drifts=view_model.data)


@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    '''拒绝交易。'''
    with db.auto_commit():
        drift = Drift.query.filter_by(
            gifter_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Reject
        requester = User.query.get_or_404(drift.requester_id)
        requester.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    '''撤销交易。'''
    with db.auto_commit():
        drift = Drift.query.filter_by(
            requester_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Redraw
        current_user.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/mailed')
@login_required
def mailed_drift(did):
    '''表示书本已邮寄。'''
    with db.auto_commit():
        drift = Drift.query.filter_by(
            gifter_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Success

        # 对赠送者的奖励并记录寄出礼物的次数
        current_user.beans += 1
        current_user.send_counter += 1

        # 对请求者要记录他获得礼物的次数
        requester = User.query.filter_by(id=drift.requester_id).first()
        requester.receive_counter += 1

        # 将礼物标记为已赠送状态
        gift = Gift.query.filter_by(id=drift.gift_id).first_or_404()
        gift.launched = True

        # 将心愿标记为已实现状态
        Wish.query.filter_by(isbn=drift.isbn, uid=drift.requester_id,
                             launched=False).update({Wish.launched: True})
    return redirect(url_for('web.pending'))


def save_drift(drift_form, current_gift):
    '''存储交易相关信息到数据库中。'''
    with db.auto_commit():
        drift = Drift()
        # 将表单中的信息赋值到 drift 对象中
        drift_form.populate_obj(drift)

        # 添加请求者信息
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname

        # 添加赠送者信息
        drift.gift_id = current_gift.id
        drift.gifter_id = current_gift.user.id
        drift.gifter_nickname = current_gift.user.nickname

        book = BookViewModel(current_gift.book)

        # 添加书籍信息
        drift.isbn = book.isbn
        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image

        current_user.beans -= 1

        db.session.add(drift)
