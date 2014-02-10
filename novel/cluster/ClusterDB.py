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

    def get_dirfmtinfo_id_list(self, site_id, update_time):
        """
        """
        conn = self.buid_connection('dir_fmt_info')
        sql = 'SELECT id FROM dir_fmt_info{0} WHERE update_time > {1}'.format(site_id, update_time)
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return []

        result = []
        for (id, ) in cursor.fetchall():
            result.append(id)
        cursor.close()
        conn.close()
        return result

    def get_dirfmtinfo_info(self, site_id, novel_id):
        """
        """
        conn = self.buid_connection('dir_fmt_info')
        sql = 'SELECT site_id, site, site_status, dir_id, dir_url, gid, book_name, pen_name ' \
              'FROM dir_fmt_info{0} ' \
              'WHERE id = {1}'.format(site_id, novel_id)
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return False

        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    def get_chapteroriinfo_list(self, site_id, dir_id):
        """
        """
        conn = self.buid_connection('chapter_ori_info{0}'.format(site_id % 2))
        sql = 'SELECT dir_id, chapter_id, chapter_sort, chapter_url, chapter_title, chapter_status ' \
              'FROM chapter_ori_info{0} ' \
              'WHERE dir_id = {1} ' \
              'ORDER BY chapter_sort ' \
              'LIMIT {2}'.format(site_id, dir_id, 100)
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return []

        result = []
        for row in cursor.fetchall():
            result.append(row)
        cursor.close()
        conn.close()
        return result

    def get_novelclusterdirinfo_info(self, dir_id):
        """
        """
        conn = self.buid_connection('novel_cluster_dir_info')
        sql = 'SELECT site_id, site, site_status, dir_id, dir_url, gid, book_name, pen_name ' \
              'FROM novel_cluster_dir_info{0} ' \
              'WHERE dir_id = {1}'.format(dir_id % 256, dir_id)
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return False

        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    def get_novelclusterchapterinfo_list(self, dir_id):
        """
        """
        conn = self.buid_connection('novel_cluster_chapter_info')
        sql = 'SELECT dir_id, chapter_id, chapter_sort, chapter_url, chapter_title, chapter_status ' \
              'FROM novel_cluster_chapter_info{0} ' \
              'WHERE dir_id = {1}'.format(dir_id % 256, dir_id)
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return []

        result = []
        for row in cursor.fetchall():
            result.append(row)
        cursor.close()
        conn.close()
        return result

    def insert_novelclusterdirinfo(self, dir_id, tuple):
        """
        """
        conn = self.buid_connection('novel_cluster_dir_info')
        sql = 'INSERT IGNORE INTO novel_cluster_dir_info{0} ' \
              '(site_id, site, site_status, ' \
              'dir_id, dir_url, ' \
              'gid, book_name, pen_name, ' \
              'chapter_count, valid_chapter_count, chapter_word_sum) ' \
              'VALUES ({1})'.format(dir_id % 256, ', '.join("'%s'" % str(filed) for filed in tuple))
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            cursor.commit()
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return False

        cursor.close()
        conn.close()
        return True

    def delete_novelclusterdirinfo(self, dir_id):
        """
        """
        conn = self.buid_connection('novel_cluster_dir_info')
        sql = 'DELETE FROM novel_cluster_dir_info{0} ' \
              'WHERE dir_id = {1}'.format(dir_id % 256, dir_id)
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            cursor.commit()
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return False

        cursor.close()
        conn.close()
        return True

    def insert_novelclusterchapterinfo_list(self, dir_id, tuple_list):
        """
        """
        conn = self.buid_connection('novel_cluster_chapter_info')
        sql = 'INSERT IGNORE INTO novel_cluster_chapter_info{0} ' \
              '(dir_id, chapter_id, chapter_sort, ' \
              'chapter_url, chapter_title, raw_chapter_title, ' \
              'chapter_status, word_sum) ' \
              'VALUES {1}'.format(dir_id % 256, ', '.join('(%s)' % ', '.join("'%s'" % str(field) for field in tuple) for tuple in tuple_list))
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            cursor.commit()
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return False

        cursor.close()
        conn.close()
        return True

    def delete_novelclusterchapterinfo_list(self, dir_id):
        """
        """
        conn = self.buid_connection('novel_cluster_chapter_info')
        sql = 'DELETE FROM novel_cluster_chapter_info{0} ' \
              'WHERE dir_id = {1}'.format(dir_id % 256, dir_id)
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            cursor.commit()
        except Exception, e:
            self.err.warning('[sql: {0}, error: {1}]'.format(sql, e))
            return False

        cursor.close()
        conn.close()
        return True



if __name__ == '__main__':
    here()    







