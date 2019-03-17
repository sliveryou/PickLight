# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

from datetime import datetime
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, SmallInteger, Integer


class SQLAlchemy(_SQLAlchemy):
    # 创建 _SQLAlchemy 的子类
    @contextmanager
    def auto_commit(self):
        # 创建上下文环境的 enter 和 exit 方法，实现自动 commit
        try:
            yield
            self.session.commit()
        except Exception as e:
            # 数据库对象事物回滚
            self.session.rollback()
            raise e


class Query(BaseQuery):
    # 继承 BaseQuery，重写 filter_by 方法
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        # super 返回当前类的基类：第一个参数表示当前类，第二个参数表示当前实例
        return super(Query, self).filter_by(**kwargs)


# 传递已经改写过的继承 BaseQuery 的 Query 对象
db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    __abstract__ = True
    status = Column(SmallInteger, default=1)  # 状态标识：1代表存在，0代表已删除
    create_time = Column('create_time', Integer)

    def __init__(self):
        # 默认在对象建立时添加创建时间戳
        self.create_time = int(datetime.now().timestamp())

    # 动态赋值
    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def delete(self):
        self.status = 0
