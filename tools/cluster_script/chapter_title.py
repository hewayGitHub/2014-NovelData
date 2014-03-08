#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-12 18:07'

import MySQLdb
import random

from basic.NovelStructure import *
from novel.cluster.NovelCleanModule import *

def here():
    print('PrimeMusic')


def chapter_clean_debug(conn):
    """
    """
    cursor = conn.cursor()

    novel_node = NovelNodeInfo(book_name = u'诱宠宝贝乖乖乖', pen_name = u'夏伊儿')
    novel_node.chapter_list = []

    sql = 'SELECT raw_chapter_title FROM novel_cluster_chapter_info212 WHERE dir_id = 4130465196533952379'
    cursor.execute(sql)
    for (raw_chapter_title, ) in cursor.fetchall():
        chapter = NovelChapterInfo(chapter_title = raw_chapter_title.decode('GBK', 'ignore'))
        novel_node.chapter_list.append(chapter)
    cursor.close()

    novel_clean = NovelCleanModule()
    novel_clean.novel_chapter_clean(novel_node)

    for chapter in novel_node.chapter_list:
        print('{chapter_title: {0}, raw_chapter_title: {1}}'.format(chapter.chapter_title.encode('GBK', 'ignore'), chapter.raw_chapter_title.encode('GBK', 'ignore')))


if __name__ == '__main__':

    here()

    conn = MySQLdb.connect(
        host = "127.0.0.1",
        port = 3306,
        user = "root",
        passwd = "root",
        db = "novels"
    )

    chapter_clean_debug(conn)

    conn.close()

