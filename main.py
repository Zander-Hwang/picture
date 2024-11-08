"""
# -*- coding: utf-8 -*-
@Project: picture
@File: main.py
@Author: zander
@Date: 2024/10/17 14:33
@Software: PyCharm
@Description: 入口文件
"""
import os
from src.local import LocalGit
from src.remote import RemoteReq

if __name__ == '__main__':
    # 创建请求日志文件夹
    if 'log' not in os.listdir('.'):
        os.mkdir(r"./log")
    LocalGit()
    RemoteReq()
