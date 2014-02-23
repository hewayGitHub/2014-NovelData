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
        short_list = novel_node_x.chapter_list
        long_list = novel_node_y.chapter_list
        if len(novel_node_x.chapter_list) > len(novel_node_y.chapter_list):
            short_list = novel_node_y.chapter_list
            long_list = novel_node_x.chapter_list

        similarity_matirx = defaultdict(list)
        for index_x, chapter_x in enumerate(short_list):
            if chapter_x.chapter_title == '':
                continue
            for index_y, chapter_y in enumerate(long_list):
                chapter_similarity = self.novel_chapter_similarity_calculation(chapter_x, chapter_y)
                if chapter_similarity >= 0.7:
                    similarity_matirx[index_x].append(index_y)

        match = BipartiteGraph()
        match_number = match.bipartite_graph_max_match(len(short_list), len(long_list), similarity_matirx)
        similarity = match_number * 1.0 / len(short_list)
        return similarity


    def novel_cluster_similarity_calculation(self, novel_cluster_x, novel_cluster_y):
        """
            计算两个gid的相似度
        """
        short_list = novel_cluster_x.novel_node_list
        long_list = novel_cluster_y.novel_node_list
        if len(novel_cluster_x.novel_node_list) > len(novel_cluster_y.novel_node_list):
            short_list = novel_cluster_y.novel_node_list
            long_list = novel_cluster_x.novel_node_list

        similarity_matrix = defaultdict(list)
        for index_x, novel_node_x in enumerate(short_list):
            for index_y, novel_node_y in enumerate(long_list):
                novel_similarity = self.novel_node_similarity_calculation(novel_node_x, novel_node_y)
                if novel_similarity >= 0.7:
                    similarity_matrix[index_x].append(index_y)

        match = BipartiteGraph()
        match_number = match.bipartite_graph_max_match(len(short_list), len(long_list), similarity_matrix)
        similarity = match_number * 1.0 / len(short_list)

        return similarity


if __name__ == '__main__':
    here()    







