#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-11 15:42'

import re

from basic.NovelStructure import *
from public.BasicStringMethod import *


def here():
    print('PrimeMusic')


class NovelCleanModule(object):
    """
    """
    __metaclass__ = Singleton

    def __init__(self):
        """
        """
        number_char_list = [
            u'0', u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9',
            u'零', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九', u'十', u'百', u'千'
        ]
        self.number_char_dict = {}
        for number_char in number_char_list:
            self.number_char_dict[number_char] = 1


    def illegal_char_format(self, chapter_title):
        """
        """
        format_chapter_title = ''
        flag = True
        for char in chapter_title:
            if is_legal(char):
                format_chapter_title += char
                flag = True
            else:
                if flag:
                    format_chapter_title += u'*'
                flag = False
        return format_chapter_title


    def number_char_format(self, chapter_title):
        """
        """
        format_chapter_title = ''
        flag = True
        for char in chapter_title:
            if not self.number_char_dict.has_key(char):
                format_chapter_title += char
                flag = True
            else:
                if flag:
                    format_chapter_title += u'0'
                flag = False
        return format_chapter_title


    def chapter_title_format(self, chapter_list):
        """
        """
        for chapter in chapter_list:
            chapter.chapter_title = self.number_char_format(chapter.chapter_title)
            chapter.chapter_title = self.illegal_char_format(chapter.chapter_title)


    def common_prefix_generate(self, chapter_list):
        """
        """

    def novel_chapter_clean(self, novel_node):
        """
        """

if __name__ == '__main__':

    clean = NovelCleanModule()
    chapter_title = u'第二三章   可口可乐！（上）（求月票）'
    chapter_title = clean.illegal_char_format(chapter_title)
    print(chapter_title.encode('utf8', 'ignore'))
    chapter_title = clean.number_char_format(chapter_title)
    print(chapter_title.encode('utf8', 'ignore'))

    here()    







