#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-02 22:51'

import logging
import time
from ConfigParser import SafeConfigParser
from collections import defaultdict

from basic.NovelStructure import *
from novel.cluster.ClusterDB import *
from novel.cluster.NovelCleanModule import *
from novel.cluster.ClusterEdgeModule import *
from public.BasicStringMethod import *


def here():
    print('PrimeMusic')


class ClusterNodeModule(object):
    """
        将各个站点的小说信息整合后更新到点集合中
    """
    def init_data_info(self):
        """
        """
        self.proc_time_dict = {}
        for line in open('./data/NovelClusterModule.time', 'r').readlines():
            (table, update_time) = line.strip().split(':')
            self.proc_time_dict[table] = int(update_time)

        self.site_dict = {}
        for line in open('./data/site', 'r').readlines():
            (site_id, site) = line.strip().split(':')
            if site == 'null':
                continue
            site_id = int(site_id)
            self.site_dict[site_id] = site


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


    def __init__(self):
        """
            初始化基础信息，加载配置
        """
        self.init_log_info()
        self.init_conf_info()
        self.init_data_info()
        self.logger.info('novel cluster node module init successful')

        self.update_node_number = 0
        self.insert_node_number = 0

        self.delete_chapter_number = 0
        self.update_chapter_number = 0
        self.insert_chapter_number = 0


    def __del__(self):
        """
        """
        with open('./data/NovelClusterModule.time', "w") as f:
            for (table, update_time) in self.proc_time_dict.iteritems():
                f.write("{0}:{1}\n".format(table, update_time))


    def novel_node_collection(self, site_id, novel_id_list):
        """
            收集一本小说的基本信息
        """
        cluster_db = ClusterDBModule()

        dir_id_list = []
        current_novel_node_dict = {}
        current_novel_node_list = []

        result = cluster_db.get_dirfmtinfo_info(site_id, novel_id_list)
        for (site_id, site, site_status, dir_id, dir_url, gid, book_name, pen_name, chapter_count, last_chapter_title, update_time) in result:
            book_name = book_name.decode('GBK', 'ignore')
            book_name = string_Q2B(book_name)
            book_name = string_filter(book_name)
            pen_name = pen_name.decode('GBK', 'ignore')
            pen_name = string_Q2B(pen_name)
            pen_name = string_filter(pen_name)
            last_chapter_title = last_chapter_title.decode('GBK', 'ignore')
            last_chapter_title = string_Q2B(last_chapter_title)
            last_chapter_title = string_filter(last_chapter_title)
            chapter_word_sum = 0

            novel_node = NovelNodeInfo(
                site_id, site, site_status,
                dir_id, dir_url, gid, book_name, pen_name,
                chapter_count, chapter_word_sum, last_chapter_title
            )

            dir_id_list.append(dir_id)
            current_novel_node_dict[dir_id] = novel_node

            table_name = 'dir_fmt_info{0}'.format(site_id)
            self.proc_time_dict[table_name] = max(self.proc_time_dict[table_name], update_time)

        result = cluster_db.get_chapteroriinfo_list(site_id, dir_id_list)
        for (dir_id, chapter_id, chapter_sort, chapter_url, chapter_title) in result:
            chapter_title = chapter_title.decode('GBK', 'ignore')
            novel_node = current_novel_node_dict[dir_id]
            chapter = NovelChapterInfo(novel_node.gid, site_id, dir_id, chapter_sort, chapter_id, chapter_url, chapter_title)
            novel_node.chapter_list.append(chapter)

        for (dir_id, novel_node) in current_novel_node_dict.items():
            if len(novel_node.chapter_list) <= 1:
                continue
            current_novel_node_list.append(novel_node)
        return current_novel_node_list


    def novel_node_integrate(self, novel_node):
        """
            单本小说信息的整合处理
        """
        clean = NovelCleanModule()
        clean.novel_chapter_clean(novel_node)

        if novel_node.site_status == 0:
            novel_node.site_status = 1
        if novel_node.site_status == 2:
            novel_node.site_status = 0
        return True


    def check_novel_dir_update(self, origin_novel_node, novel_node):
        """
        """
        if origin_novel_node.gid != novel_node.gid:
            return False
        if origin_novel_node.chapter_count != novel_node.chapter_count:
            return False
        if origin_novel_node.last_chapter_title != novel_node.last_chapter_title:
            return False
        return True


    def novel_node_dir_update(self, gid_rid_dict, dir_node_dict, current_novel_node_list):
        """
        """
        cluster_db = ClusterDBModule()

        insert_tuple_list = []
        update_tuple_list = []
        for novel_node in current_novel_node_list:
            if gid_rid_dict.has_key(novel_node.gid):
                novel_node.rid = gid_rid_dict[novel_node.gid]

            if not dir_node_dict.has_key(novel_node.dir_id):
                insert_tuple_list.append(novel_node.generate_insert_tuple())
                continue
            if not self.check_novel_dir_update(dir_node_dict[novel_node.dir_id], novel_node):
                update_tuple_list.append(novel_node.generate_update_tuple())
                continue

        self.update_node_number += len(update_tuple_list)
        self.insert_node_number += len(insert_tuple_list)
        self.logger.info('dir update number: {0}, dir insert number: {1}'.format(
            len(update_tuple_list),
            len(insert_tuple_list)
        ))
        if len(update_tuple_list):
            cluster_db.update_novelclusterdirinfo(update_tuple_list)
        if len(insert_tuple_list):
            cluster_db.insert_novelclusterdirinfo(insert_tuple_list)


    def check_novel_chapter_update(self, origin_chapter, chapter):
        """
        """
        if origin_chapter.gid != chapter.gid:
            return False
        if origin_chapter.chapter_title != chapter.chapter_title:
            return False
        return True


    def novel_node_chapter_update(self, table_id, dir_chapter_dict, current_novel_node_list):
        """
        """
        cluster_db = ClusterDBModule()

        delete_tuple_list = []
        update_tuple_list = []
        insert_tuple_list = []

        for novel_node in current_novel_node_list:
            dir_id = novel_node.dir_id
            if not dir_chapter_dict.has_key(dir_id):
                insert_tuple_list.extend([chapter.generate_insert_tuple() for chapter in novel_node.chapter_list])
                continue

            chapter_list = novel_node.chapter_list
            chapter_list = sorted(chapter_list, lambda a, b: cmp(a.chapter_sort, b.chapter_sort))
            origin_chapter_list = dir_chapter_dict[dir_id]
            origin_chapter_list = sorted(origin_chapter_list, lambda a, b: cmp(a.chapter_sort, b.chapter_sort))

            if len(origin_chapter_list) > len(chapter_list):
                delete_tuple_list.extend([chapter.generate_delete_tuple() for chapter in origin_chapter_list[len(chapter_list) : ]])
            for index, chapter in enumerate(chapter_list):
                if index >= len(origin_chapter_list):
                    insert_tuple_list.append(chapter.generate_insert_tuple())
                    continue
                if not self.check_novel_chapter_update(origin_chapter_list[index], chapter):
                    update_tuple_list.append(chapter.generate_update_tuple())
                    continue

        self.delete_chapter_number += len(delete_tuple_list)
        self.update_chapter_number += len(update_tuple_list)
        self.insert_chapter_number += len(insert_tuple_list)
        self.logger.info('chapter delete number: {0}, chapter update number: {1}, chapter insert number: {2}'.format(
            len(delete_tuple_list),
            len(update_tuple_list),
            len(insert_tuple_list)
        ))
        if len(delete_tuple_list) > 0:
            cluster_db.delete_novelclusterchapterinfo(table_id, delete_tuple_list)
        if len(update_tuple_list) > 0:
            cluster_db.update_novelclusterchapterinfo(table_id, update_tuple_list)
        if len(insert_tuple_list) > 0:
            cluster_db.insert_novelclusterchapterinfo(table_id, insert_tuple_list)


    def novel_node_update(self, table_id, current_novel_node_list):
        """
        """
        if len(current_novel_node_list) == 0:
            return True

        cluster_db = ClusterDBModule()
        dir_id_list = [novel_node.dir_id for novel_node in current_novel_node_list]
        gid_list = {}.fromkeys([novel_node.gid for novel_node in current_novel_node_list]).keys()

        result = cluster_db.get_novelclusterdirinfo_gidlist(gid_list)
        gid_rid_dict = {}
        for (gid, rid) in result:
            gid_rid_dict[gid] = rid

        result = cluster_db.get_novelclusterdirinfo_diridlist(dir_id_list)
        dir_node_dict = {}
        for (dir_id, gid, chapter_count, last_chapter_title) in result:
            last_chapter_title = last_chapter_title.decode('GBK', 'ignore')
            node = NovelNodeInfo(dir_id = dir_id, gid = gid, chapter_count = chapter_count, last_chapter_title = last_chapter_title)
            dir_node_dict[dir_id] = node
        self.novel_node_dir_update(gid_rid_dict, dir_node_dict, current_novel_node_list)

        result = cluster_db.get_novelclusterchapterinfo_diridlist(table_id, dir_id_list)
        dir_chapter_dict = defaultdict(list)
        for (dir_id, chapter_sort, gid, chapter_title) in result:
            chapter_title = chapter_title.decode('GBK', 'ignore')
            chapter = NovelChapterInfo(gid = gid, dir_id = dir_id, chapter_sort = chapter_sort, chapter_title = chapter_title)
            dir_chapter_dict[dir_id].append(chapter)
        self.novel_node_chapter_update(table_id, dir_chapter_dict, current_novel_node_list)

        return True


    def novel_node_generate(self, site_id, update_time):
        """
            更新site_id站点中，更新时间大于update_time的小说信息
        """
        cluster_db = ClusterDBModule()
        novel_id_list = cluster_db.get_dirfmtinfo_id_list(site_id, update_time)

        current_novel_id_list = []
        current_novel_node_dict = defaultdict(list)
        for index, novel_id in enumerate(novel_id_list):
            current_novel_id_list.append(novel_id)
            if len(current_novel_id_list) < 500 and index < len(novel_id_list) - 1:
                continue
            self.logger.info('[site_id: {0}, current_count: {1}, total_count: {2}]'.format(site_id, index, len(novel_id_list)))

            current_novel_node_list = self.novel_node_collection(site_id, current_novel_id_list)
            current_novel_id_list = []
            for novel_node in current_novel_node_list:
                table_id = novel_node.gid % 256
                self.novel_node_integrate(novel_node)
                current_novel_node_dict[table_id].append(novel_node)
                if len(current_novel_node_dict[table_id]) == 50:
                    self.novel_node_update(table_id, current_novel_node_dict[table_id])
                    current_novel_node_dict[table_id] = []

        for (table_id, current_novel_node_list) in current_novel_node_dict.items():
            if len(current_novel_node_list) == 0:
                continue
            self.novel_node_update(table_id, current_novel_node_list)

        return True


    def run(self):
        """
        """
        self.logger.info('novel cluster node module start')

        for site_id in xrange(self.start_site_id, self.end_site_id + 1):
            if not self.site_dict.has_key(site_id):
                continue
            update_time = self.proc_time_dict['dir_fmt_info{0}'.format(site_id)]
            self.novel_node_generate(site_id, update_time)

        self.logger.info('total update dir: {0}, total insert dir: {1}'.format(
            self.update_node_number,
            self.insert_node_number
        ))
        self.logger.info('total delete chapter: {0}, total update chapter: {1}, total insert chapter: {2}'.format(
            self.delete_chapter_number,
            self.update_chapter_number,
            self.insert_chapter_number
        ))
        self.logger.info('novel cluster node module end')
        return True


if __name__ == '__main__':
    here()



