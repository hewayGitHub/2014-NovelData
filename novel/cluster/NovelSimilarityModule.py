#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-11 15:42'

from basic.NovelStructure import *
from public.BasicStringMethod import *

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
        similarity = 0
        return similarity


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







