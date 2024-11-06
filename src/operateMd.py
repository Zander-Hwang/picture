"""
# -*- coding: utf-8 -*-
@Project: picture
@File: operateMd
@Author: zander
@Date: 2024/10/23 15:24
@Software: PyCharm
@Description: Markdown文件操作 - 将更改之后的图片写入文件中以便预览
"""
from lxml import etree
from src.utils import FileUtils
import os
from src.utils import DateUtils
import time


class OperateMd:
    # def __init__(self):
    #     json_map = FileUtils.read_json('./archivist/wallpaper/bing.json')
    #     json_list = []
    #     for key in json_map:
    #         value = json_map[key]
    #         json_list.extend(value)
    #     for i in range(6):
    #         self.update_readme('./archivist/bing.md', json_list[i])
    #     # for i in json_list:
    #     #     self.update_readme('./archivist/bing.md', i)

    # @description 更新md文件
    # @param {String} path 需要写入的md文件的路径 ./archivist/img.md
    # @param {Dictionary} data 写入的数据
    @staticmethod
    def update_readme(path, data):
        name = os.path.basename(path).split('.')[0]
        if not os.path.exists(path):
            title = r'<h3><center>%s View</center></h3>' % name.capitalize()
            FileUtils.write(path, title)
        date = DateUtils.formattime('%Y-%m', time.strptime(data['date'], '%Y-%m-%d'))
        title = data['title']
        if name == 'bing':
            href = r"%s&pid=hp&w=160&h=90&rs=1&c=4" % data['url']
        else:
            href = data['url']
        change_dic = OperateMd.read_readme(path, date)
        table = '{}<table class="sn_{}" width="100%">\r\n\t<tr>\r\n\t\t<td colspan="4" style="text-align:center">{}</td>\r\n\t</tr>{}</table>'
        tr = '{}<tr class="cont">{}</tr>{}'
        td = '{}<td width="25%"><img src="{}" alt="{}" /></td>{}'
        if change_dic['type'] == 'table':
            td_el = td.format('\r\n\t\t', href, title, '\r\n\t')
            tr_el = tr.format('\r\n\t', td_el, '\r\n')
            el_text = table.format('\r\n\r\n', date, date, tr_el)
            text = change_dic['text'].replace("<table/>", el_text)
        elif change_dic['type'] == 'tr':
            td_el = td.format('\r\n\t\t', href, title, '\r\n\t')
            el_text = tr.format('\t', td_el, '\r\n')
            text = change_dic['text'].replace("<tr/>", el_text)
        else:
            el_text = td.format('\t', href, title, '\r\n\t')
            text = change_dic['text'].replace("<td/>", el_text)
        FileUtils.write(path, text)

    # @description 读取对应的md文件内容
    # @param {Str} path 文件路径
    # @param {Date} date 当前年月
    # @returns {Dict} 返回Dict text：需要改变的字符串(直接替换相对应的类型) type：表示需要改变的类型(table、tr、td)
    @staticmethod
    def read_readme(path, date):
        table_xpath = '//table[@class="sn_{}"]'.format(date)
        readme_str = FileUtils.read(path).replace('&', '&amp;')
        readme_ele = etree.fromstring(f"<div>{readme_str}</div>".encode('utf-8'))
        now_table = readme_ele.xpath(table_xpath)
        if len(now_table) == 1:
            tr_cont = now_table[0].xpath('./tr[@class="cont"]')
            td_cont = tr_cont[-1].xpath('./td')
            if len(td_cont) == 4:
                now_table[0].append(etree.fromstring('<tr/>'))
                change_text = etree.tostring(readme_ele, encoding='unicode').replace('&amp;', '&')
                change_type = 'tr'
            else:
                tr_cont[-1].append(etree.fromstring('<td/>'))
                change_text = etree.tostring(readme_ele, encoding='unicode').replace('&amp;', '&')
                change_type = 'td'
        else:
            readme_ele.append(etree.fromstring('<table/>'))
            change_text = etree.tostring(readme_ele, encoding='unicode').replace('&amp;', '&')
            change_type = 'table'
        return {'text': change_text.replace('<div>', '').replace('</div>', ''), 'type': change_type}
