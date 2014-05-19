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
    field_list = ['site_id', 'site', 'site_status',
                  'dir_id', 'dir_url',
                  'gid', 'rid', 'book_name', 'pen_name',
                  'chapter_count', 'chapter_word_sum', 'last_chapter_title']
    result = cluster_db.get_noveldata_all('novel_cluster_dir_info', field_list)
    insert_tuple_list = []
    for insert_tuple in result:
        insert_tuple_list.append(insert_tuple)
        if len(insert_tuple_list) == 100:
            cluster_db.insert_novelclusterdirinfo(insert_tuple_list)
            insert_tuple_list = []

    if len(insert_tuple_list) > 0:
        cluster_db.insert_novelclusterdirinfo(insert_tuple_list)





