# -*- coding: UTF-8 -*-
__author__ = 'Sliver'


class TradeInfo:
    # 书籍详情页面关于上传者和求书者的视图模型
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)

    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    def __map_to_trade(self, single):
        time = single.create_datetime.strftime('%Y-%m-%d') if single.create_datetime else '未知'
        # 转化礼物模型的部分数据
        return dict(
            user_name=single.user.nickname,
            time=time,
            id=single.id
        )
