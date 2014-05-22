#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-24 18:43'

from novel.cluster.ClusterDB import *

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

    gid_list = {}.fromkeys([row[0] for row in result]).keys()


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

    result = cluster_db.get_noveldata_all('novel_cluster_dir_info_offline', ['gid', 'rid'])
    new_cluster_result = {}
    for (gid, rid) in result:
        if new_cluster_result.has_key(gid):
            continue
        new_cluster_result[gid] = rid

    for index, gid in enumerate(gid_list):
        old_rid = old_cluster_result[gid]
        new_rid = new_cluster_result[rid]





if __name__ == '__main__':
    init_log('novel')
    init_log('err')

    cluster_db = ClusterDBModule()
    result = cluster_db.get_noveldata_all('novel_cluster_dir_info_offline', ['gid', 'rid'])
    update_gid_dict = {}
    for (gid, rid) in result:
        if gid == rid:
            continue
        if update_gid_dict.has_key(gid):
            continue
        print('gid: {0}, rid: {1}'.format(gid, rid))
        cluster_db.update_novelclusterdirinfo_gid(gid, gid)
        update_gid_dict[gid] = 1






