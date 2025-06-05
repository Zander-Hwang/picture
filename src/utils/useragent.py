""" 
# -*- coding: utf-8 -*-
@File: useragent
@Author: zander
@Date: 2024/11/4 15:17
@Software: PyCharm
@Description: 获取userAgent列表
"""
import glob
from lxml import etree
import requests
from .dateutils import DateUtils
import os
import random


class UserAgent:
    fileAbsPath = os.path.dirname(__file__)
    url = 'http://useragentstring.com/pages/useragentstring.php?typ=Browser'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (compatible; ABrowse 0.4; Syllable)'
    }

    def __request_user_agent(self):
        try:
            # 创建请求日志文件夹
            if 'log' not in os.listdir('.'):
                os.mkdir(r"./log")
            response = requests.get(self.url, self.headers, timeout=60)
            response.encoding = response.apparent_encoding
            tree = etree.HTML(response.text)
            browsers = tree.xpath('//ul/li/a/text()')
            browsers = [browser for browser in browsers if len(browser) > 80]
            path = r'%s/resource/userAgent_%s.txt' % (self.fileAbsPath, int(round(DateUtils.time() * 1000)))
            with open(path, 'w', encoding='utf-8') as f:
                f.write("\n".join(browsers))
            f.close()

        except Exception as e:
            print("未知错误 %s\n" % e)
            with open(r"./log/request_error.log", 'a', encoding='utf-8') as f:
                f.write("未知错误 %s\n" % e)
            f.close()

    def get_user_agent(self):
        files = glob.glob(r'%s/resource/*userAgent*' % self.fileAbsPath)
        if len(files) == 0:
            self.__request_user_agent()
        filenames = [files[i] for i in range(len(files))][0]
        timer = int(round(DateUtils.time() * 1000))
        if timer - int(filenames[-17:-4]) > (365 * 24 * 60 * 60 * 1000):
            os.remove(filenames)
            self.__request_user_agent()
        with open(filenames, "r") as f:
            text = f.read()
            useragent = text.split("\n")
        f.close()
        if len(useragent) == 0:
            useragent = ['Mozilla/5.0 (compatible; ABrowse 0.4; Syllable)']
        return random.choice(useragent)
