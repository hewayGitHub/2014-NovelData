#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-02 22:54'

from basic.DBModule import *

def here():
    print('PrimeMusic')

class ClusterDBModule(MySQLModule):
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


    def get_dirfmtinfo_id_list(self, site_id, update_time):
        """
        """
        sql = 'SELECT id FROM dir_fmt_info{0} WHERE update_time > {1}'.format(site_id, update_time)
        try:
            cursor = self.get_cursor('dir_fmt_info')
            cursor.execute(sql)
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return []

        result = []
        for (id, ) in cursor.fetchall():
            result.append(id)
        cursor.close()
        return result


    def get_dirfmtinfo_info(self, site_id, novel_id):
        """
        """
        sql = 'SELECT site_id, site, site_status, dir_id, dir_url, gid, book_name, pen_name ' \
              'FROM dir_fmt_info{0} ' \
              'WHERE id = {1}'.format(site_id, novel_id)
        try:
            cursor = self.get_cursor('dir_fmt_info')
            cursor.execute(sql)
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return False

        result = cursor.fetchone()
        cursor.close()
        return result


    def get_chapteroriinfo_list(self, site_id, dir_id):
        """
        """
        sql = 'SELECT dir_id, chapter_id, chapter_sort, chapter_url, chapter_title, chapter_status ' \
              'FROM chapter_ori_info{0} ' \
              'WHERE dir_id = {1} ' \
              'ORDER BY chapter_sort ' \
              'LIMIT {2}'.format(site_id, dir_id, 100)
        try:
            cursor = self.get_cursor('chapter_ori_info{0}'.format(site_id % 2))
            cursor.execute(sql)
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return []

        result = []
        for row in cursor.fetchall():
            result.append(row)
        cursor.close()
        return result


    def get_novelclusterdirinfo_list(self, dir_id_list):
        """
        """
        sql = 'SELECT dir_id FROM novel_cluster_dir_info ' \
              'WHERE dir_id IN ({0})'.format(', '.join("'%d'" % dir_id for dir_id in dir_id_list))
        try:
            cursor = self.get_cursor('novel_cluster_dir_info')
            cursor.execute(sql)
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return []

        result = []
        for (dir_id, ) in cursor.fetchall():
            result.append(dir_id)
        cursor.close()
        return result


    def get_novelclusterdirinfo_gid(self, gid):
        """
        """
        sql = 'SELECT site_id, dir_id, dir_url, gid, book_name, pen_name ' \
              'FROM novel_cluster_dir_info ' \
              'WHERE gid = {0}'.format(gid)
        try:
            cursor = self.get_cursor('novel_cluster_dir_info')
            cursor.execute(sql)
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return []

        result = []
        for row in cursor.fetchall():
            result.append(row)
        cursor.close()
        return result


    def get_novelclusterdirinfo_name(self, key, value):
        """
        """
        sql = "SELECT gid FROM novel_cluster_dir_info WHERE {0} = '{1}'".format(key, value)
        try:
            cursor = self.get_cursor('novel_cluster_dir_info')
            cursor.execute(sql)
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return []

        result = []
        for row in cursor.fetchall():
            result.append(row)
        cursor.close()
        return result


    def update_novelclusterdirinfo(self, update_tuple_list):
        """
        """
        cursor = self.get_cursor('novel_cluster_dir_info')
        sql_prefix = "UPDATE novel_cluster_dir_info " \
                     "SET gid = '%d', book_name = '%s', pen_name = '%s' " \
                     "WHERE dir_id = '%d'"
        for update_tuple in update_tuple_list:
            sql = sql_prefix % update_tuple
            try:
                cursor.execute(sql)
            except Exception, e:
                self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
                continue

        cursor.close()
        return True


    def update_novelclusterdirinfo_gid(self, update_tuple_list):
        """
        """
        cursor = self.get_cursor('novel_cluster_dir_info')
        sql_prefix = "UPDATE novel_cluster_dir_info " \
                     "SET rid = '%d' " \
                     "WHERE gid = '%d'"
        for update_tuple in update_tuple_list:
            sql = sql_prefix % update_tuple
            try:
                cursor.execute(sql)
            except Exception, e:
                self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
                continue

        cursor.close()
        return True


    def insert_novelclusterdirinfo(self, insert_tuple_list):
        """
        """
        sql = 'INSERT IGNORE INTO novel_cluster_dir_info ' \
              '(site_id, site, site_status, ' \
              'dir_id, dir_url, ' \
              'gid, rid, book_name, pen_name, ' \
              'chapter_count, valid_chapter_count, chapter_word_sum) ' \
              'VALUES {0}'.format(', '.join('(%s)' % ', '.join("'%s'" % str(field) for field in tuple) for tuple in insert_tuple_list))
        try:
            cursor = self.get_cursor('novel_cluster_dir_info')
            cursor.execute(sql)
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return False

        cursor.close()
        return True


    def get_novelclusterchapterinfo_gid(self, gid):
        """
        """
        sql = 'SELECT dir_id, chapter_id, chapter_title ' \
              'FROM novel_cluster_chapter_info{0} ' \
              'WHERE gid = {1}'.format(gid % 256, gid)
        try:
            cursor = self.get_cursor('novel_cluster_chapter_info')
            cursor.execute(sql)
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return []

        result = []
        for row in cursor.fetchall():
            result.append(row)
        cursor.close()
        return result



    def insert_novelclusterchapterinfo(self, table_id, insert_tuple_list):
        """
        """
        sql = 'INSERT IGNORE INTO novel_cluster_chapter_info{0} ' \
              '(gid, dir_id, chapter_id, chapter_sort, ' \
              'chapter_url, chapter_title, raw_chapter_title, ' \
              'chapter_status, word_sum) ' \
              'VALUES {1}'.format(table_id, ', '.join('(%s)' % ', '.join("'%s'" % str(field) for field in tuple) for tuple in insert_tuple_list))
        try:
            cursor = self.get_cursor('novel_cluster_chapter_info')
            cursor.execute(sql)
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return False

        cursor.close()
        return True


    def delete_novelclusterchapterinfo(self, table_id, dir_id_list):
        """
        """
        sql = 'DELETE FROM novel_cluster_chapter_info{0} ' \
              'WHERE dir_id IN ({1})'.format(table_id, ', '.join("'%d'" % dir_id for dir_id in dir_id_list))
        try:
            cursor = self.get_cursor('novel_cluster_chapter_info')
            cursor.execute(sql)
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return False

        cursor.close()
        return True


    def get_novelclusteredgeinfo_gid(self, gid):
        """
        """
        sql = 'SELECT gid_x, gid_y, similarity ' \
              'FROM novel_cluster_edge_info ' \
              'WHERE gid_x = {0} OR gid_y = {1}'.format(gid, gid)
        try:
            cursor = self.get_cursor('novel_cluster_edge_info')
            cursor.execute(sql)
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return []

        result = []
        for row in cursor.fetchall():
            result.append(row)
        cursor.close()
        return result


    def delete_novelclusteredgeinfo(self, key_tuple, gid, gid_list):
        """
        """
        sql = 'DELETE FROM novel_cluster_edge_info ' \
              'WHERE {0} = {1} AND {2} IN ({3})'.format(key_tuple[0], gid, key_tuple[1], ', '.join('%d' % gid_y for gid_y in gid_list))
        try:
            cursor = self.get_cursor('novel_cluster_edge_info')
            cursor.execute(sql)
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return False

        cursor.close()
        return True


    def insert_novelclusteredgeinfo(self, insert_tuple_list):
        """
        """
        sql = 'INSERT IGNORE INTO novel_cluster_edge_info ' \
              '(gid_x, gid_y, similarity) ' \
              'VALUES {0}'.format(', '.join('(%s)' % ', '.join("'%s'" % str(field) for field in tuple) for tuple in insert_tuple_list))
        try:
            cursor = self.get_cursor('novel_cluster_edge_info')
            cursor.execute(sql)
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return False

        cursor.close()
        return True


if __name__ == '__main__':
    here()    







