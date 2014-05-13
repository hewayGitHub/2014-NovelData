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
        С˵���ƶȼ���ģ��
    """
    __metaclass__ = Singleton

    def novel_chapter_similarity_calculation(self, chapter_x, chapter_y):
        """
            ���������½ڵ�������
        """
        return string_similarity(chapter_x.chapter_title, chapter_y.chapter_title)


    def novel_node_similarity_calculation(self, novel_node_x, novel_node_y):
        """
            ��������С˵��������
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
            һ����ͨ�ڵ��һ������ڵ�ϲ������ܺϲ�����false
            Ĭ�ϣ�virtual_novel_node���½ڳ��ȴ���novel_node���½ڳ���
        """
        similarity, match_list = self.novel_node_similarity_calculation(virtual_novel_node, novel_node)
        if similarity < 0.7:
            return False


        return True


    def virtual_novel_node_generate(self, novel_cluster_node):
        """
            һ���ؼ������һ������ڵ�
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
            ��������gid�����ƶ�
        """


if __name__ == '__main__':
    here()    







