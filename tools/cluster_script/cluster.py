#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-24 18:43'

import MySQLdb
import random
from basic.NovelStructure import *

def here():
    print('PrimeMusic')


def get_cluster_node(cursor, rid):
    """
    """
    novel_node_list = []
    sql = 'SELECT dir_id, dir_url, gid, book_name, pen_name FROM novel_cluster_dir_info ' \
          'WHERE rid = {0}'.format(rid)
    cursor.execute(sql)
    for (dir_id, dir_url, gid, book_name, pen_name) in cursor.fetchall():
        novel_node = NovelNodeInfo(dir_id = dir_id, dir_url = dir_url, gid = gid, book_name = book_name, pen_name = pen_name)
        novel_node_list.append(novel_node)

    gid_number = len({}.fromkeys([novel_node.gid for novel_node in novel_node_list]).keys())
    if gid_number == 1:
        return

    for novel_node in novel_node_list:
        sql = 'SELECT chapter_title FROM novel_cluster_chapter_info{0} ' \
              'WHERE dir_id = {1}'.format(novel_node.gid % 256, novel_node.dir_id)
        cursor.execute(sql)
        chapter_title_list = []
        for (chapter_title, ) in cursor.fetchall():
            chapter_title_list.append(chapter_title)

        print('book_name: {0}, pen_name: {1}, dir_url: {2}'.format(novel_node.book_name, novel_node.pen_name, novel_node.dir_url))
        print(', '.join('%s' % chapter_title for chapter_title in chapter_title_list))


if __name__ == '__main__':
    conn = MySQLdb.connect(
        host = "127.0.0.1",
        port = 3306,
        user = "root",
        passwd = "root",
        db = "novels"
    )
    cursor = conn.cursor()

    for index in xrange(0, 10):
        id = random.randint(1, 2000000)
        sql = 'SELECT rid FROM novel_cluster_dir_info WHERE id = {0}'.format(id)
        cursor.execute(sql)
        (rid, ) = cursor.fetchone()
        print()
        print()
        print('rid: {0}'.format(rid))
        get_cluster_node(cursor, rid)
