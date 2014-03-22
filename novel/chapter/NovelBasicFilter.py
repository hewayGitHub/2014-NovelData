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
        return candidate_chapter_list


if __name__ == '__main__':
    here()    







