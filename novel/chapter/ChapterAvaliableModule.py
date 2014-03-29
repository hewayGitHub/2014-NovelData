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


    def aggregate_dir_generate(self, rid):
        """
            ��ȡһ��С˵�ľۺ�Ŀ¼
        """
        chapter_db = ChapterDBModule()
        result = chapter_db.get_novelaggregationdir_all(rid)

        aggregate_dir_list = []
        for (chapter_index, chapter_id, chapter_url, optimize_chapter_status, optimize_chapter_wordsum) in result:
            aggregate_dir_list.append((chapter_index, chapter_id, chapter_url, optimize_chapter_status, optimize_chapter_wordsum))
        return aggregate_dir_list


    def novel_avaliable_generate(self, rid):
        """
        """
        chapter_db = ChapterDBModule()

        unavaliable_count = 0
        aggregation_list = self.aggregate_dir_generate(rid)
        for (chapter_index, chapter_id, chapter_url, optimize_chapter_status, optimize_chapter_wordsum) in aggregation_list:
            if optimize_chapter_wordsum > 0:
                continue
            unavaliable_count += 1

        self.total_chapter_count += len(aggregation_list)
        self.unavaliable_chapter_count += unavaliable_count
        self.logger.info('rid: {0}, avaliable: {1}/{2}'.format(rid, unavaliable_count, len(aggregation_list)))


    def run(self):
        """
        """
        rid_list = []
        for line in open('./data/rid.txt', 'r').readlines():
            rid = int(line.strip())
            rid_list.append(rid)

        for index, rid in enumerate(rid_list):
            self.novel_avaliable_generate(rid)

        self.logger.info('avaliable: {0}/{1}'.format(self.unavaliable_chapter_count, self.total_chapter_count))


if __name__ == '__main__':
    here()    







