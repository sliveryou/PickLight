# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

from enum import Enum


class PendingStatus(Enum):
    # 定义四种状态和对应的状态码，构建枚举类
    Waiting = 1
    Success = 2
    Reject = 3
    Redraw = 4

    @classmethod
    def pending_str(cls, status, key):
        # 交易状态映射到相应的显示字符
        key_map = {
            cls.Waiting: {
                'requester': '等待对方邮寄',
                'gifter': '等待你邮寄'
            },
            cls.Reject: {
                'requester': '对方已拒绝',
                'gifter': '你已拒绝'
            },
            cls.Redraw: {
                'requester': '你已撤销',
                'gifter': '对方已撤销'
            },
            cls.Success: {
                'requester': '对方已邮寄',
                'gifter': '你已邮寄，交易完成'
            }
        }
        return key_map[status][key]


if __name__ == '__main__':
    for i in range(1, 5):
        print(PendingStatus(i), PendingStatus(i).value)
