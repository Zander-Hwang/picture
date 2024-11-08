""" 
# -*- coding: utf-8 -*-
@Project: picture
@File: remote
@Author: zander
@Date: 2024/11/6 22:55
@Software: PyCharm
@Description: 远程图片 -- 爬虫
"""
from src.utils import DateUtils
from src.utils import FetchUtils
from src.operateJson import OperateJson


class RemoteReq:
    def __init__(self):
        self.get_bing_wallpaper()

    @staticmethod
    def get_bing_wallpaper():
        regions = ['zh-CN', 'en-US']
        api = 'https://global.bing.com/HPImageArchive.aspx?format=js&idx=0&n=9&pid=hp&FORM=BEHPTB&uhd=1&uhdwidth=3840&uhdheight=2160&setmkt={}&setlang=en'
        image_map = {
            'type': 'A',
            'url': '',
            'path': '',
            'path_en': '',
            'date': DateUtils.formattime('%Y-%m-%d'),
            'title': '',
            'title_en': '',
            'copyright': '',
            'copyright_en': ''
        }
        for i in regions:
            image = FetchUtils.get(api.format(i)).json()['images'][0]
            path = image['url'].replace('&rf=LaDigue_UHD.jpg&pid=hp&w=3840&h=2160&rs=1&c=4', '')
            title_copyright = image['copyright'].split(' (©')
            title = title_copyright[0]
            copyright = title_copyright[1].replace(')', '')
            if i == 'en-US':
                image_map['path_en'] = path
                image_map['title_en'] = title
                image_map['copyright_en'] = r'©%s' % copyright
            else:
                image_map['url'] = r'https://cn.bing.com%s' % path
                image_map['path'] = path
                image_map['title'] = title
                image_map['copyright'] = r'©%s' % copyright
        OperateJson.set_changed([image_map], 'bing')
