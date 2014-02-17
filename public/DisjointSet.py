#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-17 10:29'


def here():
    print('PrimeMusic')


class DisjointSet(object):
    """
    """
    def __init__(self):
        """
        """

    def initialize(self, parent, rank):
        """
        """
        self.parent = parent
        self.rank = rank


    def get_father(self, index):
        """
            路径压缩
        """
        if self.parent[index] != index :
            self.parent[index] = self.get_father(self.parent[index])
        return self.parent[index]


    def merge(self, index1, index2):
        """
            按秩合并
        """
        index1 = self.get_father(index1)
        index2 = self.get_father(index2)

        if index1 == index2 :
            return
        if self.rank[index1] > self.rank[index2] :
            self.parent[index2] = index1
            self.rank[index1] += self.rank[index2]
        else :
            self.parent[index1] = index2
            self.rank[index2] += self.rank[index1]


if __name__ == '__main__':
    here()    







