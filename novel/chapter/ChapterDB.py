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


    def get_novelauthoritydir_list(self, rid):
        """
        """
        cursor = self.get_cursor('novel_authority_dir')
        sql = 'SELECT align_id, chapter_index, chapter_status ' \
              'FROM novel_authority_dir{0} ' \
              'WHERE rid = {1} ' \
              'ORDER BY chapter_index'.format(rid % 256, rid)
        try:
            cursor.execute(sql)
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return []

        result = []
        for row in cursor.fetchall():
            result.append(row)
        cursor.close()
        return result


    def get_novelclusterdirinfo_list(self, rid):
        """
        """
        cursor = self.get_cursor('novel_cluster_dir_info')
        sql = 'SELECT book_name, pen_name, dir_url ' \
              'FROM novel_cluster_dir_info ' \
              'WHERE rid = {0}'.format(rid)
        try:
            cursor.execute(sql)
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return []

        result = []
        for row in cursor.fetchall():
            result.append(row)
        cursor.close()
        return result


    def get_integratechapterinfo_list(self, rid, align_id):
        """
        """
        cursor = self.get_cursor('integrate_chapter_info')
        sql = 'SELECT chapter_id, chapter_url, chapter_title ' \
              'FROM integrate_chapter_info{0} ' \
              'WHERE rid = {1} AND align_id = {2}'.format(rid % 256, rid, align_id)
        try:
            cursor.execute(sql)
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return []

        result = []
        for row in cursor.fetchall():
            result.append(row)
        cursor.close()
        return result


if __name__ == '__main__':
    here()    







