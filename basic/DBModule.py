#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-02 13:58'

from basic.NovelStructure import *

import MySQLdb
import logging
from ConfigParser import SafeConfigParser

def here():
    print('PrimeMusic')

class MySQLModule(object):
    """
        和MySQL数据库操作的基类
    """
    __metaclass__ = Singleton

    def __init__(self):
        """
            单例类，初始化操作读取配置
        """
        parser = SafeConfigParser()
        parser.read('./conf/db.conf')

        self.conection_info = {}
        for table_name in parser.sections():
            item = {}
            for key, value in parser.items(table_name):
                item[key] = value
            self.conection_info[table_name] = item

        self.logger = logging.getLogger('novel.db')
        self.err = logging.getLogger('err.db')

    def buid_connection(self, table_name):
        """
            建立连接
        """
        if not self.conection_info.has_key(table_name):
            self.err.warning('no table {0}'.format(table_name))
            return False
        try:
            conn = MySQLdb.connect(
                host = self.conection_info[table_name]['host'],
                port = int(self.conection_info[table_name]['port']),
                user = self.conection_info[table_name]['user'],
                passwd = self.conection_info[table_name]['passwd'],
                db = self.conection_info[table_name]['db']
            )
        except Exception, e:
            self.err.warning('can not connect to MySQL [table: {0}, err: {1}]'.format(table_name, e))
            return False
        return conn


if __name__ == '__main__':
    here()    







