# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

from app.libs.helper import get_isbn


class BookViewModel:
    def __init__(self, book):
        # 将从 API 得到的书籍数据处理修正一番
        self.title = book['title']
        self.author = '、'.join(book['author']) or '未知'  # author 是一个列表，可以先拼接成一个字符串
        self.binding = book['binding'] or '未知'
        self.publisher = book['publisher'] or '未知'
        self.image = book['image']
        self.price = '￥' + book['price'] if book['price'] else '未知'
        self.isbn = get_isbn(book)
        self.pubdate = book['pubdate'] or '未知'
        self.pages = book['pages'] or '未知'
        self.summary = book['summary'].replace(r'\n', '') if book['summary'] else '暂无相关介绍。'

    @property
    def intro(self):
        # 得到关于书籍的作者、出版社和价格的介绍
        intros = [message for message in [self.author, self.publisher, self.price] if message]
        # 返回字符分隔后的最终结果
        return ' / '.join(intros)


class BookCollection:
    # 包含一系列 BookViewModel 的书籍列表
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, bookgetter, keyword):
        self.total = bookgetter.total
        self.books = [BookViewModel(book) for book in bookgetter.books]
        self.keyword = keyword


'''
class BookViewModel:
    @classmethod
    def package_single(cls, data, keyword):
        # 这里的 data 传递的是一个字典
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = 1
            returned['books'] = [cls.__cut_book_data(data)]
        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        # 这里的 data[books] 是一个包含很多字典的列表
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = data['total']
            returned['books'] = [cls.__cut_book_data(book) for book in data['books']]
        return returned

    @classmethod
    def __cut_book_data(cls, data):
        # 将 API 得到的数据处理修正一番
        book = {
            'title': data['title'],
            'publisher': data['publisher'],
            'pages': data['pages'] or '',
            'author': '、'.join(data['author']),  # author 是一个列表，可以先拼接成一个字符串
            'price': data['price'],
            'summary': data['summary'] or '',
            'image': data['image']
        }
        return book
'''
