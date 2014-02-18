#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-17 00:40'


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
        self.cluster_node_dict = None


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

        for table_id in xrange(0, 256):
            result = cluster_db.get_novelclusterdirinfo_list(table_id, 'gid')
            for (dir_id, gid) in result:
                cluster_node = ClusterNode(dir_id, gid)
                self.cluster_node_dict[dir_id] = cluster_node


    def cluster_info_update(self):
        """
        """


    def run(self):
        """
        """
        self.cluster_node_generate()

        disjoint_set = DisjointSet()
        disjoint_set.initialize(self.cluster_node_dict)

        for similarity in xrange(20, 16, -1):
            for table_id in xrange(0, 256, 1):
                cluster_edge_list = self.cluster_edge_generate(table_id, similarity)
                for (dir_id_i, dir_id_j) in cluster_edge_list:
                    nodex = self.cluster_node_dict[dir_id_i]
                    nodey = self.cluster_node_dict[dir_id_j]
                    disjoint_set.merge(nodex, nodey)

        self.cluster_info_update()



if __name__ == '__main__':
    here()    







