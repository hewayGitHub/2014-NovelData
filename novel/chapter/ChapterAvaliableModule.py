#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-03-27 22:27'

import logging
from basic.SilkServerModule import *
from public.BasicStringMethod import *
from novel.chapter.ChapterDB import *

def here():
    print('PrimeMusic')

class ChapterAvaliableModule(object):
    """
    """
    def __init__(self):
        """
        """
        self.logger = logging.getLogger('novel.chapter.avaliable')
        self.err = logging.getLogger('err.chapter.avaliable')

        parser = SafeConfigParser()
        parser.read('./conf/NovelChapterModule.conf')
        self.start_rid_id = parser.getint('chapter_module', 'proc_start_rid_id')
        self.end_rid_id = parser.getint('chapter_module', 'proc_end_rid_id')

        self.total_chapter_number = 0
        self.total_unavaliable_chapter_number = 0


    def optimize_chapter_collection(self, rid, align_id):
        """
        """
        silk_server = SilkServer()
        chapter_page = silk_server.get(src = 'http://test.com', pageid = '{0}|{1}'.format(rid, align_id))

        if not chapter_page:
            return False
        if not chapter_page.has_key('blocks'):
            return False
        return chapter_page


    def optimize_chapter_check(self, rid, align_id):
        """
        """
        chapter_page = self.optimize_chapter_collection(rid, align_id)
        if chapter_page is False:
            chapter_page = self.optimize_chapter_collection(rid, align_id)
        if chapter_page is False:
            chapter_page = self.optimize_chapter_collection(rid, align_id)
        if chapter_page is False:
            return False

        raw_chapter_content = ''
        for block in chapter_page['blocks']:
            if block.has_key('type') and block['type'] == 'NOVELCONTENT':
                raw_chapter_content = block['data_value']

        chapter_chinest_count = 0
        for char in raw_chapter_content:
            if is_chinese(char):
                chapter_chinest_count += 1
        if chapter_chinest_count < 10:
            return False
        return chapter_chinest_count


    def update_chapter_info(self, rid, align_id):
        """
        """
        chapter_db = ChapterDBModule()
        chapter_db.update_novelaggregationdir_init(rid, align_id)


    def aggregation_dir_check(self, rid):
        """
        """
        chapter_db = ChapterDBModule()
        aggregation_dir_list = chapter_db.get_novelaggregationdir_all(rid)

        avaliable_chapter_num = 0
        for (chapter_index, align_id, chapter_id, chapter_url, chapter_title, optimize_chapter_wordsum) in aggregation_dir_list:
            self.logger.info('chapter_index: {0}, chapter_title: {1}'.format(chapter_index, chapter_title))
            if optimize_chapter_wordsum == 0:
                continue
            flag = self.optimize_chapter_check(rid, align_id)
            if flag is False:
                self.update_chapter_info(rid, align_id)
                continue
            avaliable_chapter_num += 1
            self.logger.info('chapter optimize OK!')

        self.logger.info('rid: {0}, unavaliable: {1}/{2}'.format(rid, len(aggregation_dir_list) - avaliable_chapter_num, len(aggregation_dir_list)))


    def unavaliable_chapter_count(self, rid):
        """
        """
        chapter_db = ChapterDBModule()
        aggregation_dir_list = chapter_db.get_novelaggregationdir_all(rid)

        avaliable_chapter_num = 0
        for (chapter_index, align_id, chapter_id, chapter_url, chapter_title, optimize_chapter_wordsum) in aggregation_dir_list:
            if optimize_chapter_wordsum == 0:
                self.logger.info('chapter_index: {0}, chapter_title: {1}'.format(chapter_index, chapter_title))
                continue
            avaliable_chapter_num += 1
        self.logger.info('rid: {0}, unavaliable: {1}/{2}'.format(rid, len(aggregation_dir_list) - avaliable_chapter_num, len(aggregation_dir_list)))
        self.total_chapter_number += len(aggregation_dir_list)
        self.total_unavaliable_chapter_number += len(aggregation_dir_list) - avaliable_chapter_num


    def top_candidate_rid_collection(self):
        """
        """
        rid_list = []
        result = [int(line.strip()) for line in open('./data/rid.txt', 'r').readlines()]
        for index, rid in enumerate(result):
            if index <= self.end_rid_id and index >= self.start_rid_id:
                rid_list.append(rid)
        return rid_list


    def total_candidate_rid_collection(self):
        """
        """
        chapter_db = ChapterDBModule()

        rid_list = []
        for table_id in xrange(0, 256):
            if table_id > self.end_rid_id or table_id < self.start_rid_id:
                continue
            result = chapter_db.get_novelaggregationdir_rid(table_id)
            rid_list.extend(result)
        return rid_list


    def run(self):
        """
        """
        rid_list = self.top_candidate_rid_collection()
        #rid_list = self.total_candidate_rid_collection()

        for index, rid in enumerate(rid_list):
            self.logger.info('index: {0}, rid: {1}'.format(index, rid))
            #self.aggregation_dir_check(rid)
            self.unavaliable_chapter_count(rid)

        self.logger.info('total unavaliable chapter number: {0}'.format(self.total_unavaliable_chapter_number))
        self.logger.info('total chapter number: {0}'.format(self.total_chapter_number))
        self.logger.info('avaliable module end!')


if __name__ == '__main__':
    here()    







