#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-11 15:42'


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
            u'��', u'һ', u'��', u'��', u'��', u'��', u'��', u'��', u'��', u'��', u'ʮ', u'��', u'ǧ'
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
                    format_chapter_title += u'#'
                flag = False
        return format_chapter_title


    def chapter_title_format(self, chapter_list):
        """
            �½ڱ����һ����
            1.  �����ֵ��ַ�ͳһ��һ��Ϊ#����������ϲ�
            2.  �ѷ����ַ�ͳһ��һ��Ϊ*����������ϲ�
        """
        for chapter in chapter_list:
            chapter.chapter_title = self.number_char_format(chapter.chapter_title)
            chapter.chapter_title = self.illegal_char_format(chapter.chapter_title)


    def common_prefix_generate(self, chapter_list):
        """
        """
        trie = Trie()
        for chapter in chapter_list:
            trie.insert_string(chapter.chapter_title)

        count = int(len(chapter_list) * 0.7) + 1
        common_prefix = trie.find_common_prefix(trie.root, count, '')
        return common_prefix


    def common_prefix_filter(self, chapter_list):
        """
            ����ǰ׺���ˣ�
            1.  ��chapter_title����Trie��
            2.  ��Trie����ѡ����ִ�������70%�������ǰ׺
        """
        common_prefix = self.common_prefix_generate(chapter_list)
        length = len(common_prefix)

        for chapter in chapter_list:
            if chapter.chapter_title[0 : length] == common_prefix:
                chapter.chapter_title = chapter.chapter_title[length : ]


    def useless_suffix_generate(self, chapter):
        """
        """
        useless_suffix = ''
        if chapter.raw_chapter_title[-1] not in [u']', u')', u'}', u'��', u'��', u'}']:
            return useless_suffix

        for index in xrange(2, len(chapter.chapter_title)):
            if chapter.chapter_title[-index] == u'*':
                useless_suffix = chapter.chapter_title[-(index - 1) : -1]
                break
        return useless_suffix


    def useless_suffix_check(self, index, chapter_list, useless_suffix):
        """
        """
        chapter_title = chapter_list[index].chapter_title
        length = len(chapter_title) - len(useless_suffix) - 2

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
            �������õ��½ڱ����׺��
            1.  �ҳ�chapter_title���ԣ�...����...����β���ַ�����׺
            2.  �ж�chapter_titleȥ����׺����Լ�ǰ���chapter_title�Ƿ���ͬ
        """
        for index, chapter in enumerate(chapter_list):
            useless_suffix = self.useless_suffix_generate(chapter)
            if not useless_suffix:
                continue
            if self.useless_suffix_check(index, chapter_list, useless_suffix):
                length = len(chapter.chapter_title) - len(useless_suffix) - 2
                chapter.chapter_title = chapter.chapter_title[0 : length]


    def novel_chapter_clean(self, novel_node):
        """
            С˵�½ڱ�������
            1.  ��chapter_title���й�һ��
            2.  ����chapter_title�еĹ���ǰ׺
            3.  ����chapter_title�е����õĺ�׺
        """
        for chapter in novel_node.chapter_list:
            chapter.chapter_title.replace(novel_node.book_name, u'')
            chapter.chapter_title.replace(novel_node.pen_name, u'')

        self.chapter_title_format(novel_node.chapter_list)
        self.common_prefix_filter(novel_node.chapter_list)
        self.useless_suffix_filter(novel_node.chapter_list)

        for chapter in novel_node.chapter_list:
            chapter.chapter_title = string_filter(chapter.chapter_title)


if __name__ == '__main__':

    clean = NovelCleanModule()
    novel_node = NovelNodeInfo(book_name = u'����ǧ��', pen_name = u'��������')
    novel_node.chapter_list = []
    novel_node.chapter_list.append(NovelChapterInfo(chapter_title = u'��һ��.���ˣ�1��'))
    novel_node.chapter_list.append(NovelChapterInfo(chapter_title = u'��һ��.���ˣ�2��'))
    novel_node.chapter_list.append(NovelChapterInfo(chapter_title = u'�ڶ���.��ѪħŮ��1��'))
    novel_node.chapter_list.append(NovelChapterInfo(chapter_title = u'�ڶ���.��ѪħŮ��2��'))
    novel_node.chapter_list.append(NovelChapterInfo(chapter_title = u'������.�¼��1��'))
    novel_node.chapter_list.append(NovelChapterInfo(chapter_title = u'��ʮһ��.�ԣ�1��'))
    novel_node.chapter_list.append(NovelChapterInfo(chapter_title = u'��ʮһ��.�ԣ�2��'))
    novel_node.chapter_list.append(NovelChapterInfo(chapter_title = u'��ʮ����.��������£�3��'))
    clean.novel_chapter_clean(novel_node)
    for chapter in novel_node.chapter_list:
        print(chapter.chapter_title.encode('utf8', 'ignore'))
        print(chapter.raw_chapter_title.encode('utf8', 'ignore'))

    here()    







