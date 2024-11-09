""" 
# -*- coding: utf-8 -*-
@File: database
@Author: zander
@Date: 2024/11/8 15:44
@Software: PyCharm
@Description: sqlite3 数据库操作相关
"""
import sqlite3
from collections import namedtuple
from math import ceil


class DataBase:
    def __init__(self, dbpath='./database/database.db'):
        # @description 初始化 SQLite 数据库连接和游标
        # @param {dbpath} 数据库文件路径
        self.conn = sqlite3.connect(dbpath)
        # 通过索引获取值
        self.conn.row_factory = sqlite3.Row
        # 创建游标对象
        self.cursor = self.conn.cursor()

    # @description 创建表
    # @param {table_name} 表名称
    # @param {columns} 列定义，格式为 "列名1 数据类型1, 列名2 数据类型2, ...
    # db.create_table('students', 'id INTEGER PRIMARY KEY, name TEXT NOT NULL, age INTEGER, gender TEXT')
    def create_table(self, table_name, columns):
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                {columns}
            )
        ''')
        self.conn.commit()

    # @description 删除表
    # @param {table_name} 表名称
    def delete_table(self, table_name):
        self.cursor.execute(f'''
            DROP TABLE IF EXISTS {table_name}
        ''')
        self.conn.commit()

    # @description 插入数据
    # @param {table_name} 表名称
    # @param {data} 要插入的数据，格式为 {"列名1": 值1, "列名2": 值2, ...}
    # @returns 插入的数据的所有行
    # db.insert('students', {'name': 'Alice', 'age': 20, 'gender': 'Female'})
    def insert(self, table_name, data):
        # 列
        columns = ', '.join(data.keys())
        # 占位符
        placeholders = ', '.join(['?'] * len(data))
        values = tuple(data.values())
        self.cursor.execute(f'''
            INSERT INTO {table_name} ({columns}) VALUES ({placeholders})
        ''', values)
        self.conn.commit()
        return self.cursor.fetchall()

    # @description 更新数据
    # @param {table_name} 表名称
    # @param {data} 要更新的数据，格式为 {"列名1": 值1, "列名2": 值2, ...}
    # @param {condition} 更新条件
    # db.update('students', {'age': 21, 'gender': 'Female'}, 'name = "Alice"')
    def update(self, table_name, data, condition):
        columns = ', '.join([f'{column}=?' for column in data.keys()])
        values = tuple(data.values())
        self.cursor.execute(f'''
            UPDATE {table_name} SET {columns} WHERE {condition}
        ''', values)
        self.conn.commit()

    # @description 删除数据
    # @param {table_name} 表名称
    # @param {condition} 删除条件
    # db.delete('students', 'name = "Bob"')
    def delete(self, table_name, condition):
        self.cursor.execute(f'''
            DELETE FROM {table_name} WHERE {condition}
        ''')
        self.conn.commit()

    # @description 查询表格中的所有数据
    # @param {table_name} 表名称
    # @returns 所有数据的所有行
    # db.query_all('students')
    def query_all(self, table_name):
        self.cursor.execute(f'''
            SELECT * FROM {table_name}
        ''')
        return self.cursor.fetchall()

    # @description 分页查询表格中的数据
    # @param {table_name} 表名称
    # @param {page_size} 每页数据数量
    # @param {page_number} 页码
    # @param {condition} 查询条件 ”age > 10“
    # @returns 分页数据的所有行、总数和总页数
    # rows, total_count, total_pages = db.query_page('users', 10, 1)
    def query_page(self, table_name, page_size, page_number, condition=None):
        if condition:
            query = f'''
                SELECT * FROM {table_name}
                WHERE {condition}
                LIMIT {page_size} OFFSET {page_size * (page_number - 1)}
            '''
        else:
            query = f'''
                SELECT * FROM {table_name}
                LIMIT {page_size} OFFSET {page_size * (page_number - 1)}
            '''
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        column_names = [desc[0] for desc in self.cursor.description]
        Row = namedtuple('Row', column_names)
        rows = [Row(*row) for row in results]
        # 查询总数
        count_query = f'SELECT COUNT(*) FROM {table_name}'
        if condition:
            count_query += f' WHERE {condition}'
        self.cursor.execute(count_query)
        total_count = self.cursor.fetchone()[0]
        # 计算总页数
        total_pages = ceil(total_count / page_size)

        return rows, total_count, total_pages

    # @description 执行自定义的SQL语句
    # @param {sql} SQL语句
    # @param {params} SQL语句中的参数，可选
    # @returns 执行结果的所有行
    # db.execute_sql('DELETE FROM students WHERE name = "Charlie"')
    def execute_sql(self, sql, params=None):
        if params is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, params)
        # self.conn.commit()
        return self.cursor.fetchall()

    # @description 执行表格的连接查询
    # @param {table1_name} 第一个表名称
    # @param {table2_name} 第二个表名称
    # @param {on_condition} 连接条件
    # @returns 连接查询结果的所有行
    # db.query_join('students', 'courses', 'students.id = courses.id')
    def query_join(self, table1_name, table2_name, on_condition):
        self.cursor.execute(f'''
            SELECT * FROM {table1_name}
            INNER JOIN {table2_name} ON {on_condition}
        ''')
        return self.cursor.fetchall()

    def close(self):
        # 关闭游标
        self.cursor.close()
        # 关闭数据库连接
        self.conn.close()
