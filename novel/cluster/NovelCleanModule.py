#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-11 15:42'

import re
from basic.NovelStructure import *
from public.Trie import *
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
            章节标题归一化：
            1.  去除空格
            2.  把数字的字符统一归一化为0，连续多个合并
        """
        for chapter in chapter_list:
            chapter.chapter_title = re.sub(r'\s+', '', chapter.chapter_title)
            chapter.chapter_title = self.number_char_format(chapter.chapter_title)


    def strong_common_prefix_generate(self, chapter_list):
        """
        """
        trie = Trie()
        for chapter in chapter_list:
            trie.insert_string(chapter.chapter_title)

        count = int(len(chapter_list) * 0.7) + 1
        common_prefix_list = trie.find_common_prefix(trie.root, count, '')
        return common_prefix_list


    def weak_common_prefix_generate(self, chapter_list):
        """
        """
        trie = Trie()
        for chapter in chapter_list:
            trie.insert_string(chapter.chapter_title)

        common_prefix_list = trie.find_common_prefix(trie.root, 10, '')
        return common_prefix_list


    def common_prefix_filter(self, chapter_list):
        """
            公共前缀过滤：
            1.  用chapter_title建立Trie树
            2.  在Trie树中找出chapter_title的强公共前缀（覆盖70%以上），进行弱过滤（前缀子串）
            3.  在Trie树中找出chapter_title的弱公共前缀（出现10次以上），进行强过滤（完全匹配）
        """
        if len(chapter_list) == 1:
            return

        strong_common_prefix_list = self.strong_common_prefix_generate(chapter_list)
        for common_prefix in strong_common_prefix_list:
            for chapter in chapter_list:
                index = 0
                for char in common_prefix:
                    if index >= len(chapter.chapter_title):
                        break
                    if chapter.chapter_title[index] == char:
                        index += 1
                chapter.chapter_title = chapter.chapter_title[index : ]

        weak_common_prefix_list = self.weak_common_prefix_generate(chapter_list)
        for common_prefix in weak_common_prefix_list:
            length = len(common_prefix)
            if length == 0 or length > 5:
                continue
            for chapter in chapter_list:
                if len(chapter.chapter_title) - length < 2:
                    continue
                if chapter.chapter_title[0 : length] == common_prefix:
                    chapter.chapter_title = chapter.chapter_title[length : ]


    def manual_prefix_filter(self, chapter_title):
        """
            暴力方式，手工去除一些badcase
        """
        chapter_title = re.sub(u'VIP', '', chapter_title)
        chapter_title = re.sub(u'^0?第?0[章|回|节]', '', chapter_title)
        chapter_title = re.sub(u'^.*第0[章|回|节]', '', chapter_title)
        return chapter_title


    def number_char_recover(self, chapter_title, raw_chapter_title):
        """
            恢复chapter_title中被归一化的数字字符
        """
        recover_chapter_title = ''

        index = len(raw_chapter_title) - 1
        for i in xrange(0, len(chapter_title)):
            j = len(chapter_title) - i - 1
            char = chapter_title[j]

            if char != u'0':
                recover_chapter_title += char
                continue

            s = None
            e = None
            while index >= 0:
                char = raw_chapter_title[index]
                if self.number_char_dict.has_key(char):
                    e = index
                    break
                else:
                    index -= 1
            while index >= 0:
                char = raw_chapter_title[index]
                if self.number_char_dict.has_key(char):
                    index -= 1
                    if index == -1:
                        s = index
                    continue
                else:
                    s = index
                    break
            if (s is None) or (e is None):
                continue

            recover_chapter_title += raw_chapter_title[s + 1 : e + 1][::-1]

        recover_chapter_title = recover_chapter_title[::-1]
        return recover_chapter_title


    def useless_suffix_generate(self, chapter):
        """
        """
        useless_suffix = ''
        for index in xrange(1, len(chapter.chapter_title)):
            char = chapter.chapter_title[-index]
            if char not in [u'(', u'[', u'（', u'【']:
                continue
            useless_suffix = chapter.chapter_title[-index : ]
        return useless_suffix


    def useless_suffix_check(self, index, chapter_list, useless_suffix):
        """
        """
        chapter_title = chapter_list[index].chapter_title
        length = len(chapter_title) - len(useless_suffix)
        if index != 0:
            pre_chapter_title = chapter_list[index - 1].chapter_title
            if chapter_title[0 : length] == pre_chapter_title[0 : length]:
                return False

        if index != len(chapter_list) - 1:
            next_chapter_title = chapter_list[index + 1].chapter_title
            if chapter_title[0 : length] == next_chapter_title[0 : length]:
                return False
        return True


    def useless_suffix_filter(self, chapter_list):
        """
            过滤无用的章节标题后缀：
            1.  找出chapter_title中以（...）【...】结尾的字符串后缀
            2.  判断chapter_title去掉后缀后和自己前后的chapter_title是否相同
        """
        for index, chapter in enumerate(chapter_list):
            useless_suffix = self.useless_suffix_generate(chapter)
            if not useless_suffix:
                continue
            if self.useless_suffix_check(index, chapter_list, useless_suffix):
                length = len(chapter.chapter_title) - len(useless_suffix)
                chapter.chapter_title = chapter.chapter_title[0 : length]


    def novel_chapter_clean(self, novel_node):
        """
            小说章节标题清理：
            1.  对chapter_title中的数字，符号做归一化处理
            2.  过滤chapter_title中的公共前缀，剩下的部分恢复数字
            3.  过滤chapter_title中的无用的后缀
        """
        for chapter in novel_node.chapter_list:
            chapter.chapter_title = string_Q2B(chapter.chapter_title)
            chapter.chapter_title = chapter.chapter_title.replace(novel_node.book_name, u'')
            chapter.chapter_title = chapter.chapter_title.replace(novel_node.pen_name, u'')

        self.chapter_title_format(novel_node.chapter_list)
        self.common_prefix_filter(novel_node.chapter_list)
        for chapter in novel_node.chapter_list:
            chapter.chapter_title = self.manual_prefix_filter(chapter.chapter_title)
            chapter.chapter_title = self.number_char_recover(chapter.chapter_title, chapter.raw_chapter_title)

        self.useless_suffix_filter(novel_node.chapter_list)
        for chapter in novel_node.chapter_list:
            chapter.chapter_title = string_filter(chapter.chapter_title)


if __name__ == '__main__':

    clean = NovelCleanModule()
    novel_node = NovelNodeInfo(book_name = u'络泪千秋', pen_name = u'言若珂月')
    novel_node.chapter_list = []
    novel_node.chapter_list.append(NovelChapterInfo(chapter_title = u'络泪千秋 第一章.旅人（一）'))
    novel_node.chapter_list.append(NovelChapterInfo(chapter_title = u'第1章.旅人（二）'))
    novel_node.chapter_list.append(NovelChapterInfo(chapter_title = u'第2章.炼血魔女（上）'))
    novel_node.chapter_list.append(NovelChapterInfo(chapter_title = u'第８章.炼血魔女（下）'))
    novel_node.chapter_list.append(NovelChapterInfo(chapter_title = u'第五章.  落泪（第一更'))
    novel_node.chapter_list.append(NovelChapterInfo(chapter_title = u'第十一章.暝（1）'))
    novel_node.chapter_list.append(NovelChapterInfo(chapter_title = u'第十一.暝（2）'))
    novel_node.chapter_list.append(NovelChapterInfo(chapter_title = u'第十五章.3十二旧事（三）'))
    novel_node.chapter_list.append(NovelChapterInfo(chapter_title = u'第十五章.  【剑脉，红菱】 '))
    novel_node.chapter_list.append(NovelChapterInfo(chapter_title = u'十五章.[灵境，牧]'))
    novel_node.chapter_list.append(NovelChapterInfo(chapter_title = u'第30深 他是真的喜欢她'))
    clean.novel_chapter_clean(novel_node)
    for chapter in novel_node.chapter_list:
        print(chapter.chapter_title.encode('utf8', 'ignore'))
        print(chapter.raw_chapter_title.encode('utf8', 'ignore'))

    here()    







