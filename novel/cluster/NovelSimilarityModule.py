#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-11 15:42'

from collections import defaultdict

from basic.NovelStructure import *
from public.BasicStringMethod import *
from public.BipartiteGraph import *

def here():
    print('PrimeMusic')

class NovelSimilarityModule(object):
    """
        计算两本小说的相似性
    """
    __metaclass__ = Singleton

    def __init__(self):
        """
        """

    def chapter_similarity_calculation(self, chapter_x, chapter_y):
        """
            计算两个章节的相似性
        """
        return string_similarity(chapter_x.chapter_title, chapter_y.chapter_title)


    def chapter_list_similarity_calculation(self, chapter_list_x, chapter_list_y):
        """
            计算两个章节列表的相似性
        """
        short_list = chapter_list_x
        long_list = chapter_list_y

        if len(chapter_list_x) > len(chapter_list_y):
            short_list = chapter_list_y
            long_list = chapter_list_x

        begin_match = len(short_list) - 1
        end_match = 0
        similarity_matirx = defaultdict(list)

        for index_x, chapter_x in enumerate(short_list):
            flag = False
            for index_y, chapter_y in enumerate(long_list):
                chapter_similarity = self.chapter_similarity_calculation(chapter_x, chapter_y)
                if chapter_similarity >= 0.8:
                    flag = True
                    similarity_matirx[index_x].append(index_y)
            if flag:
                begin_match = min(begin_match, index_x)
                end_match = max(end_match, index_x)
        if begin_match > end_match:
            return 0

        match = BipartiteGraph()
        match_number = match.bipartite_graph_max_match(len(short_list), len(long_list), similarity_matirx)

        similarity = match_number * 10.0 / (end_match - begin_match + 1)

        return int(similarity)


    def novel_node_similarity_calculation(self, novel_node_x, novel_node_y):
        """
            计算两本小说的相似性
        """
        novel_similarity = self.chapter_list_similarity_calculation(novel_node_x.chapter_list, novel_node_y.chapter_list)
        if novel_node_x.book_name == novel_node_y.book_name:
            novel_similarity += 10
        if novel_node_x.pen_name == novel_node_y.pen_name:
            novel_similarity += 10
        return novel_similarity


if __name__ == '__main__':
    here()    







