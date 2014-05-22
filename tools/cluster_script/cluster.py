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


def show_cluster_node(rid):
    """
    """
    cluster_db = ClusterDBModule()
    result = cluster_db.get_novelclusterdirinfo_name('rid', rid)

    cluster_edge = ClusterEdgeModule()
    cluster_similarity = NovelSimilarityModule()
    gid_list = {}.fromkeys([row[0] for row in result]).keys()
    print('rid: {0}'.format(rid))
    for index, gid in enumerate(gid_list):
        cluster_node = cluster_edge.cluster_node_collection(gid)
        virtual_novel_node = cluster_similarity.virtual_novel_node_generate(cluster_node)
        book_name = cluster_node.book_name.encode('GBK', 'ignore')
        pen_name = cluster_node.pen_name.encode('GBK', 'ignore')
        print('gid: {0}, book_name: {1}, pen_name: {2}'.format(gid, book_name, pen_name))
        print(', '.join("'%s'" % (chapter.chapter_title.encode('GBK', 'ignore') for chapter in virtual_novel_node.chapter_list)))


def check_cluster_diff():
    """
    """
    cluster_db = ClusterDBModule()
    gid_list = [int(line.strip()) for line in open('./data/rid.txt', 'r').readlines()]

    result = cluster_db.get_noveldata_all('novel_cluster_dir_info', ['gid', 'rid'])
    old_cluster_result = {}
    for (gid, rid) in result:
        if old_cluster_result.has_key(gid):
            continue
        old_cluster_result[gid] = rid
    here()

    result = cluster_db.get_noveldata_all('novel_cluster_dir_info_offline', ['gid', 'rid'])
    new_cluster_result = {}
    for (gid, rid) in result:
        if new_cluster_result.has_key(gid):
            continue
        new_cluster_result[gid] = rid
    here()

    for index, gid in enumerate(gid_list):
        if not old_cluster_result.has_key(gid):
            continue
        if not new_cluster_result.has_key(gid):
            continue
        old_rid = old_cluster_result[gid]
        new_rid = new_cluster_result[gid]
        if old_rid == new_rid:
            continue
        print('gid: {0}, old_rid: {1}, new_rid: {2}'.format(gid, old_rid, new_rid))
        show_cluster_node(old_rid)
        show_cluster_node(new_rid)


if __name__ == '__main__':
    init_log('novel')
    init_log('err')

    check_cluster_diff()




