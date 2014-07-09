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
        min_length = min(len(novel_node_x.chapter_list), len(novel_node_y.chapter_list))
        if min_length <= 2:
            return 0.0, []

        similarity_matirx = defaultdict(list)
        for index_x, chapter_x in enumerate(novel_node_x.chapter_list):
            if len(chapter_x.chapter_title) == 0:
                continue
            for index_y, chapter_y in enumerate(novel_node_y.chapter_list):
                if len(chapter_y.chapter_title) == 0:
                    continue
                chapter_similarity = self.novel_chapter_similarity_calculation(chapter_x, chapter_y)
                if chapter_similarity >= 0.8:
                    similarity_matirx[index_x].append(index_y)

        match = BipartiteGraph()
        match_number, match_list = match.bipartite_graph_max_match(
            len(novel_node_x.chapter_list),
            len(novel_node_y.chapter_list),
            similarity_matirx
        )
        similarity = match_number * 1.0 / min_length
        return similarity, match_list


    def virtual_novel_node_merge(self, virtual_novel_node, novel_node):
        """
            一个普通节点和一个虚拟节点合并，不能合并返回false
        """
        similarity, match_list = self.novel_node_similarity_calculation(virtual_novel_node, novel_node)
        if similarity < 0.7:
            return False

        virtual_novel_node.rank += novel_node.site_status + 1
        for index, chapter in enumerate(novel_node.chapter_list):
            if match_list[index] == -1:
                continue
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

        real_chapter_number = len([chapter for chapter in virtual_novel_node.chapter_list if len(chapter.chapter_title) > 0])
        real_chapter_rate = 1.0 * real_chapter_number / len(virtual_novel_node.chapter_list)
        if real_chapter_number >= 20 or real_chapter_rate >= 0.6:
            virtual_novel_node.chapter_list = [chapter for chapter in virtual_novel_node.chapter_list if len(chapter.chapter_title) > 0]

        return True


    def debug_novel_node(self, novel_node):
        """
        """
        print(novel_node.rank)
        print(', '.join('%s: %d' % (chapter.chapter_title.encode('GBK', 'ignore'), chapter.rank) for chapter in novel_node.chapter_list))


    def virtual_novel_node_init(self, novel_node):
        """
        """
        novel_node.rank = novel_node.site_status + 1
        for chapter in novel_node.chapter_list:
            chapter.rank = 0


    def virtual_novel_node_generate(self, novel_cluster_node):
        """
            一个簇计算产生一个虚拟节点
        """
        novel_cluster_node.novel_node_list = sorted(
            novel_cluster_node.novel_node_list,
            lambda a, b: cmp(len(b.chapter_list), len(a.chapter_list))
        )
        virtual_novel_node_list = []
        for novel_node in novel_cluster_node.novel_node_list:
            flag = False
            for virtual_novel_node in virtual_novel_node_list:
                flag = self.virtual_novel_node_merge(virtual_novel_node, novel_node)
                if flag is True:
                    break
            if flag is False:
                self.virtual_novel_node_init(novel_node)
                virtual_novel_node_list.append(novel_node)

        max_virtual_novel_node = virtual_novel_node_list[0]
        for virtual_novel_node in virtual_novel_node_list:
            if virtual_novel_node.rank > max_virtual_novel_node.rank:
                max_virtual_novel_node = virtual_novel_node

        real_chapter_number = len([chapter for chapter in max_virtual_novel_node.chapter_list if len(chapter.chapter_title) > 0])
        real_chapter_rate = 1.0 * real_chapter_number / len(max_virtual_novel_node.chapter_list)
        if real_chapter_number >= 20 or real_chapter_rate >= 0.6:
            max_virtual_novel_node.chapter_list = [chapter for chapter in max_virtual_novel_node.chapter_list if len(chapter.chapter_title) > 0]

        return max_virtual_novel_node


    def novel_cluster_similarity_calculation(self, virtual_novel_node_x, virtual_novel_node_y):
        """
            计算两个gid的相似度
        """
        similarity, match_list = self.novel_node_similarity_calculation(virtual_novel_node_x, virtual_novel_node_y)
        return similarity


if __name__ == '__main__':
    here()    







