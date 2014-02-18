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
    def __init__(self, dir_id = 0, gid = 0):
        """
        """
        self.dir_id = dir_id
        self.gid = gid

        self.parent = dir_id
        self.rand = 1



class DisjointSet(object):
    """
    """
    __metaclass__ = Singleton

    def initialize(self, cluster_node_dict):
        """
        """
        self.cluster_node_dict = cluster_node_dict


    def get_father(self, node):
        """
            路径压缩
        """
        if node.parent != node.dir_id:
            node.parent = self.get_father(self.cluster_node_dict[node.parent])
        return node.parent


    def merge(self, nodex, nodey):
        """
            按秩合并
        """
        nodex.parent = self.get_father(nodex)
        nodey.parent = self.get_father(nodey)

        if nodex.parent == nodey.parent:
            return
        if nodex.rank > nodey.rank:
            nodey.parent = nodex.parent
            nodex.rank += nodey.rank
        else:
            nodex.parent = nodey.parent
            nodey.rank += nodex.rank

    def

if __name__ == '__main__':
    here()    







