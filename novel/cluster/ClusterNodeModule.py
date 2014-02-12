#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-02 22:51'

import logging
from ConfigParser import SafeConfigParser
from collections import defaultdict

from basic.NovelStructure import *
from novel.cluster.ClusterDB import *
from public.BasicStringMethod import *


def here():
    print('PrimeMusic')


class ClusterNodeModule(object):
    """
        将各个站点的小说信息整合后更新到点集合中
    """
    def init_time_info(self):
        """
        """
        self.proc_time_dict = {}
        for line in open('./data/NovelClusterModule.time', 'r').readlines():
            (table, update_time) = line.strip().split(':')
            self.proc_time_dict[table] = int(update_time)


    def init_log_info(self):
        """
        """
        self.logger = logging.getLogger('novel.cluster.node')
        self.err = logging.getLogger('err.cluster.node')


    def init_conf_info(self):
        """
        """
        parser = SafeConfigParser()
        parser.read('./conf/NovelClusterModule.conf')
        self.start_site_id = parser.getint('cluster_node_module', 'proc_start_site_id')
        self.end_site_id = parser.getint('cluster_node_module', 'proc_end_site_id')


    def init(self):
        """
            初始化基础信息，加载配置
        """
        self.init_log_info()
        self.init_conf_info()
        self.init_time_info()
        self.logger.info('novel cluster node module init successful')


    def novel_node_collection(self, site_id, novel_id):
        """
            收集一本小说的基本信息
        """
        cluster_db = ClusterDBModule()

        result = cluster_db.get_dirfmtinfo_info(site_id, novel_id)
        if not result:
            return False
        (site_id, site, site_status, dir_id, dir_url, gid, book_name, pen_name) = result
        book_name = book_name.decode('GBK', 'ignore')
        pen_name = pen_name.decode('GBK', 'ignore')
        novel_node = NovelNodeInfo(site_id, site, site_status, dir_id, dir_url, gid, book_name, pen_name)

        result = cluster_db.get_chapteroriinfo_list(site_id, dir_id)
        if len(result) == 0:
            return False
        for (dir_id, chapter_id, chapter_sort, chapter_url, chapter_title, chapter_status) in result:
            chapter_title = chapter_title.decode('GBK', 'ignore')
            chapter = NovelChapterInfo(dir_id, chapter_id, chapter_sort, chapter_url, chapter_title, chapter_status)
            novel_node.chapter_list.append(chapter)
        return novel_node


    def novel_node_integrate(self, novel_node):
        """
            单本小说信息的整合处理
        """
        for chapter in novel_node.chapter_list:
            chapter.chapter_title = string_filter(chapter.chapter_title)
        return True


    def novel_node_update(self, table_id):
        """
        """
        cluster_db = ClusterDBModule()

        dir_id_list = []
        for novel_node in self.current_novel_node_dict[table_id]:
            dir_id_list.append(novel_node.dir_id)
        cluster_db.delete_novelclusterdirinfo(table_id, dir_id_list)
        cluster_db.delete_novelclusterchapterinfo_list(table_id, dir_id_list)

        dir_insert_tuple_list = []
        chapter_insert_tuple_list = []
        for novel_node in self.current_novel_node_dict[table_id]:
            dir_insert_tuple_list.append(novel_node.generate_insert_tuple())
            for chapter in novel_node.chapter_list:
                chapter_insert_tuple_list.append(chapter.generate_insert_tuple())
        cluster_db.insert_novelclusterdirinfo(table_id, dir_insert_tuple_list)
        cluster_db.insert_novelclusterchapterinfo_list(table_id, chapter_insert_tuple_list)

        self.current_novel_node_dict[table_id] = []
        return True


    def novel_node_generate(self, site_id, update_time):
        """
            更新site_id站点中，更新时间大于update_time的小说信息
        """
        cluster_db = ClusterDBModule()
        novel_id_list = cluster_db.get_dirfmtinfo_id_list(site_id, update_time)

        self.current_novel_node_dict = defaultdict(list)
        for index, novel_id in enumerate(novel_id_list):
            novel_node = self.novel_node_collection(site_id, novel_id)
            if not novel_node:
                continue

            self.novel_node_integrate(novel_node)
            table_id = novel_node.dir_id % 256
            self.current_novel_node_dict[table_id].append(novel_node)

            if len(self.current_novel_node_dict[table_id]) == 100:
                self.novel_node_update(table_id)

            if index % 100 == 0:
                self.logger.info('[site_id: {0}, current_count: {1}, total_count: {2}]'.format(site_id, index, len(novel_id_list)))

        for (table_id, novel_node_list) in self.current_novel_node_dict.items():
            self.novel_node_update(table_id)
        return True


    def run(self):
        """
        """
        self.logger.info('novel cluster node module start')

        for site_id in xrange(self.start_site_id, self.end_site_id + 1):
            update_time = self.proc_time_dict['dir_fmt_info{0}'.format(site_id)]
            self.novel_node_generate(site_id, update_time)
        return True


if __name__ == '__main__':
    here()







