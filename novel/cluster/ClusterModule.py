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
        self.novel_node_list = []

        parser = SafeConfigParser()
        parser.read('./conf/NovelClusterModule')

        self.authority_site_list = map(int, parser.get('cluster_module', 'authority_site').split(','))


    def cluster_edge_generate(self, table_id, similarity):
        """
        """
        cluster_db = ClusterDBModule()
        result = cluster_db.get_novelclusteredgeinfo_list(table_id, similarity)
        return result


    def cluster_node_generate(self):
        """
        """
        cluster_db = ClusterDBModule()
        disjoint_set = DisjointSet()

        for table_id in xrange(0, 256):
            result = cluster_db.get_novelclusterdirinfo_list(table_id, 'gid, site_id')
            for (dir_id, gid, site_id) in result:
                self.novel_node_list.append((dir_id, gid, site_id))

                rank = 10
                if site_id in self.authority_site_list:
                    rank += 2
                disjoint_set.add_novel_node(gid, rank)


    def cluster_info_update(self):
        """
        """
        cluster_rid_dict = defaultdict(list)

        disjoint_set = DisjointSet()

        for (dir_id, cluster_node) in self.cluster_node_dict.items():
            parent = disjoint_set.get_father(cluster_node)
            cluster_rid_dict[parent].append(cluster_node)


    def run(self):
        """
        """
        self.cluster_node_generate()

        disjoint_set = DisjointSet()

        for similarity in xrange(20, 16, -1):
            for table_id in xrange(0, 256, 1):
                cluster_edge_list = self.cluster_edge_generate(table_id, similarity)


        self.cluster_info_update()



if __name__ == '__main__':
    here()    







