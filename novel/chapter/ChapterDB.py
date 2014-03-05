#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-03-05 17:16'

from basic.DBModule import *

def here():
    print('PrimeMusic')


class ChapterDBModule(MySQLModule):
    """
        封装聚类模块中用到的数据库操作
    """
    def __init__(self):
        """
        """
        MySQLModule.__init__(self)

        self.connection_dict = {}


    def __del__(self):
        """
        """
        for (table_name, conn) in self.connection_dict.items():
            try:
                conn.close()
            except Exception, e:
                continue


    def get_cursor(self, table_name):
        """
        """
        if not self.connection_dict.has_key(table_name):
            conn = self.buid_connection(table_name)
            self.connection_dict[table_name] = conn

        conn = self.connection_dict[table_name]
        cursor = conn.cursor()

        return cursor


    def get_novelauthoritydir_list(self, ):

if __name__ == '__main__':
    here()    







