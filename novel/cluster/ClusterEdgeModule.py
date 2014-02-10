#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-02 22:51'

import logging
from collections import defaultdict

from basic.NovelStructure import *
from novel.cluster.ClusterDB import *
from public.BasicStringMethod import *

def here():
    print('PrimeMusic')

class ClusterEdgeModule(object):
    """
        更新小说边集合信息
    """
    def __init__(self):
        """
            初始化操作，读取配置
        """
        self.logger = logging.getLogger('novel.cluster.edge')
        self.err = logging.getLogger('err.cluster.edge')

        self.novel_node_dict = None

        self.current_novel_node_info_list = None
        self.current_novel_edge_info_list = None

    def novel_edge_generate(self, novel_node_list):
        """
            计算单个特征下点集合的边信息
        """
        self.current_novel_node_info_list = []
        for dir_id in novel_node_list:
            novel_node = self.novel_node_generate(dir_id)
            if not novel_node:
                continue
            self.current_novel_node_info_list.append(novel_node)

        self.current_novel_edge_info_list = []
        for index_x, novel_node_x in enumerate(self.current_novel_node_info_list):
            for index_y, novel_node_y in enumerate(self.current_novel_node_info_list):
                if index_x == index_y:
                    continue
                similarity = self.novel_node_similarity_calculation(novel_node_x, novel_node_y)

    def novel_node_similarity_calculation(self, novel_node_x, novel_node_y):
        """
            计算两个点的相似度
        """
        novel_similarity = self.chapter_list_similarity_calculation(novel_node_x.chapter_list, novel_node_y.chapter_list)
        if novel_node_x.book_name == novel_node_y.book_name:
            novel_similarity += 10
        if novel_node_x.pen_name == novel_node_y.pen_name:
            novel_similarity += 10
        return novel_similarity

    def chapter_list_similarity_calculation(self, chapter_list_x, chapter_list_y):
        """
        """
        chapter_count = min(len(chapter_list_x), len(chapter_list_y))
        if chapter_count == 0:
            return 0
        match_count = 0
        for chapter_x in chapter_list_x:
            for chapter_y in chapter_list_y:
                if string_similarity(chapter_x.chapter_title, chapter_y.chapter_title) > 0.7:
                    match_count += 1
                    break
        similarity = match_count * 1.0 / chapter_count
        similarity = int(similarity * 10)
        return similarity

    def novel_node_generate(self, dir_id):
        """
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

    def novel_node_collection(self):
        """
            读取所有小说的点集合，按特征划分
        """
        cluster_db = ClusterDBModule()

        self.novel_node_dict = defaultdict(list)
        for table_id in xrange(0, 256):
            novel_node_list = cluster_db.get_novelclusterdirinfo_list(table_id, 'book_name')
            if not novel_node_list:
                continue
            for (dir_id, field) in novel_node_list:
                self.novel_node_dict[field].append(dir_id)


if __name__ == '__main__':
    here()    







