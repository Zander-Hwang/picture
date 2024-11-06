""" 
# -*- coding: utf-8 -*-
@File: dateutils
@Author: zander
@Date: 2024/10/21 14:12
@Software: PyCharm
@Description: 时间处理工具类
"""
import time


class DateUtils:

    @staticmethod
    def sleep(secs):
        time.sleep(secs)

    @staticmethod
    def time():
        return time.time()

    @staticmethod
    def localtime(date=None):
        if date is None:
            date = time.time()
        return time.localtime(date)

    @staticmethod
    def formattime(format_str='%Y-%m-%d %H:%M:%S', date=None):
        if date is None:
            date = time.localtime()
        return time.strftime(format_str, date)

    @staticmethod
    def strptime(date, format_str='%Y-%m-%d %H:%M:%S'):
        return time.strptime(date, format_str)

    @staticmethod
    def getDate():
        return DateUtils.localtime().tm_mday

    @staticmethod
    def getDay():
        return DateUtils.localtime().tm_wday

# %y 两位数的年份表示（00-99）
# %Y 四位数的年份表示（000-9999）
# %m 月份（01-12）
# %d 月内中的一天（0-31）
# %H 24小时制小时数（0-23）
# %I 12小时制小时数（01-12）
# %M 分钟数（00=59）
# %S 秒（00-59）
# %a 本地简化星期名称
# %A 本地完整星期名称
# %b 本地简化的月份名称
# %B 本地完整的月份名称
# %c 本地相应的日期表示和时间表示
# %j 年内的一天（001-366）
# %p 本地A.M.或P.M.的等价符
# %U 一年中的星期数（00-53）星期天为星期的开始
# %w 星期（0-6），星期天为星期的开始
# %W 一年中的星期数（00-53）星期一为星期的开始
# %x 本地相应的日期表示
# %X 本地相应的时间表示
# %Z 当前时区的名称
# %% %号本身
