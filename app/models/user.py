# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

from flask import current_app
from flask_login import UserMixin
from sqlalchemy import Integer, String, Column, Float, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.models.base import Base, db
from app.models.gift import Gift
from app.models.wish import Wish
from app.models.drift import Drift

from app import login_manger
from app.libs.helper import is_isbn_or_key
from app.libs.enums import PendingStatus
from app.spider.bookgetter import BookGetter


class User(UserMixin, Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    _password = Column('password', String(128), nullable=False)  # 将表字段命名为 password
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property
    def password(self):
        # 定义 password 属性
        return self._password

    @password.setter
    def password(self, raw):
        # 为 password 赋值时，进行加密操作
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        # 检测密码是否正确
        return check_password_hash(self._password, raw)

    def can_save_to_list(self, isbn):
        # 判断传入的 isbn 是否符合 isbn 规范
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        bookgetter = BookGetter()
        bookgetter.search_by_isbn(isbn)
        # 判断是否能在 API 中查询到这本书
        if not bookgetter.first:
            return False

        # 其他判断原则
        # 1.不允许一个用户同时赠送多本相同的书
        # 2.一个用户不可能同时成为赠送者和索要者

        # 既不在赠送清单，也不在心愿清单才能添加
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False

    def can_send_drift(self):
        # 判断当前用户的拾光豆是否符合要求
        if self.beans < 1:
            return False
        # 获得用户已赠送书籍数量
        success_gifts_count = Gift.query.filter_by(
            uid=self.id, launched=True).count()
        # 获得用户已获得书籍数量
        success_receive_count = Drift.query.filter_by(
            requester_id=self.id, pending=PendingStatus.Success).count()
        # 每索取两本书，自己要送出一本书
        return True if success_receive_count // 2 <= success_gifts_count else False

    @property
    def summary(self):
        # 得到用户的简介信息
        return {'nickname': self.nickname,
                'beans': self.beans,
                'email': self.email,
                'send_receive': str(self.send_counter) + '/' + str(self.receive_counter),
                'create_datetime': self.create_datetime.strftime('%Y-%m-%d')}

    def generate_token(self, expiration=600):
        # 添加随机字符串密钥和过期时间（默认为600s）生成令牌值
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')  # 将 bytes 类型的数据解码为 utf-8 格式的字符串

    @staticmethod
    def reset_password(token, new_password):
        # 解密 token 获得相关用户信息
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            # 如果 token 过期或者伪造时，返回 False
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)  # 返回指定主键对应的行
            user.password = new_password
        return True


@login_manger.user_loader
def get_user(uid):
    return User.query.get(int(uid))  # 返回指定主键对应的行
