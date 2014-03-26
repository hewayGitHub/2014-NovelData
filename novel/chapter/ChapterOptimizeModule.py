#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-03-17 16:36'

import logging
import random
from collections import defaultdict

from basic.NovelStructure import *
from basic.SilkServerModule import *
from public.BasicStringMethod import *
from novel.chapter.ChapterDB import *
from novel.chapter.NovelChapterFilter import *

def here():
    print('PrimeMusic')

class ChapterOptimizeModule(object):
    """
    """
    def __init__(self):
        """
        """
        self.logger = logging.getLogger('novel.chapter')
        self.err = logging.getLogger('err.chapter')

        parser = SafeConfigParser()
        parser.read('./conf/NovelChapterModule.conf')
        self.start_rid_id = parser.getint('chapter_module', 'proc_start_rid_id')
        self.end_rid_id = parser.getint('chapter_module', 'proc_end_rid_id')


    def aggregate_dir_generate(self, rid):
        """
            获取一本小说的聚合目录
        """
        chapter_db = ChapterDBModule()
        result = chapter_db.get_novelaggregationdir_list(rid)

        aggregate_dir_list = []
        for (align_id, chapter_index, chapter_status) in result:
            aggregate_dir_list.append((align_id, chapter_index, chapter_status))
        return aggregate_dir_list


    def chapter_content_generate(self, chapter):
        """
            获取一个章节的正文信息
        """
        silk_server = SilkServer()

        chapter_page = silk_server.get(src = chapter.chapter_url)
        if not chapter_page:
            return False
        if not chapter_page.has_key('blocks'):
            return False

        raw_chapter_content = ''
        for block in chapter_page['blocks']:
            if block['type'] == 'NOVELCONTENT':
                raw_chapter_content = block['data_value']
        raw_chapter_content = html_filter(raw_chapter_content)
        if len(raw_chapter_content) < 50:
            return False

        chapter.chapter_page = chapter_page
        chapter.chapter_content = raw_chapter_content
        chapter.raw_chapter_content = raw_chapter_content
        return chapter


    def candidate_chapter_collecion(self, rid, align_id):
        """
            获取一个章节的所有候选章节的基础信息
        """
        chapter_db = ChapterDBModule()

        candidate_chapter_list = []
        result = chapter_db.get_integratechapterinfo_list(rid, align_id)
        for (dir_id, chapter_id, chapter_url, chapter_title) in result:
            chapter = NovelContentInfo(rid, align_id, dir_id, chapter_id, chapter_url, chapter_title)
            if not chapter:
                continue
            candidate_chapter_list.append(chapter)

        if len(candidate_chapter_list) == 0:
            return candidate_chapter_list
        dir_id_list = [chapter.dir_id for chapter in candidate_chapter_list]
        result = chapter_db.get_novelclusterdirinfo_dir(dir_id_list)

        dir_id_dict = {}
        for (dir_id, site, site_id, site_status) in result:
            dir_id_dict[dir_id] = (site, site_id, site_status)
        for chapter in candidate_chapter_list:
            dir_id = chapter.dir_id
            if not dir_id_dict.has_key(dir_id):
                chapter.site_id = -1
                chapter.site_status = 0
                continue
            (site, site_id, site_status) = dir_id_dict[dir_id]
            chapter.site_id = site_id
            chapter.site_status = site_status
        return candidate_chapter_list


    def candidate_chapter_generate(self, rid, align_id):
        """
            根据rid和align_id获取候选章节
        """
        total_candidate_chapter_list = self.candidate_chapter_collecion(rid, align_id)
        random.shuffle(total_candidate_chapter_list)

        candidate_chapter_list = []
        site_id_dict = {}
        for index, chapter in enumerate(total_candidate_chapter_list):
            site_id = chapter.site_id
            site_status = chapter.site_status
            if site_id_dict.has_key(site_id):
                continue
            if site_status == 1 or len(candidate_chapter_list) < 10:
                chapter = self.chapter_content_generate(chapter)
                if not chapter:
                    continue
                candidate_chapter_list.append(chapter)
                site_id_dict[site_id] = True

        self.logger.info('rid: {0}, align_id: {1}, candidate_chapter_length: {2}'.format(
            rid, align_id, len(candidate_chapter_list)
        ))
        for chapter in candidate_chapter_list:
            self.logger.info('chapter_title: {0}, chapter_url: {1}, chapter_length: {2}'.format(
                chapter.chapter_title,
                chapter.chapter_url,
                len(chapter.chapter_content)
            ))
        return candidate_chapter_list


    def basic_chapter_filter(self, candidate_chapter_list):
        """
            根据基础信息进行一轮过滤
        """
        average_count = 1.0 * sum([len(chapter.chapter_content) for chapter in candidate_chapter_list]) / len(candidate_chapter_list)
        threshold_count = 0.8 * average_count

        self.logger.info('average chapter length: {0}, chapter length threshold: {1}'.format(average_count, threshold_count))
        chapter_list = []
        for chapter in candidate_chapter_list:
            if len(chapter.chapter_content) < threshold_count:
                self.logger.info('filter chapter url: {0}'.format(chapter.chapter_url))
                continue
            chapter_list.append(chapter)

        if len(chapter_list) <= len(candidate_chapter_list) / 2:
            return candidate_chapter_list
        else:
            return chapter_list


    def candidate_chapter_filter(self, candidate_chapter_list):
        """
            候选章节过滤
        """
        if len(candidate_chapter_list) < 3:
            return candidate_chapter_list

        chapter_filter = NovelChapterFilter()
        candidate_chapter_list = self.basic_chapter_filter(candidate_chapter_list)
        candidate_chapter_list = chapter_filter.filter(candidate_chapter_list)

        self.logger.info('selected_candidate_chapter_length: {0}'.format(len(candidate_chapter_list)))
        for chapter in candidate_chapter_list:
            self.logger.info('chapter_url: {0}, feature_point: {1}, nosiy_point: {2}'.format(
                chapter.chapter_url,
                sum(chapter.feature_list),
                chapter.nosiy_point
            ))

        return candidate_chapter_list


    def candidate_chapter_rank(self, candidate_chapter_list):
        """
            确定选取一章
        """
        selected_chapter = candidate_chapter_list[0]
        for chapter in candidate_chapter_list:
            chapter.chinese_count = 0
            for char in chapter.chapter_content:
                if is_chinese(char):
                    chapter.chinese_count += 1
            chapter.chinese_rate = 1.0 * chapter.chinese_count / len(chapter.chapter_content)
            if chapter.chinese_rate > selected_chapter.chinese_rate + 0.1 or chapter.chinese_count > selected_chapter.chinese_count + 200:
                selected_chapter = chapter

        self.logger.info('chapter_title: {0}, chapter_url: {1}, chapter_length: {2}/{3}'.format(
            selected_chapter.chapter_title,
            selected_chapter.chapter_url,
            selected_chapter.chinese_count,
            len(selected_chapter.chapter_content)
        ))
        return selected_chapter


    def selected_chapter_update(self, current_chapter_status, chapter, debug = False):
        """
        """
        if debug:
            print('rid: {0}'.format(chapter.rid))
            print('chapter_title: {0}, chapter_url: {1}'.format(chapter.chapter_title, chapter.chapter_url))
            print(chapter.chapter_content.encode('GBK', 'ignore'))
            return

        silk_server = SilkServer()
        silk_server.save('{0}|{1}'.format(chapter.rid, chapter.align_id), chapter.chapter_page)

        chapter_db = ChapterDBModule()
        chapter.chapter_url = "'{0}'".format(url_format(chapter.chapter_url))
        chapter_db.update_novelaggregationdir_info(current_chapter_status, chapter)


    def novel_chapter_optimize(self, rid, cluster_size):
        """
            一本小说章节选取入口
        """
        standard_chapter_status = min(cluster_size, 20) / 2

        aggregate_dir_list = self.aggregate_dir_generate(rid)
        for (align_id, chapter_index, chapter_status) in aggregate_dir_list:
            if len(aggregate_dir_list) - chapter_index > 3:
                continue
            chapter_status = 0
            if chapter_status >= standard_chapter_status:
                continue

            candidate_chapter_list = self.candidate_chapter_generate(rid, align_id)
            current_chapter_status = len(candidate_chapter_list)
            if chapter_status >= current_chapter_status:
                continue
            if current_chapter_status <= 1:
                continue

            candidate_chapter_list = self.candidate_chapter_filter(candidate_chapter_list)
            chapter = self.candidate_chapter_rank(candidate_chapter_list)
            self.selected_chapter_update(current_chapter_status, chapter, True)


    def run(self):
        rid_list = [
            3278655874,
        ]
        for rid in rid_list:
            self.novel_chapter_optimize(rid, 20)


    def run_test(self):
        """
        """
        chapter_db = ChapterDBModule()
        candidate_rid_list = chapter_db.get_noveldata_all('novel_cluster_dir_info', ['rid'])
        candidate_rid_dict = defaultdict(int)
        for (rid, ) in candidate_rid_list:
            if rid % 256 < self.start_rid_id or rid % 256 > self.end_rid_id:
                continue
            candidate_rid_dict[rid] += 1

        rid_list = candidate_rid_dict.items()
        for (index, (rid, cluster_size)) in enumerate(rid_list):
            if cluster_size <= 2:
                continue
            self.logger.info('chapter module rid: {0}/{1}'.format(index, len(rid_list)))
            self.novel_chapter_optimize(rid, cluster_size)
        self.logger.info('chapter module end !')


if __name__ == '__main__':
    here()    







