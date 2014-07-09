#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-17 00:40'

from collections import defaultdict
from ConfigParser import SafeConfigParser

from novel.cluster.ClusterDB import *
from public.DisjointSet import *

def here():
    print('PrimeMusic')


class ClusterModule(object):
    """
    """
    def __init__(self):
        """
        """
        self.logger = logging.getLogger('novel.cluster')
        self.err = logging.getLogger('err.cluster')


    def novel_node_collection(self):
        """
        """
        cluster_db = ClusterDBModule()
        novel_node_list = cluster_db.get_noveldata_all('novel_cluster_dir_info_offline', ['gid', 'rid', 'site_status'])
        self.logger.info('novel node number: {0}'.format(len(novel_node_list)))
        disjoint_set = DisjointSet()
        for (gid, rid, site_status) in novel_node_list:
            disjoint_set.add_novel_node(gid, rid, site_status)

        rid_list = []
        for table_id in xrange(0, 256):
            result = cluster_db.get_novelaggregationdir_rid(table_id)
            rid_list.extend(result)
        self.logger.info('novel authority node number: {0}'.format(len(rid_list)))
        for rid in rid_list:
            disjoint_set.agg_novel_node_rank(rid)


    def novel_edge_collection(self):
        """
        """
        cluster_db = ClusterDBModule()
        novel_edge_list = cluster_db.get_noveldata_all('novel_cluster_edge_info_offline', ['gid_x', 'gid_y'])
        self.logger.info('novel edge number: {0}'.format(len(novel_edge_list)))

        disjoint_set = DisjointSet()
        for (gid_x, gid_y) in novel_edge_list:
            disjoint_set.merge(gid_x, gid_y)


    def novel_cluster_update(self):
        """
        """
        disjoint_set = DisjointSet()
        update_tuple_list = disjoint_set.generate_update_tuple_list()
        self.logger.info('novel cluster update number: {0}'.format(len(update_tuple_list)))

        cluster_db = ClusterDBModule()
        for index, (gid, rid) in enumerate(update_tuple_list):
            self.logger.info('index: {0}/{1}, gid: {2}, rid: {3}'.format(index, len(update_tuple_list), gid, rid))
            cluster_db.update_novelclusterdirinfo_gid(gid, rid)


    def run(self):
        """
        """
        self.logger.info('novel cluster module start')

        self.novel_node_collection()
        self.novel_edge_collection()
        self.novel_cluster_update()

        self.logger.info('novel cluster module end')
        return True



if __name__ == '__main__':
    here()




