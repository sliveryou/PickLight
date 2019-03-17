# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

from sqlalchemy import Integer, String, Column, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship

from app.models.base import Base, db
from app.spider.bookgetter import BookGetter


class Wish(Base):
    __tablename__ = 'wish'

    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    isbn = Column(String(13), nullable=False)
    launched = Column(Boolean, default=False)

    @classmethod
    def get_user_wishes(cls, uid):
        # 得到当前 user 的心愿清单
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(
            desc(Wish.create_time)).all()
        return wishes

    @classmethod
    def get_gift_counts(cls, isbn_list):
        from app.models.gift import Gift
        # 根据传入的一组 isbn，到 Gift 表中检索出相应的礼物，并且计算出某个礼物的赠送数量
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False,
            Gift.isbn.in_(isbn_list),
            Gift.status == 1).group_by(
            Gift.isbn).all()
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    @property
    def book(self):
        # 返回当前心愿对应的书籍对象
        bookgetter = BookGetter()
        bookgetter.search_by_isbn(self.isbn)
        return bookgetter.first
