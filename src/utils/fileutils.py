""" 
# -*- coding: utf-8 -*-
@File: readfile
@Author: zander
@Date: 2024/10/20 12:03
@Software: PyCharm
@Description: 文件读取方法类
"""
import json
import os

TYPE_LIST = {
    '3c68313ee689abe68f8f': 'html',
    '504B0304140006000800': 'xlsx',
    '504b0304140008080800': 'docx',
    "d0cf11e0a1b11ae10000": 'doc/xls/vsd',
    '2d2d204d7953514c2064': 'sql',
    'ffd8ffe000104a464946': 'jpg',
    '89504e470d0a1a0a0000': 'png',
    '47494638396126026f01': 'gif',
    '3c21444f435459504520': 'html',
    '3c21646f637479706520': 'htm',
    '48544d4c207b0d0a0942': 'css',
    '2f2a21206a5175657279': 'js',
    '255044462d312e350d0a': 'pdf',
    '68746D6C3E': 'html',
    '7b0a2020223230323': 'json',
    '44656C69766572792D64': 'eml',
    '49492a00227105008037': 'tif',
    '424d228c010000000000': 'bmp',
    '424d8240090000000000': 'bmp',
    '424d8e1b030000000000': 'bmp',
    '41433130313500000000': 'dwg',
    '696b2e71623d696b2e71': 'js',
    '7b5c727466315c616e73': 'rtf',
    '38425053000100000000': 'psd',
    '46726f6d3a203d3f6762': 'eml',
    '5374616E64617264204A': 'mdb',
    '252150532D41646F6265': 'ps',
    '2e524d46000000120001': 'rmvb',
    '464c5601050000000900': 'flv',
    '00000020667479706d70': 'mp4',
    '49443303000000002176': 'mp3',
    '000001ba210001000180': 'mpg',
    '3026b2758e66cf11a6d9': 'wmv',
    '52494646e27807005741': 'wav',
    '52494646d07d60074156': 'avi',
    '4d546864000000060001': 'mid',
    '504b0304140000080044': 'zip',
    '504b03040a0000080000': 'zip',
    '504b03040a0000000000': 'zip/jar',
    '526172211a0700cf9073': 'rar',
    '235468697320636f6e66': 'ini',
    '4d5a9000030000000400': 'exe',
    '3c25402070616765206c': 'jsp',
    '4d616e69666573742d56': 'mf',
    '3c3f786d6c2076657273': 'xml',
    '494e5345525420494e54': 'sql',
    '7061636b616765207765': 'java',
    '406563686f206f66660d': 'bat',
    '1f8b0800000000000000': 'gz',
    '6c6f67346a2e726f6f74': 'properties',
    'cafebabe0000002e0041': 'class',
    '49545346030000006000': 'chm',
    '04000000010000001300': 'mxp',
    '504b0304140006000800': 'docx',
    '6431303a637265617465': 'torrent',
}


class FileUtils:
    # 字节码转16进制字符串
    @staticmethod
    def __bytes2hex(byte):
        num = len(byte)
        hexstr = u""
        for i in range(num):
            t = u"%x" % byte[i]
            if len(t) % 2:
                hexstr += u"0"
            hexstr += t
        return hexstr.upper()

    # @description 获取文件类型
    # @param {String} path 需要读取的文件的路径
    # @returns {Dictionary} 文件类型 png、jpg、pdf
    @staticmethod
    def file_type(path):
        try:
            bin_file = open(path, 'rb')
            bins = bin_file.read(20)
            bin_file.close()
            bins = FileUtils.__bytes2hex(bins).lower()
            type_list = list(TYPE_LIST.keys())
            file_type = 'unknown'
            for i in type_list:
                lens = len(i)
                if bins[0:lens] == i:
                    file_type = TYPE_LIST[i]
                    break
            # 全码未找到，优化处理，码表取8位验证
            if file_type == 'unknown':
                bins = bins[0:8]
            for i in type_list:
                if len(i) > 8 and bins == i[0:8]:
                    file_type = TYPE_LIST[i]
                    break
            if file_type == 'unknown' or len(file_type.split('/')) > 1:
                file_type = os.path.splitext(path)[1][1:]
            return file_type
        except Exception as e:
            print(e)

    # @description 获取文件信息
    # @param {String} path 需要读取的文件的路径
    # @returns {Dictionary} 读取到的数据
    @staticmethod
    def file_info(path):
        if os.path.exists(path):
            return {
                'name': os.path.basename(path),
                'type': 'file' if os.path.isfile(path) else 'directory',
                'size': os.path.getsize(path),
                'modified_time': os.path.getmtime(path),
                'accessed_time': os.path.getatime(path),
                'created_time': os.path.getctime(path)
            }
        else:
            print("文件不存在或路径错误")

    # @description 读取文件
    # @param {String} path 需要读取的文件的路径
    # @param {String} mode 可选，文件打开模式 默认以只读方式打开文件。文件的指针将会放在文件的开头。
    # @returns {Dictionary} data 读取到的数据
    @staticmethod
    def read(path, mode='r', encoding='utf-8'):
        try:
            with open(path, mode, encoding=encoding) as f:
                data = f.read()
            f.close()
            return data
        except FileNotFoundError:
            print("文件不存在或路径错误")
        except IOError:
            print("文件读取错误")

    # @description 读取json文件
    # @param {String} path 需要读取的json文件的路径
    # @param {String} mode 可选，文件打开模式 默认以只读方式打开文件。文件的指针将会放在文件的开头。
    # @returns {Dictionary} data 读取到的数据
    @staticmethod
    def read_json(path, mode='r', encoding='utf-8'):
        try:
            with open(path, mode, encoding=encoding) as f:
                data = json.load(f)
            f.close()
            return data
        except FileNotFoundError:
            print("文件不存在或路径错误")
        except IOError:
            print("文件读取错误")

    # @description 写入文件
    # @param {String} path 需要写入的文件的路径
    # @param {String} mode 可选，文件打开模式 打开一个文件只用于写入
    # @param {String} data 需要写入的数据
    @staticmethod
    def write(path, data, mode='w', encoding='utf-8'):
        with open(path, mode, encoding=encoding) as f:
            f.write(data)
        f.close()

    # @description 写入json文件
    # @param {String} path 需要写入的json文件的路径
    # @param {String} mode 可选，文件打开模式 打开一个文件只用于写入
    # @param {String} data 需要写入的数据
    @staticmethod
    def write_json(path, data, mode='w', encoding='utf-8'):
        with open(path, mode, encoding=encoding) as f:
            json_str = json.dumps(data, ensure_ascii=False, indent=2)
            f.write(json_str)
        f.close()
