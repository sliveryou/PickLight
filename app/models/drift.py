# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

from app.models.base import Base
from app.libs.enums import PendingStatus
from sqlalchemy import Column, SmallInteger, Integer, String


class Drift(Base):
    # 记录一次具体的交易信息
    id = Column(Integer, primary_key=True)

    # 邮寄信息
    recipient_name = Column(String(20), nullable=False)  # 收件人姓名
    address = Column(String(100), nullable=False)  # 收件人地址
    message = Column(String(200))  # 留言
    mobile = Column(String(20), nullable=False)  # 手机号码

    # 书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))

    # 请求者信息
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))

    # 赠送者信息
    gift_id = Column(Integer)
    gifter_id = Column(Integer)
    gifter_nickname = Column(String(20))

    _pending = Column('pending', SmallInteger, default=1)

    @property
    def pending(self):
        # 返回枚举类型对应的状态
        return PendingStatus(self._pending)

    @pending.setter
    def pending(self, status):
        # 赋值时需要赋值枚举状态对应的数值
        self._pending = status.value
