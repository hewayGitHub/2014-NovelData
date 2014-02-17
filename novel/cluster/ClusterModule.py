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


    def cluster_edge_generate(self):
        """
        """

    def cluster_node_generate(self):
        """
        """
        cluster_db = ClusterDBModule()

        for table_id in xrange(0, 256):
            result = cluster_db.get_novelclusterdirinfo_list(table_id, 'gid')
            for (dir_id, gid) in result:
                cluster_node = ClusterNode(dir_id, gid)
                self.cluster_node_dict[dir_id] = cluster_node


    def run(self):
        """
        """



if __name__ == '__main__':
    here()    







