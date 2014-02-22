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
    def init_conf_info(self):
        """
        """
        parser = SafeConfigParser()
        parser.read('./conf/NovelClusterModule.conf')
        self.start_gid_id = parser.getint('cluster_edge_module', 'proc_start_gid_id')
        self.end_gid_id = parser.getint('cluster_edge_module', 'proc_end_gid_id')


    def init_log_info(self):
        """
        """
        self.logger = logging.getLogger('novel.cluster.edge')
        self.err = logging.getLogger('err.cluster.edge')


    def init(self):
        """
            初始化操作
        """
        self.init_log_info()
        self.init_conf_info()
        self.logger.info('novel cluster edge module init successful')


    def cluster_node_collection(self, gid):
        """
        """
        cluster_node = NovelClusterInfo(gid)

        cluster_db = ClusterDBModule()
        dir_info_list = cluster_db.get_novelclusterdirinfo_gid(gid)
        chapter_info_list = cluster_db.get_novelclusterchapterinfo_gid(gid)

        chapter_dict = defaultdict(list)
        for (dir_id, chapter_id, chapter_title) in chapter_info_list:
            chapter = NovelChapterInfo(chapter_id = chapter_id, chapter_title = chapter_title)
            chapter_dict[dir_id].append(chapter)

        cluster_node.novel_node_list = []
        for (site_id, dir_id, dir_url, gid, book_name, pen_name) in dir_info_list:
            novel_node = NovelNodeInfo(site_id = site_id, dir_id = dir_id, dir_url = dir_url, gid = gid)
            novel_node.book_name = book_name.decode('GBK', 'ignore')
            novel_node.pen_name = pen_name.decode('GBK', 'ignore')
            if not chapter_dict.has_key(novel_node.dir_id):
                continue
            if len(chapter_dict[novel_node.dir_id]) <= 1:
                continue
            novel_node.chapter_list = chapter_dict[novel_node.dir_id]
            cluster_node.novel_node_list.append(novel_node)

        if len(cluster_node.novel_node_list) == 0:
            return False
        cluster_node.book_name = cluster_node.novel_node_list[0].book_name
        cluster_node.pen_name = cluster_node.novel_node_list[0].pen_name
        return cluster_node


    def process_gid_collection(self):
        """
        """
        cluster_db = ClusterDBModule()
        result = cluster_db.get_novelclusterdirinfo_all(['gid'])

        g = lambda gid: gid % 256 <= self.end_gid_id and gid % 256 >= self.start_gid_id
        return {}.fromkeys(filter(g, [row[0] for row in result])).keys()


    def related_gid_collection(self, cluster_node):
        """
        """
        cluster_db = ClusterDBModule()

        related_list = []
        if cluster_node.book_name:
            related_list.extend(cluster_db.get_novelclusterdirinfo_name('book_name', cluster_node.book_name.encode('GBK', 'ignore')))
        if cluster_node.pen_name:
            related_list.extend(cluster_db.get_novelclusterdirinfo_name('pen_name', cluster_node.pen_name.encode('GBK', 'ignore')))

        g = lambda gid: gid > cluster_node.gid
        return {}.fromkeys(filter(g, [row[0] for row in related_list])).keys()


    def cluster_edge_update(self, gid, cluster_edge_list):
        """
        """
        cluster_db = ClusterDBModule()

        cluster_db.delete_novelclusteredgeinfo(gid)
        cluster_db.insert_novelclusteredgeinfo([edge.generate_insert_tuple() for edge in cluster_edge_list])


    def run(self):
        """
        """
        similarity = NovelSimilarityModule()

        process_gid_list = self.process_gid_collection()
        self.logger.info('process gid list length: {0}'.format(len(process_gid_list)))

        for gid in process_gid_list:
            cluster_node = self.cluster_node_collection(gid)
            if not cluster_node:
                continue

            related_gid_list = self.related_gid_collection(cluster_node)
            self.logger.info('-------------------------')
            self.logger.info('[{0}, {1}, {2}, {3}]'.format(cluster_node.gid, cluster_node.book_name.encode('GBK'), cluster_node.pen_name.encode('GBK'), len(related_gid_list)))

            related_edge_list = []
            for related_gid in related_gid_list:
                related_cluster_node = self.cluster_node_collection(related_gid)
                if not related_cluster_node:
                    continue
                cluster_similarity = similarity.novel_cluster_similarity_calculation(cluster_node, related_cluster_node)
                if cluster_similarity >= 0.6:
                    cluster_edge = ClusterEdgeInfo(cluster_node.gid, related_cluster_node.gid, cluster_similarity)
                    related_edge_list.append(cluster_edge)
                    self.logger.info('[{0}, {1}, {2}, {3}]'.format(related_cluster_node.gid, related_cluster_node.book_name.encode('GBK'), related_cluster_node.pen_name.encode('GBK'), cluster_edge.similarity))

        return True



if __name__ == '__main__':
    here()






