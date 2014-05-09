#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-12 18:07'

import MySQLdb
import random

def here():
    print('PrimeMusic')


def chapter_title_debug(conn, gid):
    """
    """
    cursor = conn.cursor()

    dir_list = []
    sql = 'SELECT site, site_id, dir_id, dir_url FROM novel_cluster_dir_info WHERE gid = {0}'.format(gid)
    cursor.execute(sql)
    for (site, site_id, dir_id, dir_url) in cursor.fetchall():
        dir_list.append((site, site_id, dir_id, dir_url))

    for (site, site_id, dir_id, dir_url) in dir_list:
        print('site: {0}, site_id, {1}, dir_id: {2}, dir_url: {3}'.format(site_id, site_id, dir_id, dir_url))
        sql = 'SELECT chapter_sort, chapter_title, raw_chapter_title ' \
              'FROM novel_cluster_chapter_info{0} ' \
              'WHERE dir_id = {1} ' \
              'ORDER BY chapter_sort'.format(gid % 256, dir_id)

        chapter_title_list = []
        cursor.execute(sql)
        for (chapter_sort, chapter_title, raw_chapter_title) in cursor.fetchall():
            chapter_title_list.append(chapter_title)
        print(', '.join('%s' % chapter_title for chapter_title in chapter_title_list))
        print('')

    cursor.close()


if __name__ == '__main__':

    conn = MySQLdb.connect(
        host = "10.46.7.114",
        port = 6216,
        user = "novelclu1_w",
        passwd = "OrEYBymP3gb3D8Ic",
        db = "novels"
    )
    chapter_title_debug(conn, 534588203)

    conn.close()

