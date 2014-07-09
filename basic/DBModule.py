#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-02 13:58'

from basic.NovelStructure import *

import types
import MySQLdb
import MySQLdb.connections
import logging
import random
from collections import defaultdict
from ConfigParser import SafeConfigParser

def here():
    print('PrimeMusic')


@classmethod
def addMethod(cls, method_name, method):
    """
    """
    setattr(cls, method_name, types.MethodType(method, None, cls))


def cursor(_cursor):
    """
    """
    def cursor_wrap(self, cursorclass=None):
        """
        """
        try:
            self.ping()
        except Exception as e:
            self.reconnect()
        return _cursor(self, cursorclass)

    return cursor_wrap


def reconnect(self):
    """
    """
    try:
        self.__init__(*self.conn_args['args'], **self.conn_args['kwargs'])
    except Exception as e:
        return False

    if callable(getattr(self, 'conn_init', None)):
        getattr(self, 'conn_init')()

    return True


def conn_init(self):
    """
    """
    self.set_character_set('GBK')
    self.autocommit(True)
    return True


MySQLdb.connections.Connection.addMethod = addMethod

MySQLdb.connections.Connection.addMethod('reconnect', reconnect)
MySQLdb.connections.Connection.addMethod('cursor', cursor(MySQLdb.connections.Connection.cursor))
MySQLdb.connections.Connection.addMethod('conn_init', conn_init)


class MySQLModule(object):
    """
        和MySQL数据库操作的基类
    """
    __metaclass__ = Singleton

    def __init__(self):
        """
            单例类，初始化操作读取配置
        """
        self.logger = logging.getLogger('novel.db')
        self.err = logging.getLogger('err.db')

        parser = SafeConfigParser()
        parser.read('./conf/db.conf')

        self.conection_info = defaultdict(list)
        for table_name in parser.sections():
            item = {}
            for key, value in parser.items(table_name):
                item[key] = value
            table_name = table_name.split('-')[0]
            self.conection_info[table_name].append(item)



    def db_connect(self, *args, **kwargs):
        """
        """
        try:
            conn = MySQLdb.connect(*args, **kwargs)
            conn.conn_init()
            conn.conn_args = {'args': args, 'kwargs': kwargs}
        except Exception as e:
            self.err.warning('[connect error: {0}]'.format(e))
            conn = False
        return conn


    def buid_connection(self, table_name):
        """
            建立连接
        """
        if not self.conection_info.has_key(table_name):
            self.err.warning('no table {0}'.format(table_name))
            return False
        item = self.conection_info[table_name][random.randint(0, len(self.conection_info[table_name]) - 1)]
        conn = self.db_connect(
            host = item['host'],
            port = int(item['port']),
            user = item['user'],
            passwd = item['passwd'],
            db = item['db']
        )
        return conn


if __name__ == '__main__':
    here()    







