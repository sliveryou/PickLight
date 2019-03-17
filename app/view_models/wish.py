# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

from .book import BookViewModel


class MyWishes:
    # 心愿清单心愿列表的视图模型
    def __init__(self, wishes_of_mine, gift_count_list):
        self.wishes = []
        self.__wishes_of_mine = wishes_of_mine
        self.__gift_count_list = gift_count_list
        self.wishes = self.__parse()

    def __parse(self):
        # 解析传入的 wish 和 gift_count
        temp_wishes = []
        for wish in self.__wishes_of_mine:
            my_wish = self.__matching(wish)
            temp_wishes.append(my_wish)
        return temp_wishes

    def __matching(self, wish):
        count = 0
        for gift_count in self.__gift_count_list:
            if wish.isbn == gift_count['isbn']:
                count = gift_count['count']
        my_wish = {'id': wish.id, 'book': BookViewModel(wish.book), 'gifts_count': count}
        return my_wish
