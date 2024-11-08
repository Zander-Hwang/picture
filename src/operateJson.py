""" 
# -*- coding: utf-8 -*-
@Project: picture
@File: operateJson
@Author: zander
@Date: 2024/11/6 15:02
@Software: PyCharm
@Description: Json 文件操作 - 将更改之后的图片写入 Json 文件中
"""
import os


class OperateJson:
    # @description 设置更改的文件的对应json记录
    # @param {String} directory 文件相对目录(针对的是【file】文件夹里面的目录) 'img/2024'
    # @param {List} files 更改的文件列表
    # @returns {List} 返回更改的文件json记录列表
    @staticmethod
    def set_changed_json(directory, files):
        file_details = []
        for file in files:
            filename = os.path.splitext(file)[0]
            relative_path = "{}/{}".format(directory, file)
            file_details.append({
                "url": "https://cdn.jsdelivr.net/gh/Zander-Hwang/picture/file/{}".format(relative_path),
                "path": fr"/file/{relative_path}",
                "title": filename,
                "title_en": filename,
                "copyright": "",
                "copyright_en": ""
            })
        return file_details

    @staticmethod
    def set_changed(data, file_type):
        # print(file_type)
        append_map = {}
        delete_list = {}
        for i in data:
            date = r'%s-%s' % (i['date'].split('-')[0], i['date'].split('-')[1])
            if i['type'] == 'A':
                i.pop('type')
                if date in append_map:
                    append_map[date].append(i)
                else:
                    append_map[date] = [i]
            else:
                i.pop('type')
                if date in delete_list:
                    delete_list[date].append(i)
                else:
                    delete_list[date] = [i]
        # print(append_map)
        # print(delete_list)
