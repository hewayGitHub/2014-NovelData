#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-11 15:42'

from collections import defaultdict

from basic.NovelStructure import *
from public.BasicStringMethod import *
from public.BipartiteGraph import *
from tools.debug import *

def here():
    print('PrimeMusic')

class NovelSimilarityModule(object):
    """
        小说相似度计算模块
    """
    __metaclass__ = Singleton

    def novel_chapter_similarity_calculation(self, chapter_x, chapter_y):
        """
            计算两个章节的相似性
        """
        return string_similarity(chapter_x.chapter_title, chapter_y.chapter_title)


    def novel_node_similarity_calculation(self, novel_node_x, novel_node_y):
        """
            计算两本小说的相似性
        """
        long_list = novel_node_x.chapter_list
        short_list = novel_node_y.chapter_list
        if len(novel_node_y.chapter_list) > len(novel_node_x.chapter_list):
            long_list = novel_node_y.chapter_list
            short_list = novel_node_x.chapter_list

        similarity_matirx = defaultdict(list)
        for index_x, chapter_x in enumerate(long_list):
            if chapter_x.chapter_title == '':
                continue
            for index_y, chapter_y in enumerate(short_list):
                chapter_similarity = self.novel_chapter_similarity_calculation(chapter_x, chapter_y)
                if chapter_similarity >= 0.7:
                    similarity_matirx[index_x].append(index_y)

        match = BipartiteGraph()
        match_number, match_list = match.bipartite_graph_max_match(len(long_list), len(short_list), similarity_matirx)
        similarity = match_number * 1.0 / len(short_list)
        return similarity, match_list


    def virtual_novel_node_merge(self, virtual_novel_node, novel_node):
        """
            一个普通节点和一个虚拟节点合并，不能合并返回false
            默认：virtual_novel_node的章节长度大于novel_node的章节长度
        """
        similarity, match_list = self.novel_node_similarity_calculation(virtual_novel_node, novel_node)
        if similarity < 0.7:
            return False


        return True


    def virtual_novel_node_generate(self, novel_cluster_node):
        """
            一个簇计算产生一个虚拟节点
        """
        novel_node_list = novel_cluster_node.novel_node_list
        sorted(novel_node_list, lambda a, b: cmp(len(b.chapter_list), len(a.chapter_list)))

        virtual_node_list = []
        for novel_node in novel_node_list:
            flag = False
            for index, virtual_novel_node in enumerate(virtual_node_list):
                flag = self.virtual_novel_node_merge(virtual_novel_node, novel_node)
                if flag:
                    break
            if not flag:
                virtual_novel_node = novel_node
                virtual_novel_node.rank = 1
                virtual_novel_node.chapter_weight_list = [1] * len(novel_node.chapter_list)
                virtual_node_list.append(virtual_novel_node)


    def novel_cluster_similarity_calculation(self, novel_cluster_x, novel_cluster_y):
        """
            计算两个gid的相似度
        """


if __name__ == '__main__':
    here()    







