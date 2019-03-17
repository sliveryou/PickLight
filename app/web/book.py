# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

from . import web
from flask import render_template, request, flash
from flask_login import current_user

from app.libs.helper import is_isbn_or_key
from app.spider.bookgetter import BookGetter
from app.forms.book import SearchForm

from app.view_models.book import BookCollection, BookViewModel
from app.view_models.trade import TradeInfo

from app.models.gift import Gift
from app.models.wish import Wish


@web.route('/book/search', methods=['GET'])
def search():
    '''书籍搜索视图函数。'''
    form = SearchForm(request.args)  # 提交网页的 GET 请求参数
    books = BookCollection()
    if form.validate():  # 使用 wtforms 验证输入是否正确
        q = form.q.data.strip()
        page = form.page.data
        bookgetter = BookGetter()
        isbn_or_key = is_isbn_or_key(q)  # 判断 q 是关键字还是 isbn

        if isbn_or_key == 'isbn':
            bookgetter.search_by_isbn(q)
        else:
            bookgetter.search_by_keyword(q, page)

        books.fill(bookgetter, q)
        '''
        # 返回 books 对象中所有变量的字典形式
        import json
        return json.dumps(books, default=lambda x: x.__dict__,
                          ensure_ascii=False, indent=4), 200, {'content-type': 'application/json'}
        '''
    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
        # return jsonify(form.errors)
    return render_template('web/search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    '''书籍详情页面。'''
    # 一本书对于一个用户的两种不同状态
    has_in_gifts = False  # 是否在礼物清单
    has_in_wishes = False  # 是否在心愿清单

    # 获取书籍详情数据
    bookgetter = BookGetter()
    bookgetter.search_by_isbn(isbn)
    book = BookViewModel(bookgetter.first)

    # 用户登录时
    if current_user.is_authenticated:
        # 查询这本书是否在用户的赠送清单
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_gifts = True
        # 查询这本书是否在用户的心愿清单
        elif Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_wishes = True

    # 在数据库中寻找对应的礼物或心愿
    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    # 视图模型对原始数据进行转化
    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)

    return render_template('web/book_detail.html', book=book,
                           wishes=trade_wishes_model, gifts=trade_gifts_model,
                           has_in_wishes=has_in_wishes, has_in_gifts=has_in_gifts)
