""" 
# -*- coding: utf-8 -*-
@Project: picture
@File: archivist
@Author: zander
@Date: 2024/11/9 11:02
@Software: PyCharm
@Description: 文件归档 - 写入 SQLite 数据库、写入 MarkDown 文件展示
"""
from src.utils import DataBase


class ArchivistUtil:
    @staticmethod
    def update_file_info(data, edit_type):
        db = DataBase('./database/picture.db')
        if edit_type == 'A':
            db.insert('picture_info', data)
        elif edit_type == 'D':
            db.delete('picture_info', 'PATH = "%s"' % data['path'])
        else:
            file_type = 'img' if data['to_path'].find('file/img/') >= 0 > 10 else 'liberty'
            db.update('picture_info', {'path': data['to_path'], 'type': file_type}, 'PATH = "%s"' % data['path'])
        db.close()
