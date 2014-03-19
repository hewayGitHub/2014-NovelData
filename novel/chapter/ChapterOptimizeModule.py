#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-03-17 16:36'

import logging
from collections import defaultdict

from basic.NovelStructure import *
from basic.SilkServerModule import *
from public.BasicStringMethod import *
from novel.chapter.ChapterDB import *

def here():
    print('PrimeMusic')

class ChapterOptimizeModule(object):
    """
    """
    def __init__(self):
        """
        """
        self.logger = logging.getLogger('novel.chapter')
        self.logger = logging.getLogger('err.chapter')


    def aggregate_dir_generate(self, rid):
        """
            获取一本小说的聚合目录
        """
        chapter_db = ChapterDBModule()
        result = chapter_db.get_novelauthoritydir_list(rid)

        aggregate_dir_list = []
        for (align_id, chapter_index, chapter_status) in result:
            aggregate_dir_list.append((align_id, chapter_index))
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

        dir_id_list = [chapter.dir_id for chapter in candidate_chapter_list]
        result = chapter_db.get_novelclusterdirinfo_dir(dir_id_list)

        dir_id_dict = {}
        for (dir_id, site, site_id, site_status) in result:
            dir_id_dict[dir_id] = (site, site_id, site_status)
        for chapter in candidate_chapter_list:
            dir_id = chapter.dir_id
            (site, site_id, site_status) = dir_id_dict[dir_id]
            chapter.site_id = site_id
            chapter.site_status = site_status
        return candidate_chapter_list


    def candidate_chapter_generate(self, rid, align_id):
        """
        """
        candidate_chapter_list = self.candidate_chapter_collecion(rid, align_id)

        authority_chapter_dict = defaultdict(list)
        pirate_chapter_dict = defaultdict(list)
        for chapter in candidate_chapter_list:
            site_id = chapter.site_id
            if chapter.site_status == 1:
                authority_chapter_dict[site_id].append(chapter)
            if chapter.site_status == 0:
                pirate_chapter_dict[site_id].append(chapter)

        candidate_chapter_list = []
        for (site_id, chapter_list) in authority_chapter_dict.items():
            for chapter in chapter_list:
                chapter = self.chapter_content_generate(chapter)
                if not chapter:
                    candidate_chapter_list.append(chapter)
                    break
        if len(candidate_chapter_list) > 5:
            return candidate_chapter_list
        for (site_id, chapter_list) in authority_chapter_dict.items():
            for chapter in chapter_list:
                chapter = self.chapter_content_generate(chapter)
                if not chapter:
                    candidate_chapter_list.append(chapter)
                    break
        return candidate_chapter_list


    def candidate_chapter_filter(self, candidate_chapter_list):
        """
        """
        print('*****************************************************************************')
        for chapter in candidate_chapter_list:
            print('chapter_title: {0}, chapter_url: {1}, chapter_word_sum: {2}'.format(
                chapter.chapter_title, chapter.chapter_url, len(chapter.raw_chapter_content)))


    def novel_chapter_optimize(self, rid):
        """
            一本小说章节选取入口
        """
        chapter_db = ChapterDBModule()

        result = chapter_db.get_novelclusterdirinfo_rid(rid)
        if len(result) <= 1:
            return

        aggregate_dir_list = self.aggregate_dir_generate(rid)
        for (align_id, chapter_index) in aggregate_dir_list:
            candidate_chapter_list = self.candidate_chapter_generate(rid, align_id)
            self.candidate_chapter_filter(candidate_chapter_list)
            if chapter_index > 10:
                break


    def run(self):
        """
        """
        self.novel_chapter_optimize(3994882921)



if __name__ == '__main__':
    here()    







