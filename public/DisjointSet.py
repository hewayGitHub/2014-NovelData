#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-17 10:29'

from basic.NovelStructure import *

def here():
    print('PrimeMusic')


class ClusterNode(object):
    """
    """
    def __init__(self, gid = 0):
        """
        """
        self.gid = gid
        self.parent = gid

        self.rank = 0



class DisjointSet(object):
    """
    """
    __metaclass__ = Singleton

    def __init__(self):
        """
        """
        self.cluster_node_dict = {}


    def add_novel_node(self, gid = 0, rank = 10):
        """
        """
        if not self.cluster_node_dict.has_key(gid):
            self.cluster_node_dict[gid] = ClusterNode(gid)
        self.cluster_node_dict[gid].rank += rank


    def get_father(self, gid):
        """
            路径压缩
        """
        node = self.cluster_node_dict[gid]
        if node.parent != node.gid:
            node.parent = self.cluster_node_dict(node.parent)
        return node.parent


    def check_rank(self, nodex, nodey):
        """
            比较两个点大小
        """
        if nodex.rank > nodey.rank:
            return True
        else:
            if nodex.rank == nodey.rank and nodex.gid < nodey.gid:
                return True
            return False


    def merge(self, gidx, gidy):
        """
            按秩合并
        """
        gidx = self.get_father(gidx)
        gidy = self.get_father(gidy)

        if gidx == gidy:
            return

        nodex = self.cluster_node_dict[gidx]
        nodey = self.cluster_node_dict[gidy]

        if self.check_rank(nodex, nodey):
            nodey.parent = nodex.parent
        else:
            nodex.parent = nodey.parent



if __name__ == '__main__':
    here()    







