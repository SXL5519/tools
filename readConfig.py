#-*- coding:utf-8 -*-
import os
import codecs
import configparser

import sys

"""
读取配置文件的数据
"""
path=os.path.split(sys.path[0])[0]
# print(path)
configPath =(path+"/config.ini")
# configPath =("../config.ini")  ###本地运行
class ReadConfig:
    def __init__(self):
        fd = open(configPath)
        data = fd.read()


        #  remove BOM
        """
        去除文件字符编码格式前的隐藏字符BOM
        """
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(configPath, "w")
            file.write(data)
            file.close()
        fd.close()

        self.cf = configparser.ConfigParser()
        self.cf.read(configPath)

    def get_email(self, name):
        value = self.cf.get("EMAIL", name)
        return value

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_db(self, name):
        value = self.cf.get("DATABASE", name)
        return value