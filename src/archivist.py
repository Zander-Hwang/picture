""" 
# -*- coding: utf-8 -*-
@Project: picture
@File: archivist
@Author: zander
@Date: 2024/11/9 11:02
@Software: PyCharm
@Description: 文件归档 - 写入 SQLite 数据库、写入 MarkDown 文件展示
"""
import os
from lxml import etree
from src.utils import DataBase, FileUtils, DateUtils


class ArchivistUtil:
    def __init__(self):
        db = DataBase('./database/picture.db')
        for i in db.query_all('picture_info'):
            print(dict(i))
        db.close()

    # @description 更新数据库
    # @param {Dictionary} data 需要更新的数据
    # @param {String} edit_type 更新的类型(新增A、删除D、移动R100)
    @staticmethod
    def update_file_info(data, edit_type):
        db = DataBase('./database/picture.db')
        if edit_type == 'A':
            db.insert('picture_info', data)
        elif edit_type == 'D':
            db.delete('picture_info', 'PATH = "%s"' % data['path'])
        else:
            file_type = 'img' if data['to_path'].find('file/img/') >= 0 else 'liberty'
            db.update('picture_info', {'path': data['to_path'], 'type': file_type}, 'PATH = "%s"' % data['path'])
        db.close()

    # @description 更新md文件
    # @param {Dictionary} data 需要更新的数据
    # @param {String} edit_type 更新的类型(新增A、删除D、移动R100)
    @staticmethod
    def update_readme_info(data, edit_type):
        path = ''
        to_path = ''
        if 'type' in data:
            path = r'./archivist/%s.md' % data['type']
        else:
            file_type = 'img' if data['path'].find('file/img/') >= 0 else 'liberty'
            to_file_type = 'img' if data['to_path'].find('file/img/') >= 0 else 'liberty'
            path = r'./archivist/%s.md' % file_type
            to_path = r'./archivist/%s.md' % to_file_type
            name = os.path.basename(to_path).split('.')[0]
            if not os.path.exists(to_path):
                title = r'<h3><center>%s View</center></h3>%s' % (name.capitalize(), '\r\n\r\n')
                FileUtils.write(to_path, title)
        name = os.path.basename(path).split('.')[0]
        if not os.path.exists(path):
            title = r'<h3><center>%s View</center></h3>%s' % (name.capitalize(), '\r\n\r\n')
            FileUtils.write(path, title)
        if edit_type == 'A':
            ArchivistUtil.add_readme(path, data)
        elif edit_type == 'D':
            ArchivistUtil.delete_readme(path, data)
        # else:
        #     ArchivistUtil.update_readme(path, to_path, data)

    @staticmethod
    def add_readme(path, data):
        date = DateUtils.strptime(data['date'], '%Y-%m-%d', '%Y-%m')
        title = data['title']
        if data['type'] == 'bing':
            href = r'https://bing.com%s&pid=hp&w=160&h=90&rs=1&c=4' % data['path']
        else:
            href = r'https://cdn.jsdelivr.net/gh/Zander-Hwang/picture%s' % data['path']
        table_xpath = '//table[@class="sn_{}"]'.format(date)
        readme_str = FileUtils.read(path).replace('&', '&amp;')
        readme_ele = etree.fromstring(f"<div>{readme_str}</div>".encode('utf-8'))
        now_table = readme_ele.xpath(table_xpath)
        table_str = r'''
<table class="sn_date" style="width:100%;">
    <tr>
        <td colspan="4" style="text-align:center">date</td>
    </tr>{}
</table>
'''
        tr_str = r'''
    <tr class="cont">{}
    </tr>'''
        td_str = r'''
        <td class="cont" style="padding:2px;font-size:0;text-align:center"><img src="href" alt="title"/></td>'''
        if len(now_table) == 1:
            td_cont = now_table[0].xpath('./tr[@class="cont"]/td')
            if len(td_cont) % 4 == 0:
                new_tr = etree.Element("tr")
                new_tr.set('class', 'cont')
                now_table[0].append(new_tr)
            tr_cont = now_table[0].xpath('./tr[@class="cont"]')
            for i in range(len(tr_cont)):
                if i + 1 < len(tr_cont) and len(tr_cont[i].xpath('./td')) >= 4:
                    tr_cont[i + 1].insert(0, tr_cont[i].xpath('./td')[-1])
            tr_cont[0].insert(0, etree.fromstring(td_str))
        else:
            table_str = table_str.format(tr_str.format(td_str))
            readme_ele.insert(1, etree.fromstring(table_str))
        change_text = etree.tostring(readme_ele, pretty_print=True, encoding='unicode')
        # html代码格式化
        change_text = change_text.replace('&amp;', '&').replace('<div>', '').replace('</div>', '')
        change_text = change_text.replace('</table><table', '</table>\r\n\r\n<table')
        change_text = change_text.replace('</table>\n<table', '</table>\r\n\r\n<table')
        change_text = change_text.replace('</table>\n\n<table', '</table>\r\n\r\n<table')
        change_text = change_text.replace('</td><td', '</td>\r\n\t\t<td').replace('</tr></table>', '</tr>\r\n</table>')
        change_text = change_text.replace('</td>\n\t\t</tr>', '</td>\r\n\t</tr>').replace('</table>\n', '</table>')
        change_text = change_text.replace('</tr>\n<tr', '</tr>\r\n\t<tr').replace('</td>\n\t<td', '</td>\r\n\t\t<td')
        change_text = change_text.replace('<tr class="cont"><td', '<tr class="cont">\r\n\t\t<td')
        text = change_text.replace('date', date).replace('href', href).replace('title', title)
        FileUtils.write(path, text)

    @staticmethod
    def delete_readme(path, data):
        date = DateUtils.strptime(data['date'], '%Y-%m-%d', '%Y-%m')
        table_xpath = '//table[@class="sn_{}"]'.format(date)
        readme_str = FileUtils.read(path).replace('&', '&amp;')
        readme_ele = etree.fromstring(f"<div>{readme_str}</div>".encode('utf-8'))
        now_table = readme_ele.xpath(table_xpath)
        del_ele = now_table[0].xpath(r'./tr[@class="cont"]/td/img[contains(@src, "%s")]/..' % data['path'])[0]
        del_ele.getparent().remove(del_ele)
        tr_cont = now_table[0].xpath('./tr[@class="cont"]')
        for i in range(len(tr_cont)):
            if len(tr_cont[i].xpath('./td')) < 4 and i + 1 < len(tr_cont):
                tr_cont[i].append(tr_cont[i + 1].xpath('./td')[0])
            if len(tr_cont[i].xpath('./td')) == 0:
                tr_cont[i].getparent().remove(tr_cont[i])
        change_text = etree.tostring(readme_ele, pretty_print=True, encoding='unicode')
        # html代码格式化
        change_text = change_text.replace('&amp;', '&').replace('<div>', '').replace('</div>', '')
        change_text = change_text.replace('\n\t</table>\n', '\r\n</table>')
        change_text = change_text.replace('</td>\n\t<td', '</td>\r\n\t\t<td')
        change_text = change_text.replace('</td>\n\t\t</tr', '</td>\r\n\t</tr')
        FileUtils.write(path, change_text)

    @staticmethod
    def update_readme(path, to_path, data):
        print(path)
        print(to_path)
        print(data)
