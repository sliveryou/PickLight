# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

from app import mail
from threading import Thread
from flask import current_app, render_template
from flask_mail import Message


def send_async_email(app, msg):
    # 因为线程隔离的影响，所以需要创建应用上下文
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass


def send_email(to, subject, template, **kwargs):
    msg = Message(current_app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=current_app.config['MAIL_SENDER'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    # 获取真实的 app 对象
    app = current_app._get_current_object()
    # 异步发送电子邮件
    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()