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


    def __init__(self):
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
            chapter = NovelChapterInfo(chapter_id = chapter_id, chapter_title = chapter_title.decode('GBK', 'ignore'))
            chapter_dict[dir_id].append(chapter)

        cluster_node.novel_node_list = []
        for (site_id, site_status, dir_id, dir_url, gid, book_name, pen_name) in dir_info_list:
            novel_node = NovelNodeInfo(site_id = site_id, site_status = site_status, dir_id = dir_id, dir_url = dir_url, gid = gid)
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


    def related_gid_collection(self, cluster_node):
        """
        """
        cluster_db = ClusterDBModule()

        related_list = []
        if cluster_node.book_name not in [u'', u'未知']:
            related_list.extend(cluster_db.get_novelclusterdirinfo_name('book_name', cluster_node.book_name.encode('GBK', 'ignore')))
        if cluster_node.pen_name not in [
            u'', u'未知', u'暂缺', u'匿名',
            u'1', u'作者', u'feiku', u'发表评论', u'征文作者',
            u'金庸', u'古龙'
        ]:
            related_list.extend(cluster_db.get_novelclusterdirinfo_name('pen_name', cluster_node.pen_name.encode('GBK', 'ignore')))

        g = lambda gid: gid != cluster_node.gid
        return {}.fromkeys(filter(g, [row[0] for row in related_list])).keys()


    def cluster_edge_update(self, gid, cluster_edge_list):
        """
        """
        if len(cluster_edge_list) == 0:
            return True

        cluster_db = ClusterDBModule()
        cluster_db.delete_novelclusteredgeinfo(gid)

        insert_edge_list = []
        for cluster_edge in cluster_edge_list:
            insert_edge_list.append(cluster_edge.generate_insert_tuple())
        if len(insert_edge_list) > 0:
            cluster_db.insert_novelclusteredgeinfo(insert_edge_list)

        return True


    def process_gid_collection(self):
        """
        """
        cluster_db = ClusterDBModule()
        result = cluster_db.get_noveldata_all('novel_cluster_dir_info_offline', ['gid'])

        g = lambda gid: gid % 256 <= self.end_gid_id and gid % 256 >= self.start_gid_id
        return {}.fromkeys(filter(g, [row[0] for row in result])).keys()


    def run(self):
        """
        """
        self.logger.info('novel cluster edge module start')

        similarity = NovelSimilarityModule()

        process_gid_list = self.process_gid_collection()
        for index, gid in enumerate(process_gid_list):

            cluster_db = ClusterDBModule()
            cluster_db.delete_novelclusteredgeinfo(gid)

            cluster_node = self.cluster_node_collection(gid)
            if not cluster_node:
                continue
            virtual_node = similarity.virtual_novel_node_generate(cluster_node)
            related_gid_list = self.related_gid_collection(cluster_node)
            if len(related_gid_list) == 0:
                continue

            book_name = cluster_node.book_name.encode('GBK')
            pen_name = cluster_node.pen_name.encode('GBK')
            self.logger.info('index: {0}/{1}'.format(index, len(process_gid_list)))
            self.logger.info('novel_info: {0}@{1}@{2}, '
                             'chater_number: {3}, related_gid_number: {4}'.format(
                gid, book_name, pen_name,
                len(virtual_node.chapter_list), len(related_gid_list)
            ))

            related_edge_list = []
            for related_gid in related_gid_list:
                related_cluster_node = self.cluster_node_collection(related_gid)
                if not related_cluster_node:
                    continue
                related_virtual_node = similarity.virtual_novel_node_generate(related_cluster_node)
                cluster_similarity = similarity.novel_cluster_similarity_calculation(virtual_node, related_virtual_node)
                if cluster_similarity >= 0.7:
                    cluster_edge = ClusterEdgeInfo(cluster_node.gid, related_cluster_node.gid, cluster_similarity)
                    related_edge_list.append(cluster_edge)

                    book_name = related_cluster_node.book_name.encode('GBK')
                    pen_name = related_cluster_node.pen_name.encode('GBK')
                    self.logger.info('novel_info: {0}@{1}@{2}, '
                                     'chapter_number: {3}, similarity: {4}'.format(
                        related_gid, book_name, pen_name,
                        len(related_virtual_node.chapter_list), cluster_similarity
                    ))
            self.cluster_edge_update(gid, related_edge_list)

        self.logger.info('novel cluster edge module end')
        return True


if __name__ == '__main__':
    here()






