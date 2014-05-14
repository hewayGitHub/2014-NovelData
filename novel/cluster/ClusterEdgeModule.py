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


    def related_gid_collection(self, cluster_node):
        """
        """
        cluster_db = ClusterDBModule()

        related_list = []
        if cluster_node.book_name not in [u'', u'未知']:
            related_list.extend(cluster_db.get_novelclusterdirinfo_name('book_name', cluster_node.book_name.encode('GBK', 'ignore')))
        if cluster_node.pen_name not in [u'', u'未知', u'匿名', u'作者', u'feiku', u'发表评论']:
            related_list.extend(cluster_db.get_novelclusterdirinfo_name('pen_name', cluster_node.pen_name.encode('GBK', 'ignore')))

        g = lambda gid: gid != cluster_node.gid
        return {}.fromkeys(filter(g, [row[0] for row in related_list])).keys()


    def cluster_edge_update(self, gid, cluster_edge_list):
        """
        """
        if len(cluster_edge_list) == 0:
            return (0, 0)

        cluster_db = ClusterDBModule()
        result = cluster_db.get_novelclusteredgeinfo_gid(gid)
        related_gid_set = set()
        for (gid_x, gid_y, similarity) in result:
            related_gid_set.add(gid_y)
            related_gid_set.add(gid_x)
        current_gid_set = set()
        for cluster_edge in cluster_edge_list:
            current_gid_set.add(cluster_edge.gid_y)

        insert_edge_list = []
        for cluster_edge in cluster_edge_list:
            if cluster_edge.gid_y in related_gid_set:
                continue
            insert_edge_list.append(cluster_edge.generate_insert_tuple())
        if len(insert_edge_list) > 0:
            cluster_db.insert_novelclusteredgeinfo(insert_edge_list)

        delete_edge_list_x = []
        delete_edge_list_y = []
        for (gid_x, gid_y, similarity) in result:
            if gid_y in current_gid_set or gid_x in current_gid_set:
                continue
            if gid_x == gid:
                delete_edge_list_y.append(gid_y)
            if gid_y == gid:
                delete_edge_list_x.append(gid_x)
        if len(delete_edge_list_x) > 0:
            cluster_db.delete_novelclusteredgeinfo(('gid_y', 'gid_x'), gid, delete_edge_list_x)
        if len(delete_edge_list_y) > 0:
            cluster_db.delete_novelclusteredgeinfo(('gid_x', 'gid_y'), gid, delete_edge_list_y)

        for gid_x in delete_edge_list_x:
            self.err.warning('gid_x: {0}, gid_y: {1}'.format(gid_x, gid))
        for gid_y in delete_edge_list_y:
            self.err.warning('gid_x: {0}, gid_y: {1}'.format(gid, gid_y))

        return (len(insert_edge_list), len(delete_edge_list_x) + len(delete_edge_list_y))


    def process_gid_collection(self):
        """
        """
        cluster_db = ClusterDBModule()
        result = cluster_db.get_noveldata_all('novel_cluster_dir_info', ['gid'])

        g = lambda gid: gid % 256 <= self.end_gid_id and gid % 256 >= self.start_gid_id
        return {}.fromkeys(filter(g, [row[0] for row in result])).keys()


    def run(self, process_gid_list = []):
        """
        """
        similarity = NovelSimilarityModule()

        if len(process_gid_list) == 0:
            process_gid_list = self.process_gid_collection()

        for index, gid in enumerate(process_gid_list):
            cluster_node = self.cluster_node_collection(gid)
            if not cluster_node:
                continue

            related_gid_list = self.related_gid_collection(cluster_node)
            related_edge_list = []
            for related_gid in related_gid_list:
                related_cluster_node = self.cluster_node_collection(related_gid)
                if not related_cluster_node:
                    continue
                cluster_similarity = similarity.novel_cluster_similarity_calculation(cluster_node, related_cluster_node)
                if cluster_similarity >= 0.7:
                    cluster_edge = ClusterEdgeInfo(cluster_node.gid, related_cluster_node.gid, cluster_similarity)
                    related_edge_list.append(cluster_edge)
                    book_name = related_cluster_node.book_name.encode('GBK')
                    pen_name = related_cluster_node.pen_name.encode('GBK')
                    self.logger.info('book_name: {0}, pen_name: {1}'.format(book_name, pen_name))
            (insert_num, delete_num) = self.cluster_edge_update(gid, related_edge_list)

            book_name = cluster_node.book_name.encode('GBK')
            pen_name = cluster_node.pen_name.encode('GBK')
            self.logger.info('gid: {0}, '
                             'index: {1}/{2}, book_info: {3}/{4}, '
                             'related_num: {5}/{6}, update_edge_num: {7}/{8}'.format(
                gid,
                index, len(process_gid_list), book_name, pen_name,
                len(related_gid_list), len(related_edge_list), insert_num, delete_num
            ))

        return True


    def run_test(self):
        """
            跑评估数据
        """
        gid_list = [int(line.strip()) for line in open('./data/rid.txt', 'r').readlines()]
        similarity = NovelSimilarityModule()

        for index, gid in enumerate(gid_list):
            cluster_node = self.cluster_node_collection(gid)
            if not cluster_node:
                continue
            novel_node = similarity.virtual_novel_node_generate(cluster_node)
            print('gid: {0}, book_name: {1}, pen_name: {2}'.format(
                gid,
                novel_node.book_name.encode('GBK', 'ignore'),
                novel_node.pen_name.encode('GBK', 'ignore')
            ))
            print(', '.join('%s' % chapter.chapter_title.encode('GBK', 'ignore') for chapter in novel_node.chapter_list))
            print()




if __name__ == '__main__':
    here()






