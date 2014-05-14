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
        """
        similarity, match_list = self.novel_node_similarity_calculation(virtual_novel_node, novel_node)
        if similarity < 0.7:
            return False

        virtual_novel_node.rank += 1
        for index, chapter in enumerate(novel_node.chapter_list):
            if match_list[index] == -1:
                chapter.rank = 1
                virtual_novel_node.chapter_list.append(chapter)
            else:
                match_chapter = virtual_novel_node.chapter_list[match_list[index]]
                match_chapter.rank += 1
        return True


    def virtual_novel_chapter_generate(self, virtual_novel_node):
        """
            一个虚拟节点计算产生虚拟目录
        """
        threshold = 1
        left = min([chapter.rank for chapter in virtual_novel_node.chapter_list])
        right = max([chapter.rank for chapter in virtual_novel_node.chapter_list])
        while left <= right:
            mid = (left + right) / 2
            number = sum([1 for chapter in virtual_novel_node.chapter_list if chapter.rank >= mid])
            if number >= 60:
                threshold = mid
                left = mid + 1
            else:
                right = mid - 1
        virtual_novel_node.chapter_list = [chapter for chapter in virtual_novel_node.chapter_list if chapter.rank >= threshold]
        return True


    def debug_novel_node(self, novel_node):
        """
        """
        print(novel_node.rank)
        print(', '.join('%s: %d' % (chapter.chapter_title.encode('GBK', 'ignore'), chapter.rank) for chapter in novel_node.chapter_list))


    def virtual_novel_node_generate(self, novel_cluster_node):
        """
            一个簇计算产生一个虚拟节点
        """
        novel_node_list = novel_cluster_node.novel_node_list
        sorted(novel_node_list, lambda a, b: cmp(len(b.chapter_list), len(a.chapter_list)))

        virtual_novel_node_list = []
        for novel_node in novel_node_list:
            flag = False
            for index, virtual_novel_node in enumerate(virtual_novel_node_list):
                flag = self.virtual_novel_node_merge(virtual_novel_node, novel_node)
                if flag is True:
                    break
            if flag is False:
                novel_node.rank = 1
                for chapter in novel_node.chapter_list:
                    chapter.rank = 1
                virtual_novel_node_list.append(novel_node)

        max_virtual_novel_node = virtual_novel_node_list[0]
        for virtual_novel_node in virtual_novel_node_list:
            self.debug_novel_node(virtual_novel_node)
            if virtual_novel_node.rank > max_virtual_novel_node.rank:
                max_virtual_novel_node = virtual_novel_node

        self.virtual_novel_chapter_generate(max_virtual_novel_node)
        return max_virtual_novel_node


    def novel_cluster_similarity_calculation(self, novel_cluster_x, novel_cluster_y):
        """
            计算两个gid的相似度
        """
        virtual_novel_node_x = self.virtual_novel_node_generate(novel_cluster_x)
        virtual_novel_node_y = self.virtual_novel_node_generate(novel_cluster_y)

        similarity, match_list = self.novel_node_similarity_calculation(virtual_novel_node_x, virtual_novel_node_y)
        return similarity



if __name__ == '__main__':
    here()    







