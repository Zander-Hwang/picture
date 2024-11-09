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
from src.archivist import ArchivistUtil


class LocalGit:
    def __init__(self):
        self.get_git_local_changes()

    @staticmethod
    def get_git_local_changes():
        cmd = 'git log --name-status --reverse --after="yesterday" file'
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        output = result.stdout
        output = output.split('commit ')
        output.pop(0)
        change_list = []
        for s in output:
            add_reg = r'^(A)\t(.*?)\s*$'
            del_reg = r'^(D)\t(.*?)\s*$'
            up_reg = r'^(R100)\t(.*?)\s*$'
            add_file = re.findall(add_reg, s, re.M)
            del_file = re.findall(del_reg, s, re.M)
            up_file = re.findall(up_reg, s, re.M)
            date = re.search(r'^Date\b.*$', s, re.M).group().replace('Date:   ', '')
            date = DateUtils.strptime(date, '%a %b %d %H:%M:%S %Y +0800', '%Y-%m-%d')
            if len(add_file) > 0:
                change_list.extend((*t, date) for t in add_file)
            if len(del_file) > 0:
                change_list.extend((*t, date) for t in del_file)
            if len(up_file) > 0:
                change_list.extend((*t, date) for t in up_file)
        for i in change_list:
            edit_type = i[0]
            path = i[1].split('\t')
            date = i[2]
            item = {
                'type': edit_type,
                'date': date
            }
            if len(path) > 1:
                item = {
                    'path': r'/%s' % path[0],
                    'to_path': r'/%s' % path[1],
                    'date': date
                }
            else:
                filename = os.path.basename(path[0]).split('.')[0]
                item = {
                    'type': 'img' if path[0].find('file/img/') >= 0 > 10 else 'liberty',
                    'path': r'/%s' % path[0],
                    'date': date,
                    'title': filename
                }
            ArchivistUtil.update_file_info(item, edit_type)
