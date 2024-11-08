""" 
# -*- coding: utf-8 -*-
@Project: picture
@File: local
@Author: zander
@Date: 2024/11/6 15:47
@Software: PyCharm
@Description: PicGo 上传文件处理
"""
import re
import os
import subprocess
from src.utils import DateUtils
from src.operateJson import OperateJson


class LocalGit:
    def __init__(self):
        self.get_git_local_changes()

    @staticmethod
    def get_git_local_changes():
        cmd = 'git log --name-status --after="yesterday" file'
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        output = result.stdout
        # output = output.decode('utf-8')
        print(output)
        # output = output.split('commit ')
        # output.pop(0)
        # change_map = {
        #     'img': [
        #         {
        #             'type': 'D',
        #             'url': 'https://cdn.jsdelivr.net/gh/Zander-Hwang/picture/file/img/2024/001431sFPe6.jpg',
        #             'path': '/file/img/2024/001431sFPe6.jpg',
        #             'path_en': '/file/img/2024/001431sFPe6.jpg',
        #             'date': '2024-11-06',
        #             'title': '001431sFPe6',
        #             'title_en': '001431sFPe6',
        #             'copyright': '',
        #             'copyright_en': ''
        #         }
        #     ],
        #     'liberty': []
        # }
        # for s in output:
        #     date = re.search(r'^Date\b.*$', s, re.M).group().replace('Date:   ', '')
        #     date = DateUtils.strptime(date, '%a %b %d %H:%M:%S %Y +0800', '%Y-%m-%d')
        #     file = re.findall(r'^(A|D)\t(.*?)\s*$', s, re.M)
        #     for i in file:
        #         edit_type = i[0]
        #         path = i[1]
        #         filename = os.path.basename(path).split('.')[0]
        #         item = {
        #             'type': edit_type,
        #             'url': r'https://cdn.jsdelivr.net/gh/Zander-Hwang/picture/%s' % path,
        #             'path': r'/%s' % path,
        #             'path_en': r'/%s' % path,
        #             'date': date,
        #             'title': filename,
        #             'title_en': filename,
        #             'copyright': '',
        #             'copyright_en': ''
        #         }
        #         if path.find('file/img/') >= 0:
        #             change_map['img'].append(item)
        #         else:
        #             change_map['liberty'].append(item)
        # for key in change_map:
        #     value = change_map[key]
        #     if len(value) > 0:
        #         OperateJson.set_changed(value, key)
