# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

import requests


class Http:
    @staticmethod
    def get(url, return_json=True):
        '''通过 GET 请求访问一个 URL 并返回请求结果（默认为 JSON 形式）。'''
        r = requests.get(url)
        if r.status_code != 200:  # 如果状态码不为200就返回一个空字典或者空字符串
            return {} if return_json else ''
        return r.json() if return_json else r.text  # 状态码为200就返回json格式的结果
