"""
# -*- coding: utf-8 -*-
@File: urlparse
@Author: zander
@Date: 2024/10/20 11:16
@Software: PyCharm
@Description: 解析URL字符返回对应组成部分
"""
from urllib.parse import urlparse


class ParseUrl:
    url_dict = {}

    def __init__(self, url):
        self.url_dict = self.get_url_parts(url)

    @staticmethod
    def get_url_parts(url):
        result = urlparse(url)
        return {
            "scheme": result.scheme,
            "netloc": result.netloc,
            "path": result.path,
            "params": result.params,
            "query": result.query,
            "fragment": result.fragment
        }

    # 获取协议(例如:https)
    def get_scheme(self):
        return self.url_dict['scheme']

    # 获取网络位置，即主机和端口(例如:www.example.com)
    def get_netloc(self):
        return self.url_dict['netloc']

    # 获取路径(例如:/path/to/page)
    def get_path(self):
        return self.url_dict['path']

    # 获取参数(在 URL 中很少使用)
    def get_params(self):
        return self.url_dict['params']

    # 获取查询参数部分(例如:param1=valuel&param2=value2)
    def get_query(self):
        return self.url_dict['query']

    # 获取片段或锚点(例如:在页面内的某个位置)
    def get_fragment(self):
        return self.url_dict['fragment']
