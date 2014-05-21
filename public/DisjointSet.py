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
    def __init__(self, gid = 0, rid = 0):
        """
        """
        self.gid = gid
        self.parent = gid

        self.rid = rid

        self.node_number = 0
        self.authority_node_number = 0


class DisjointSet(object):
    """
    """
    __metaclass__ = Singleton

    def __init__(self):
        """
        """
        self.cluster_node_dict = {}


    def add_novel_node(self, gid = 0, rid = 0, site_status = 0):
        """
        """
        if not self.cluster_node_dict.has_key(gid):
            self.cluster_node_dict[gid] = ClusterNode(gid, rid)
        self.cluster_node_dict[gid].node_number += 1
        self.cluster_node_dict[gid].authority_node_number += site_status


    def get_father(self, gid):
        """
            路径压缩
        """
        cluster_node = self.cluster_node_dict[gid]
        if cluster_node.parent != cluster_node.gid:
            cluster_node.parent = self.get_father(cluster_node.parent)
        return cluster_node.parent


    def check_rank(self, cluster_node_x, cluster_node_y):
        """
            比较两个点大小
        """
        if cluster_node_x.node_number > cluster_node_y.node_number:
            return True
        if cluster_node_x.node_number < cluster_node_y.node_number:
            return False
        if cluster_node_x.authority_node_number > cluster_node_y.authority_node_number:
            return True
        return False


    def merge(self, gid_x, gid_y):
        """
            按秩合并
        """
        gid_x = self.get_father(gid_x)
        gid_y = self.get_father(gid_y)
        if gid_x == gid_y:
            return

        cluster_node_x = self.cluster_node_dict[gid_x]
        cluster_node_y = self.cluster_node_dict[gid_y]
        if self.check_rank(cluster_node_x, cluster_node_y):
            cluster_node_y.parent = cluster_node_x.parent
        else:
            cluster_node_x.parent = cluster_node_y.parent


    def generate_update_tuple_list(self):
        """
        """
        result = []
        for (gid, cluster_node) in self.cluster_node_dict.items():
            rid = self.get_father(gid)
            if cluster_node.gid != rid:
                result.append((gid, rid))
        return result


if __name__ == '__main__':
    here()    







