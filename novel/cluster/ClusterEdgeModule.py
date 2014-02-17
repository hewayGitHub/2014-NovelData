#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-02 22:51'

import logging
import time
from collections import defaultdict

from basic.NovelStructure import *
from novel.cluster.ClusterDB import *
from novel.cluster.NovelSimilarityModule import *
from public.BasicStringMethod import *
from tools.debug import *

def here():
    print('PrimeMusic')

class ClusterEdgeModule(object):
    """
        更新小说边集合信息
    """
    def __init__(self):
        """
            初始化操作
        """
        self.logger = logging.getLogger('novel.cluster.edge')
        self.err = logging.getLogger('err.cluster.edge')

        self.novel_node_dict = None

        self.current_novel_node_info_list = None
        self.current_novel_edge_info_dict = None


    def novel_node_generate(self, dir_id):
        """
            根据dir_id从点集合中读取一本小说的信息
        """
        cluster_db = ClusterDBModule()

        result = cluster_db.get_novelclusterdirinfo_info(dir_id)
        if not result:
            return False

        (site_id, site, site_status, dir_id, dir_url, gid, book_name, pen_name) = result
        book_name = book_name.decode('GBK', 'ignore')
        pen_name = pen_name.decode('GBK', 'ignore')
        novel_node = NovelNodeInfo(site_id, site, site_status, dir_id, dir_url, gid, book_name, pen_name)

        result = cluster_db.get_novelclusterchapterinfo_list(dir_id)
        for (dir_id, chapter_id, chapter_sort, chapter_url, chapter_title, chapter_status) in result:
            chapter_title = chapter_title.decode('GBK', 'ignore')
            chapter = NovelChapterInfo(dir_id, chapter_id, chapter_sort, chapter_url, chapter_title, chapter_status)
            novel_node.chapter_list.append(chapter)
        return novel_node


    def novel_edge_generate(self, key, value, novel_node_list, similarity_threshold):
        """
            计算单个特征下点集合的边信息
        """
        self.logger.info('[{0}: {1}, novel_node_number: {2}]'.format(key, value, len(novel_node_list)))

        novel_similarity = NovelSimilarityModule()
        novel_node_list = sorted(novel_node_list)

        self.current_novel_node_info_list = []
        for dir_id in novel_node_list:
            novel_node = self.novel_node_generate(dir_id)
            if not novel_node:
                continue
            self.current_novel_node_info_list.append(novel_node)

        self.current_novel_edge_info_dict = defaultdict(list)
        for index_i in xrange(0, len(self.current_novel_node_info_list)):
            for index_j in xrange(index_i + 1, len(self.current_novel_node_info_list)):
                novel_node_i = self.current_novel_node_info_list[index_i]
                novel_node_j = self.current_novel_node_info_list[index_j]
                if key == 'pen_name' and novel_node_i.book_name == novel_node_j.book_name:
                    continue
                similarity = novel_similarity.novel_node_similarity_calculation(novel_node_i, novel_node_j)
                if similarity > similarity_threshold:
                    edge = NovelEdgeInfo(novel_node_i.dir_id, novel_node_j.dir_id, similarity)
                    self.current_novel_edge_info_dict[novel_node_i.dir_id].append(edge)


    def novel_edge_update(self):
        """
            单个特征下边集合的更新
        """
        cluster_db = ClusterDBModule()

        for (dir_id, novel_edge_info_list) in self.current_novel_edge_info_dict.items():
            cluster_db.insert_novelclusteredgeinfo_list(dir_id, [edge.generate_insert_tuple() for edge in novel_edge_info_list])


    def novel_node_collection(self, field = 'book_name'):
        """
            收集所有小说点，按特征分组
        """
        cluster_db = ClusterDBModule()

        self.novel_node_dict = defaultdict(list)
        for table_id in xrange(0, 256):
            novel_node_list = cluster_db.get_novelclusterdirinfo_list(table_id, field)
            if not novel_node_list:
                continue

            self.logger.info('[table_id: {0}, novel_node_number: {1}]'.format(table_id, len(novel_node_list)))
            for (dir_id, name) in novel_node_list:
                self.novel_node_dict[name].append(dir_id)


    def run(self):
        """
            1.  读取所有小说点，按特征分组
            2.  每组内小说点计算相似度，更新边信息
        """
        cluster_db = ClusterDBModule()
        cluster_db.delete_novelclusteredgeinfo()

        self.novel_node_collection('book_name')
        for (name, novel_node_list) in self.novel_node_dict.items():
            if len(novel_node_list) == 1 or name == '':
                continue
            self.novel_edge_generate('book_name', name, novel_node_list, 16)
            self.novel_edge_update()

        self.novel_node_collection('pen_name')
        for (name, novel_node_list) in self.novel_node_dict.items():
            if len(novel_node_list) == 1 or name == '':
                continue
            self.novel_edge_generate('pen_name', name, novel_node_list, 16)
            self.novel_edge_update()


    def exit(self):
        """
        """
        self.novel_node_dict = None
        self.current_novel_node_info_list = None
        self.current_novel_edge_info_dict = None


if __name__ == '__main__':
    here()






