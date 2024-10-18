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
import time


class FileUtils:

    # @description 读取对应的md文件内容
    # @param {Str} path 文件路径
    # @param {Date} date 当前年月
    # @returns {Dict} 返回Dict
    def read_readme(self, path, date):
        table_xpath = '//table[@class="sn_{}"]'.format(date)
        add_table_ele = None
        add_tr_ele = None
        add_td_ele = None
        with open(path, "r", encoding='utf-8') as f:
            readme_info = f.read()
            readme_ele = etree.fromstring(f"<div>{readme_info}</div>")
            now_table = readme_ele.xpath(table_xpath)
            if len(now_table) == 1:
                tr_cont = now_table[0].xpath('./tr[@class="cont"]')
                td_cont = tr_cont[-1].xpath('./td')
                if len(td_cont) == 4:
                    add_table_ele = readme_ele
                    add_td_ele = td_cont[-1]
                else:
                    tr_cont[-1].getparent().remove(tr_cont[-1])
                    add_table_ele = readme_ele
                    add_tr_ele = tr_cont[-1]
            else:
                add_table_ele = readme_ele
        f.close()
        return {"table": add_table_ele, "tr": add_tr_ele, "td": add_td_ele}

    def write_readme(self, path, url, title):
        now = time.localtime()
        year_month = time.strftime('%Y-%m', now)
        table_xpath = '//table[@class="sn_{}"]'.format(year_month)
        html_dict = self.read_readme(path, year_month)
        table = '\r\n<table class="sn_{}" width="100%">\r\t<tr>\r\t\t<td colspan="4" style="text-align:center">{}</td>\r\t</tr>{}\r</table>'
        tr = '\r\t<tr class="cont">{}\r\t</tr>'
        td = '\r\t\t<td width="25%"><img src="{}" alt="{}" /></td>'
        if html_dict['tr'] is None and html_dict['td'] is None:
            info = table.format(year_month, year_month, tr.format(td.format(url, title)))
            info_html = etree.fromstring(info)
            html_dict['table'].append(info_html)
        else:
            if html_dict['tr'] is None:
                info = tr.format(td.format(url, title))
                info_html = etree.fromstring(info)
                html_dict['table'].xpath(table_xpath)[-1].append(info_html)
            else:
                info = td.format(url, title)
                info_html = etree.fromstring(info)
                html_dict['tr'].append(info_html)
                html_dict['table'].xpath(table_xpath)[-1].append(html_dict['tr'])
        md_info = etree.tostring(html_dict['table']).decode('utf-8')
        md_info = md_info.replace("<div>", "")
        md_info = md_info.replace("</div>", "")
        print(md_info)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(md_info)
        f.close()
