""" 
# -*- coding: utf-8 -*-
@File: fetchutils
@Author: zander
@Date: 2024/11/3 22:54
@Software: PyCharm
@Description: 请求方法封装
"""
import os
import requests
from .useragent import UserAgent
from .dateutils import DateUtils


class FetchUtils:
    def __init__(self, method, url, **args):
        self.request(method=method, url=url, **args)

    @staticmethod
    def request(method, url, **args):
        try:
            # 创建请求日志文件夹
            if 'log' not in os.listdir('.'):
                os.mkdir(r"./log")
            if 'headers' not in args:
                headers = {'User-Agent': UserAgent().get_user_agent()}
            else:
                headers = args.pop('headers')
            response = requests.request(method=method, url=url, headers=headers, **args)
            return response
        except Exception as e:
            err_dic = {'url': url}
            err_dic.update(args)
            print("请求失败：%s\n" % err_dic)
            with open(r"./log/error.log", 'a', encoding='utf-8') as f:
                f.write("请求失败：%s【%s】%s \n" % (e, err_dic, DateUtils.formattime()))
            f.close()

    @staticmethod
    def get(url, params=None, **args):
        return FetchUtils.request('get', url=url, params=params, **args)
