# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

def is_isbn_or_key(word):
    '''判断是 isbn 搜索还是关键字搜索，并返回判断的结果。'''
    if len(word) == 13 and word.isdigit():
        # 判断 isbn13
        return 'isbn'
    elif '-' in word and len(word.replace('-', '')) == 10:
        # 判断 isbn10
        return 'isbn'
    return 'keyword'


def get_isbn(data):
    '''传递的是一个字典类型的 data，获取其中包含的 isbn 信息。'''
    isbn = data.get('isbn')
    if not isbn:
        isbn = data.get('isbn13')
        if not isbn:
            isbn = data.get('isbn10')
    return isbn
