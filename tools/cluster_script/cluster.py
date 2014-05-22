#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-24 18:43'

from novel.cluster.ClusterDB import *
from novel.cluster.ClusterEdgeModule import *
from novel.cluster.NovelSimilarityModule import *

def here():
    print('PrimeMusic')


def init_log(name):
    """
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('./log/{0}.log'.format(name))
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info('{0} log init successful!'.format(name))


def show_cluster_node(gid):
    """
    """
    cluster_db = ClusterDBModule()

    cluster_edge = ClusterEdgeModule()
    cluster_similarity = NovelSimilarityModule()

    cluster_node = cluster_edge.cluster_node_collection(gid)
    virtual_novel_node = cluster_similarity.virtual_novel_node_generate(cluster_node)
    book_name = cluster_node.book_name.encode('GBK', 'ignore')
    pen_name = cluster_node.pen_name.encode('GBK', 'ignore')
    print('gid: {0}, book_name: {1}, pen_name: {2}'.format(gid, book_name, pen_name))
    print(', '.join('%s: %d' % (chapter.chapter_title.encode('GBK', 'ignore'), chapter.rank) for chapter in virtual_novel_node.chapter_list))


def get_rid(gid, table_name):
    """
    """
    cluster_db = ClusterDBModule()

    cursor = cluster_db.get_cursor(table_name)
    sql = 'SELECT rid FROM {0} WHERE gid = {1}'.format(table_name, gid)
    cursor.execute(sql)
    rid_list = {}.fromkeys([row[0] for row in cursor.fetchall()]).keys()
    if len(rid_list) > 1 or len(rid_list) < 1:
        return False

    return rid_list[0]


def get_gid_list(rid, table_name):
    """
    """
    cluster_db = ClusterDBModule()

    cursor = cluster_db.get_cursor(table_name)
    sql = 'SELECT gid FROM {0} WHERE rid = {1}'.format(table_name, rid)
    cursor.execute(sql)
    gid_list = {}.fromkeys([row[0] for row in cursor.fetchall()]).keys()
    return gid_list


def check_diff_rid(gid):
    """
    """
    old_rid = get_rid(gid, 'novel_cluster_dir_info')
    if old_rid is False:
        return False
    new_rid = get_rid(gid, 'novel_cluster_dir_info_offline')
    if new_rid is False:
        return False

    if old_rid == new_rid:
        return True

    old_gid_list = get_gid_list(old_rid, 'novel_cluster_dir_info')
    new_gid_list = get_gid_list(new_rid, 'novel_cluster_dir_info_offline')
    print('new_rid: {0}, old_rid: {1}'.format(new_rid, old_rid))

    print('common_gid:')
    for old_gid in old_gid_list:
        if old_gid in new_gid_list:
            show_cluster_node(old_gid)


    print('old_gid_only:')
    for old_gid in old_gid_list:
        if old_gid in new_gid_list:
            continue
        show_cluster_node(old_gid)

    print('new_gid_only:')
    for new_gid in new_gid_list:
        if new_gid in old_gid_list:
            continue
        show_cluster_node(new_gid)

    print('')
    return False


def check_cluster_diff():
    """
    """
    gid_list = [int(line.strip()) for line in open('./data/rid.txt', 'r').readlines()]
    for index, gid in enumerate(gid_list):
        check_diff_rid(gid)


if __name__ == '__main__':
    init_log('novel')
    init_log('err')

    check_cluster_diff()




