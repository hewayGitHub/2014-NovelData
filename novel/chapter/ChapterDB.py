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


    def get_noveldata_all(self, table_name, field_list):
        """
        """
        cursor = self.get_cursor(table_name)

        sql = 'SELECT max(id) AS id FROM {0}'.format(table_name)
        try:
            cursor.execute(sql)
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return []
        max_id = cursor.fetchone()[0]

        sql = 'SELECT min(id) AS id FROM {0}'.format(table_name)
        try:
            cursor.execute(sql)
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return []
        min_id = cursor.fetchone()[0]

        result = []
        while True:
            if min_id > max_id:
                break

            start_id = min_id
            end_id = min_id + 10000
            if end_id > max_id:
                end_id = max_id

            sql = 'SELECT {0} FROM {1} ' \
                  'WHERE id >= {2} AND id <= {3}'.format(', '.join(field_list), table_name, start_id, end_id)
            try:
                cursor.execute(sql)
            except Exception, e:
                self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
                break
            for row in cursor.fetchall():
                result.append(row)
            min_id = end_id + 1

        cursor.close()
        return result


    def get_novelclusterdirinfo_rid(self, rid):
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


    def get_novelclusterdirinfo_dir(self, dir_id_list):
        """
        """
        cursor = self.get_cursor('novel_cluster_dir_info')
        sql = 'SELECT dir_id, site, site_id, site_status ' \
              'FROM novel_cluster_dir_info ' \
              'WHERE dir_id IN ({0})'.format(', '.join("'%d'" % dir_id for dir_id in dir_id_list))
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


    def get_integratechapterinfo_list(self, rid, align_id):
        """
        """
        cursor = self.get_cursor('integrate_chapter_info')
        sql = 'SELECT dir_id, chapter_id, chapter_url, chapter_title ' \
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


    def get_novelaggregationdir_list(self, rid):
        """
        """
        cursor = self.get_cursor('dir_agg_chapter_info')
        sql = 'SELECT chapter_index, align_id, optimize_chapter_status ' \
              'FROM dir_agg_chapter_info{0} ' \
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


    def update_novelaggregationdir_info(self, current_chapter_status, chapter):
        """
        """
        cursor = self.get_cursor('dir_agg_chapter_info')
        sql = 'UPDATE dir_agg_chapter_info{0} SET ' \
              'optimize_site_id = {1}, optimize_chapter_id = {2}, optimize_chapter_url = {3}, ' \
              'optimize_chapter_status = {4}, optimize_chapter_wordsum = {5} ' \
              'WHERE rid = {6} AND align_id = {7}'.format(
            chapter.rid % 256,
            chapter.size_id, chapter.chapter_id, chapter.chapter_url,
            current_chapter_status, chapter.chinese_count,
            chapter.rid, chapter.align_id
        )
        try:
            cursor.execute(sql)
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return False

        cursor.close()
        return True



if __name__ == '__main__':
    here()    







