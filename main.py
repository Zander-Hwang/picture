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
from src.fileUtils import FileUtils

if __name__ == '__main__':
    # 创建请求日志文件夹
    if 'log' not in os.listdir('.'):
        os.mkdir(r"./log")
    # file = FileUtils()
    # json = file.read_json('./archivist/wallpaper/liberty.json')
    # for i in json['2024-10']:
    #     file.write_readme('./archivist/liberty.md', i)
