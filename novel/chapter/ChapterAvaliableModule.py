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

        self.total_chapter_count = 0
        self.unavaliable_chapter_count = 0


    def optimize_chapter_check(self, rid, align_id):
        """
        """
        silk_server = SilkServer()

        chapter_page = silk_server.get(src = 'http://test.com', pageid = '{0}|{1}'.format(rid, align_id))
        if not chapter_page:
            return False
        if not chapter_page.has_key('blocks'):
            return False

        raw_chapter_content = ''
        for block in chapter_page['blocks']:
            if block.has_key('type') and block['type'] == 'NOVELCONTENT':
                raw_chapter_content = block['data_value']
        raw_chapter_content = html_filter(raw_chapter_content)
        if len(raw_chapter_content) < 50:
            return False

        return chapter_page


    def update_chapter_info(self, rid, align_id):
        """
        """
        chapter_db = ChapterDBModule()
        chapter_db.update_novelaggregationdir_init(rid, align_id)


    def update_chapter_content(self, rid, align_id, chapter_page):
        """
        """
        silk_server = SilkServer()
        silk_server.save('{0}|{1}'.format(rid, align_id), chapter_page)


    def aggregation_dir_check(self, rid, flag = False):
        """
        """
        chapter_db = ChapterDBModule()
        aggregation_dir_list = chapter_db.get_novelaggregationdir_all(rid)

        avaliable_chapter_num = 0
        for (chapter_index, align_id, chapter_id, chapter_url, chapter_title, optimize_chapter_wordsum) in aggregation_dir_list:
            self.logger.info('chapter_index: {0}, chapter_title: {1}'.format(chapter_index, chapter_title))
            if optimize_chapter_wordsum == 0:
                continue
            if flag is False:
                avaliable_chapter_num += 1
                continue

            chapter_page = self.optimize_chapter_check(rid, align_id)
            if chapter_page is False:
                self.err.warning('rid: {0}, align_id: {1}, chapter_index: {2}, chapter_title: {3}'.format(
                    rid, align_id, chapter_index, chapter_title))
                self.update_chapter_info(rid, align_id)
                continue

            if len(chapter_page['url']) < 4:
                self.logger.info('rid: {0}, align_id: {1}, chapter_index: {2}, chapter_title: {3}'.format(
                    rid, align_id, chapter_index, chapter_title))
                chapter_page['url'] = chapter_url
                self.update_chapter_content(rid, align_id, chapter_page)
                continue

            avaliable_chapter_num += 1

        self.logger.info('rid: {0}, avaliable: {1}, total: {2}'.format(rid, avaliable_chapter_num, len(aggregation_dir_list)))



    def run(self):
        """
        """
        rid_list = []
        for line in open('./data/rid.txt', 'r').readlines():
            rid = int(line.strip())
            rid_list.append(rid)

        self.aggregation_dir_check(rid, True)

        self.logger.info('avaliable module end!')


if __name__ == '__main__':
    here()    







