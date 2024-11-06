""" 
# -*- coding: utf-8 -*-
@File: agentpool
@Author: zander
@Date: 2024/11/4 20:02
@Software: PyCharm
@Description: 获取代理IP
"""


class AgentPool:
    def __init__(self):
        self.url1 = 'http://www.nimadaili.com/gaoni/%d/'  # ip网址1 最大页数为2000 1-350
        self.url2 = 'https://www.89ip.cn/index_%d.html'  # ip网址2  最大页数为1-110
        self.url3 = 'https://www.kuaidaili.com/free/inha/%d/'  # ip网址3  最大页数1-4000
