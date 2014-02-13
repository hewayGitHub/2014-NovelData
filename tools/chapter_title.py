#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-12 18:07'

import MySQLdb
import random

from novel.cluster.NovelCleanModule import *

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
            novel_node = NovelNodeInfo(book_name = book_name.decode('GBK', 'ignore'), pen_name = pen_name.decode('GBK', 'ignore'))
            novel_node.chapter_list = []
            cursor.close()

            sql = 'SELECT chapter_title, raw_chapter_title, chapter_sort ' \
                  'FROM novel_cluster_chapter_info{0} ' \
                  'WHERE dir_id = {1} ' \
                  'ORDER BY chapter_sort'.format(dir_id % 256, dir_id)
            cursor = conn.cursor()
            cursor.execute(sql)
            for (chapter_title, raw_chapter_title, chapter_sort, ) in cursor.fetchall():
                novel_node.chapter_list.append(NovelChapterInfo(chapter_title = raw_chapter_title.decode('GBK', 'ignore')))
            cursor.close()

            print('book_name: {0}, pen_name: {1}'.format(novel_node.book_name.encode('GBK', 'ignore'), novel_node.pen_name.encode('GBK', 'ignore')))
            for chapter in novel_node.chapter_list:
                print('chapter_title: {0}, raw_chapter_title: {1}'.format(chapter.chapter_title.encode('GBK', 'ignore'), chapter.raw_chapter_title.encode('GBK', 'ignore')))

            print('---------------------------------------------------------------------------------------')
    conn.close()






