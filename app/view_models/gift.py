# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

from .book import BookViewModel


class MyGifts:
    # 赠送清单礼物列表的视图模型
    def __init__(self, gifts_of_mine, wish_count_list):
        self.gifts = []
        self.__gifts_of_mine = gifts_of_mine
        self.__wish_count_list = wish_count_list
        self.gifts = self.__parse()

    def __parse(self):
        # 解析传入的 gift 和 wish_count
        temp_gifts = []
        for gift in self.__gifts_of_mine:
            my_gift = self.__matching(gift)
            temp_gifts.append(my_gift)
        return temp_gifts

    def __matching(self, gift):
        count = 0
        for wish_count in self.__wish_count_list:
            if gift.isbn == wish_count['isbn']:
                count = wish_count['count']
        my_gift = {'id': gift.id, 'book': BookViewModel(gift.book), 'wishes_count': count}
        return my_gift
