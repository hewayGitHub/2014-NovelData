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


if __name__ == '__main__':
    init_log('novel')
    init_log('err')

    cluster_db = ClusterDBModule()
    result = cluster_db.get_noveldata_all('novel_cluster_dir_info_offline', ['gid', 'rid'])
    for (gid, rid) in result:
        print('gid: {0}, rid: {1}'.format(gid, rid))
        cluster_db.update_novelclusterdirinfo_gid(gid, gid)








