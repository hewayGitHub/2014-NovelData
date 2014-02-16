#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-16 18:31'


import MySQLdb
import random

from novel.cluster.ClusterNodeModule import *
from novel.cluster.NovelSimilarityModule import *

def here():
    print('PrimeMusic')


def get_novel_node(conn, dir_id):
    """
    """
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
        novel_node.chapter_list[-1].chapter_title = chapter_title.decode('GBK', 'ignore') 
    cursor.close()

    return novel_node

def print_novel_node(novel_node, dir_id):
    """
    """
    print('book_name: {0}, pen_name: {1}, dir_id: {2}'.format(novel_node.book_name.encode('GBK', 'ignore'), novel_node.pen_name.encode('GBK', 'ignore'), dir_id))
    print(', '.join('%s' % chapter.chapter_title.encode('GBK') for chapter in novel_node.chapter_list))
    print(', '.join('%s' % chapter.raw_chapter_title.encode('GBK') for chapter in novel_node.chapter_list))
    

if __name__ == '__main__':


    conn = MySQLdb.connect(
        host = "127.0.0.1",
        port = 3306,
        user = "root",
        passwd = "root",
        db = "novels"
    )


    dir_id_list = []
    sql = 'SELECT dir_id FROM novel_cluster_dir_info0'
    cursor = conn.cursor()
    cursor.execute(sql)
    for (dir_id, ) in cursor.fetchall():
        dir_id_list.append(dir_id)
    cursor.close()


    for index in xrange(0, 10):
        print('-----------------------------------------------------')
        dir_id = dir_id_list[random.randint(1, 10000)]

        novel_node = get_novel_node(conn, dir_id)

        id_list = []
        for table_id in xrange(1, 256):
            sql = 'SELECT dir_id FROM novel_cluster_dir_info{0} WHERE book_name = "{1}"'.format(table_id, novel_node.book_name.encode('GBK'))
            cursor = conn.cursor()
            cursor.execute(sql)
            for (id, ) in cursor.fetchall():
                id_list.append(id)
            cursor.close()
        
        if len(id_list) == 0:
            continue
        print_novel_node(novel_node, dir_id)
        similarity = NovelSimilarityModule()
        for id in id_list:
            node = get_novel_node(conn, id)
            print_novel_node(node, id)
            print(similarity.novel_node_similarity_calculation(novel_node, node))
            novel_node = node




    conn.close()


    here()    







