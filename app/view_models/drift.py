# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

from app.libs.enums import PendingStatus


class DriftViewModel:
    # 对一份订单的数据呈现
    def __init__(self, drift, current_user_id):
        self.data = {}

        self.data = self.__parse(drift, current_user_id)

    @staticmethod
    def requester_or_gifter(drift, current_user_id):
        # 判断当前用户是赠送者还是请求者
        you_are = 'requester' if drift.requester_id == current_user_id else 'gifter'
        return you_are

    def __parse(self, drift, current_user_id):
        # 解析交易数据
        you_are = self.requester_or_gifter(drift, current_user_id)
        pending_status = PendingStatus.pending_str(drift.pending, you_are)  # 得到相应状态描述

        return {
            'you_are': you_are,
            'drift_id': drift.id,
            'book_title': drift.book_title,
            'book_author': drift.book_author,
            'book_img': drift.book_img,
            'date': drift.create_datetime.strftime('%Y-%m-%d'),
            'operator': drift.requester_nickname if you_are != 'requester' else drift.gifter_nickname,
            'message': drift.message,
            'address': drift.address,
            'status_str': pending_status,
            'recipient_name': drift.recipient_name,
            'mobile': drift.mobile,
            'status': drift.pending
        }


class DriftCollection:
    def __init__(self, drifts, current_user_id):
        self.data = []

        self.data = self.__parse(drifts, current_user_id)

    def __parse(self, drifts, current_user_id):
        return [DriftViewModel(drift, current_user_id).data for drift in drifts]
