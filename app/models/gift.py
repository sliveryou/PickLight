# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

from flask import current_app
from sqlalchemy import Integer, String, Column, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship

from app.models.base import Base, db
from app.spider.bookgetter import BookGetter


class Gift(Base):
    __tablename__ = 'gift'

    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    isbn = Column(String(13), nullable=False)
    launched = Column(Boolean, default=False)

    def is_yourself_gift(self, uid):
        # 根据当前礼物的赠送者 uid 号是否为传入的当前用户的 uid 号来判断这个礼物是不是当前用户所拥有的
        return True if self.uid == uid else False

    @classmethod
    def get_user_gifts(cls, uid):
        # 得到当前 user 的礼物清单（默认按时间倒序排列）
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
            desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        from app.models.wish import Wish
        # 根据传入的一组 isbn，到 Wish 表中检索出相应的礼物，并且计算出某个礼物的 Wish 心愿数量
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(
            Wish.isbn).all()
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    @property
    def book(self):
        # 返回当前礼物对应的书籍对象
        bookgetter = BookGetter()
        bookgetter.search_by_isbn(self.isbn)
        return bookgetter.first

    @classmethod
    def recent(cls):
        # 返回前三十个不重复的礼物清单，结果按照添加时间新旧进行排序

        # recent_gift = Gift.query.filter_by(
        #     launched=False).group_by(
        #     Gift.isbn).order_by(
        #     desc(Gift.create_time)).limit(
        #     current_app.config['RECENT_BOOK_COUNT']).distinct().all()

        recent_gift = Gift.query.filter_by(
            launched=False).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()

        return recent_gift
