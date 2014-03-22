#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-03-17 16:37'

import logging
from public.BasicStringMethod import *

def here():
    print('PrimeMusic')


class NovelBasicFilter(object):
    """
    """
    def __init__(self):
        """
        """
        self.logger = logging.getLogger('novel.chapter.filter')
        self.err = logging.getLogger('err.chapter.filter')


    def filter(self, candidate_chapter_list):
        """
        """
        print('******************************************************************')
        total_count = 0
        for chapter in candidate_chapter_list:
            count = 0
            for char in chapter.chapter_content:
                if is_chinese(char):
                    count += 1
            print('chapter_title: {0}, chapter_url: {1}, chapter_count: {2}/{3}'.format(
                chapter.chapter_title,
                chapter.chapter_url,
                count,
                len(chapter.chapter_content)
            ))
            total_count += len(chapter.chapter_content)
        print(total_count / len(candidate_chapter_list))

        return candidate_chapter_list


if __name__ == '__main__':
    here()    







