""" 
# -*- coding: utf-8 -*-
@Project: picture
@File: fileUtils
@Author: zander
@Date: 2024/10/17 15:48
@Software: PyCharm
@Description: 文件操作类
"""
from lxml import etree
import json
import time
import os


class FileUtils:

    # @description 读取对应的md文件内容
    # @param {Str} path 文件路径
    # @param {Date} date 当前年月
    # @returns {Dict} 返回Dict text：需要改变的字符串(直接替换相对应的类型) type：表示需要改变的类型(table、tr、td)
    @staticmethod
    def read_readme(path, date):
        table_xpath = '//table[@class="sn_{}"]'.format(date)
        with open(path, "r", encoding='utf-8') as f:
            readme_info = f.read()
            readme_ele = etree.fromstring(f"<div>{readme_info}</div>")
            now_table = readme_ele.xpath(table_xpath)
            if len(now_table) == 1:
                tr_cont = now_table[0].xpath('./tr[@class="cont"]')
                td_cont = tr_cont[-1].xpath('./td')
                if len(td_cont) == 4:
                    now_table[0].append(etree.fromstring('<tr/>'))
                    change_text = etree.tostring(readme_ele).decode('utf-8')
                    change_type = 'tr'
                else:
                    tr_cont[-1].append(etree.fromstring('<td/>'))
                    change_text = etree.tostring(readme_ele).decode('utf-8')
                    change_type = 'td'
            else:
                readme_ele.append(etree.fromstring('<table/>'))
                change_text = etree.tostring(readme_ele).decode('utf-8')
                change_type = 'table'
        f.close()
        return {"text": change_text.replace("<div>", "").replace("</div>", ""), "type": change_type}

    # @description 写入md文件
    # @param {String} path 需要写入的md文件的路径 ./archivist/img.md
    # @param {Dictionary} data 写入的数据
    def write_readme(self, path, data):
        now = time.localtime()
        year_month = time.strftime('%Y-%m', now)
        url = data['url']
        title = data['title']
        change_dic = self.read_readme(path, year_month)
        table = '{}<table class="sn_{}" width="100%">\r\n\t<tr>\r\n\t\t<td colspan="4" style="text-align:center">{}</td>\r\n\t</tr>{}</table>'
        tr = '{}<tr class="cont">{}</tr>{}'
        td = '{}<td width="25%"><img src="{}" alt="{}" /></td>{}'
        if change_dic['type'] == 'table':
            td_el = td.format('\r\n\t\t', url, title, '\r\n\t')
            tr_el = tr.format('\r\n\t', td_el, '\r\n')
            el_text = table.format('\r\n\r\n', year_month, year_month, tr_el)
            text = change_dic['text'].replace("<table/>", el_text)
        elif change_dic['type'] == 'tr':
            td_el = td.format('\r\n\t\t', url, title, '\r\n\t')
            el_text = tr.format('\t', td_el, '\r\n')
            text = change_dic['text'].replace("<tr/>", el_text)
        else:
            el_text = td.format('\t', url, title, '\r\n\t')
            text = change_dic['text'].replace("<td/>", el_text)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        f.close()

    # @description 读取json文件
    # @param {String} path 需要读取的json文件的路径
    # @param {Dictionary} data 读取到的数据
    def read_json(self, path):
        with open(path, "r", encoding='utf-8') as f:
            data = json.load(f)
        f.close()
        return data

    # @description 写入json文件
    # @param {String} path 需要写入的json文件的路径
    # @param {String} data 需要写入的数据
    def write_json(self, path, data):
        with open(path, "w", encoding='utf-8') as f:
            json_str = json.dumps(data, indent=2)
            f.write(json_str)
        f.close()

    # @description 设置更改的文件的对应json记录
    # @param {String} directory 文件相对目录(针对的是【file】文件夹里面的目录) 'img/2024'
    # @param {List} files 更改的文件列表
    # @returns {List} 返回更改的文件json记录列表
    def set_changed_json(self, directory, files):
        file_details = []
        for file in files:
            filename = os.path.splitext(file)[0]
            relative_path = "{}/{}".format(directory, file)
            file_details.append({
                "url": "https://cdn.jsdelivr.net/gh/Zander-Hwang/picture/file/{}".format(relative_path),
                "path": fr"/picture/{relative_path}",
                "title": filename,
                "title_en": filename,
                "copyright": "",
                "copyright_en": ""
            })
        return file_details
