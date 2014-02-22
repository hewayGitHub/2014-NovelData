#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-16 17:09'

from basic.NovelStructure import *

def here():
    print('PrimeMusic')


class BipartiteGraph(object):
    """
        ����ͼ
    """
    __metaclass__ = Singleton

    def initialize(self, m, edge):
        """
            ��ʼ������
        """
        self.match = [-1] * m
        self.visit = [False] * m

        self.edge = edge


    def visit_clean(self, m):
        """
            ����ϴ������ı��
        """
        for index in xrange(0, m):
            self.visit[index] = False


    def find_path(self, u):
        """
            Ѱ������·��
        """
        for v in self.edge[u]:
            if self.visit[v]:
                continue
            self.visit[v] = True
            if self.match[v] == -1 or self.find_path(self.match[v]):
                self.match[v] = u
                return True
        return False


    def bipartite_graph_max_match(self, n, m, edge):
        """
            �����ͼ�����ƥ��
        """
        self.initialize(m, edge)

        match_number = 0
        for u in xrange(0, n):
            self.visit_clean(m)
            if self.find_path(u):
                match_number += 1

        return match_number


if __name__ == '__main__':

    max_match = BipartiteGraph()
    edge = {}
    edge[0] = [0]
    edge[1] = [1, 2]
    edge[2] = [1, 3]
    edge[3] = [2]
    edge[4] = [3]
    print(max_match.bipartite_graph_max_match(5, 5, edge))

    here()    







