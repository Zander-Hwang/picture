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
    file = FileUtils()
    info = file.write_readme('./archivist/liberty.md', 'https://cdn.jsdelivr.net/gh/Zander-Hwang/picture/file/wallpaper/004217-1703695337d468.jpg', '004217-1703695337d468')
    info = file.write_readme('./archivist/liberty.md', 'https://cdn.jsdelivr.net/gh/Zander-Hwang/picture/file/wallpaper/010813rQ3kM.jpg', '010813rQ3kM')
    info = file.write_readme('./archivist/liberty.md', 'https://cdn.jsdelivr.net/gh/Zander-Hwang/picture/file/wallpaper/114426kZcDJ.jpg', '114426kZcDJ')
    info = file.write_readme('./archivist/liberty.md', 'https://cdn.jsdelivr.net/gh/Zander-Hwang/picture/file/wallpaper/183124HCqLE.jpg', '183124HCqLE')
    info = file.write_readme('./archivist/liberty.md', 'https://cdn.jsdelivr.net/gh/Zander-Hwang/picture/file/wallpaper/wallhaven-85por2.jpg', 'wallhaven-85por2')
    # print(info)
