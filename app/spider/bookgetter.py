# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

from app.libs.httper import Http
from flask import current_app


class BookGetter:
    # 请求指定 API 获取书籍信息
    # isbn_url = 'https://api.douban.com/v2/book/isbn/{}'
    # keyword_url = 'https://api.douban.com/v2/book/search?q={}&count={}&start={}'
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        # 根据 isbn 请求 API
        url = self.isbn_url.format(isbn)
        result = Http.get(url)
        self.__fill_single(result)

    def search_by_keyword(self, keyword, page=1):
        # 根据 keyword 请求 API
        url = self.keyword_url.format(keyword, current_app.config['PER_PAGE'],  # 从配置文件导入每页的信息条数
                                      self.calculate_start(page))
        result = Http.get(url)
        self.__fill_collection(result)

    @property
    def first(self):
        return self.books[0] if self.total >= 1 else None

    def calculate_start(self, page):
        return (page - 1) * current_app.config['PER_PAGE']

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self, data):
        if data:
            self.total = data['total']
            self.books = data['books']
