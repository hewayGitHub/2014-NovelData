#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-16 17:09'


def here():
    print('PrimeMusic')


class BipartiteGraph(object):
    """
        二分图
    """
    def __init__(self):
        """
        """
        self.visit = []
        self.match = []


    def initialize(self, m, edge):
        """
            初始化操作
        """
        for index in xrange(0, m):
            self.match.append(-1)
            self.visit.append(False)

        self.edge = edge
        self.max_match = 0


    def visit_clean(self, m):
        """
            清空上次搜索的标记
        """
        for index in xrange(0, m):
            self.visit[index] = False


    def find_path(self, u):
        """
            寻找增广路径
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
            求二分图的最大匹配
        """
        self.initialize(m, edge)

        for u in xrange(0, n):
            self.visit_clean(m)

            if self.find_path(u):
                self.max_match += 1

        return self.max_match



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







