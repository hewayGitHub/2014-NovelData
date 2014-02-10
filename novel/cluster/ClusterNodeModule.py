#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-02 22:51'

import logging

from basic.NovelStructure import *
from novel.cluster.ClusterDB import *
from public.BasicStringMethod import *

def here():
    print('PrimeMusic')

class ClusterNodeModule(object):
    """
        将各个站点的小说信息整合后更新到点集合中
    """
    def __init__(self):
        """
            初始化操作，读取配置
        """
        self.logger = logging.getLogger('novel.cluster.node')
        self.err = logging.getLogger('err.cluster.node')

    def generate_novel_node_list(self, site_id, update_time):
        """
            更新site_id站点中，更新时间大于update_time的小说信息
        """
        cluster_db = ClusterDBModule()
        novel_id_list = cluster_db.get_dirfmtinfo_id_list(site_id, update_time)
        self.logger.info('get {0} novel info'.format(len(novel_id_list)))

        for novel_id in novel_id_list:
            novel_node = self.generate_novel_node(site_id, novel_id)
            if novel_node is False:
                continue
            self.integrate_novel_node(novel_node)
            self.update_novel_node(novel_node)

    def update_novel_node(self, novel_node):
        """
            单本小说信息更新到点集合当中
        """
        cluster_node = self.generate_cluster_node(novel_node.dir_id)
        if cluster_node and novel_node.equal(cluster_node):
            return False

        cluster_db = ClusterDBModule()
        if cluster_node:
            cluster_db.delete_novelclusterdirinfo(novel_node.dir_id)
            cluster_db.delete_novelclusterchapterinfo_list(novel_node.dir_id)

        self.logger.info('dir_id: {0}, table_id: {1}'.format(novel_node.dir_id, novel_node.dir_id % 256))
        cluster_db.insert_novelclusterdirinfo(novel_node.dir_id, novel_node.generate_insert_tuple())
        cluster_db.insert_novelclusterchapterinfo_list(novel_node.dir_id, [chapter.generate_insert_tuple() for chapter in novel_node.chapter_list])
        return True

    def generate_cluster_node(self, dir_id):
        """
            根据dir_id，获取点集合中已有的点信息
        """
        cluster_db = ClusterDBModule()

        result = cluster_db.get_novelclusterdirinfo_info(dir_id)
        if not result:
            return False

        (site_id, site, site_status, dir_id, dir_url, gid, book_name, pen_name) = result
        book_name = book_name.decode('GBK', 'ignore')
        pen_name = pen_name.decode('GBK', 'ignore')
        cluster_node = NovelNodeInfo(site_id, site, site_status, dir_id, dir_url, gid, book_name, pen_name)

        result = cluster_db.get_novelclusterchapterinfo_list(dir_id)
        for (dir_id, chapter_id, chapter_sort, chapter_url, chapter_title, chapter_status) in result:
            chapter_title = chapter_title.decode('GBK', 'ignore')
            chapter = NovelChapterInfo(dir_id, chapter_id, chapter_sort, chapter_url, chapter_title, chapter_status)
            cluster_node.chapter_list.append(chapter)
        return cluster_node

    def integrate_novel_node(self, novel_node):
        """
            单本小说信息的整合处理
        """
        for chapter in novel_node.chapter_list:
            chapter.chapter_title = string_filter(chapter.chapter_title)

    def generate_novel_node(self, site_id, novel_id):
        """
            收集一本小说的基本信息
        """
        cluster_db = ClusterDBModule()

        result = cluster_db.get_dirfmtinfo_info(site_id, novel_id)
        if result is False:
            return False

        (site_id, site, site_status, dir_id, dir_url, gid, book_name, pen_name) = result
        book_name = book_name.decode('GBK', 'ignore')
        pen_name = pen_name.decode('GBK', 'ignore')
        novel_node = NovelNodeInfo(site_id, site, site_status, dir_id, dir_url, gid, book_name, pen_name)

        result = cluster_db.get_chapteroriinfo_list(site_id, dir_id)
        for (dir_id, chapter_id, chapter_sort, chapter_url, chapter_title, chapter_status) in result:
            chapter_title = chapter_title.decode('GBK', 'ignore')
            chapter = NovelChapterInfo(dir_id, chapter_id, chapter_sort, chapter_url, chapter_title, chapter_status)
            novel_node.chapter_list.append(chapter)
        return novel_node




if __name__ == '__main__':
    here()







