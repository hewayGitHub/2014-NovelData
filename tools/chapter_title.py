#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-12 18:07'

import MySQLdb
import random

def here():
    print('PrimeMusic')


if __name__ == '__main__':

    conn = MySQLdb.connect(
        host = "127.0.0.1",
        port = 3306,
        user = "root",
        passwd = "root",
        db = "novels"
    )

    for table_id in xrange(0, 256):

        dir_id_list = []
        sql = 'SELECT dir_id FROM novel_cluster_dir_info{0}'.format(table_id)
        cursor = conn.cursor()
        cursor.execute(sql)
        for (dir_id, ) in cursor.fetchall():
            dir_id_list.append(dir_id)
        cursor.close()

        for index in xrange(0, 10):
            dir_id = dir_id_list[random.randint(1, 10000)]

            sql = 'SELECT book_name, pen_name ' \
                  'FROM novel_cluster_dir_info{0} ' \
                  'WHERE dir_id = {1}'.format(dir_id % 256, dir_id)
            cursor = conn.cursor()
            cursor.execute(sql)
            (book_name, pen_name) = cursor.fetchone()
            print('book_name: {0}, pen_name: {1}'.format(book_name, pen_name))
            cursor.close()

            sql = 'SELECT chapter_title, raw_chapter_title, chapter_sort ' \
                  'FROM novel_cluster_chapter_info{0} ' \
                  'WHERE dir_id = {1} ' \
                  'ORDER BY chapter_sort'.format(dir_id % 256, dir_id)
            cursor = conn.cursor()
            cursor.execute(sql)
            for (chapter_title, raw_chapter_title, chapter_sort, ) in cursor.fetchall():
                print('chapter_sort: {0}, chapter_title: {1}, raw_chapter_title: {2}'.format(chapter_sort, chapter_title, raw_chapter_title))
            cursor.close()

            print('---------------------------------------------------------------------------------------')
    conn.close()






