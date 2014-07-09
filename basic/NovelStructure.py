#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-02 14:05'

from public.BasicStringMethod import *


def here():
    print('PrimeMusic')


class Singleton(type):
    """
        单例模式
    """

    def __call__(self, *args, **kwargs):
        if '_instance' not in vars(self):
            self._instance = super(Singleton, self).__call__(*args, **kwargs)
        return self._instance


class NovelNodeInfo(object):
    """
        一本小说的基础信息，对应于小说聚类中的一个点
    """

    def __init__(self, site_id=0, site="", site_status=0,
                 dir_id=0, dir_url="",
                 gid=0, book_name="", pen_name="",
                 chapter_count=0, chapter_word_sum=0, last_chapter_title=''):
        self.site_id = site_id
        self.site = site
        self.site_status = site_status
        self.dir_id = dir_id
        self.dir_url = dir_url
        self.gid = gid
        self.rid = gid
        self.book_name = book_name
        self.pen_name = pen_name
        self.chapter_count = chapter_count
        self.chapter_word_sum = chapter_word_sum
        self.last_chapter_title = last_chapter_title
        self.chapter_list = []


    def generate_insert_tuple(self):
        """
        """
        result = (
            self.site_id, self.site, self.site_status,
            self.dir_id, url_format(self.dir_url),
            self.gid, self.rid, string_format(self.book_name), string_format(self.pen_name),
            self.chapter_count, self.chapter_word_sum, string_format(self.last_chapter_title)
        )
        return result


    def generate_update_tuple(self):
        """
        """
        result = (
            self.gid, self.rid,
            string_format(self.book_name), string_format(self.pen_name),
            self.chapter_count, string_format(self.last_chapter_title),
            self.dir_id
        )
        return result



class NovelChapterInfo(object):
    """
        一个章节的基础信息，章节信息作为聚类点的一个特征
    """

    def __init__(self, gid=0, site_id=0, dir_id=0, chapter_sort=0,
                 chapter_id=0, chapter_url="", chapter_title="", chapter_status=0, word_sum=0):
        self.gid = gid
        self.site_id = site_id
        self.dir_id = dir_id
        self.chapter_sort = chapter_sort
        self.chapter_id = chapter_id
        self.chapter_url = chapter_url
        self.chapter_title = chapter_title
        self.raw_chapter_title = chapter_title
        self.chapter_status = chapter_status
        self.word_sum = word_sum


    def generate_insert_tuple(self):
        """
        """
        result = (
            self.gid, self.site_id, self.dir_id, self.chapter_sort, self.chapter_id,
            url_format(self.chapter_url), string_format(self.chapter_title), string_format(self.raw_chapter_title),
            self.chapter_status, self.word_sum
        )
        return result


    def generate_delete_tuple(self):
        """
        """
        result = (self.dir_id, self.chapter_sort)
        return result


    def generate_update_tuple(self):
        """
        """
        result = (
            self.gid, string_format(self.chapter_title), string_format(self.raw_chapter_title),
            self.dir_id, self.chapter_sort
        )
        return result



class NovelClusterInfo(object):
    """
        一个簇的基础信息，包含gid相同的所有小说
    """

    def __init__(self, gid=0):
        """
        """
        self.gid = gid
        self.novel_node_list = []

        self.book_name = ''
        self.pen_name = ''


class ClusterEdgeInfo(object):
    """
        两点直接的边的信息，即两本小说的相似度
    """

    def __init__(self, gid_x=0, gid_y=0, similarity=0):
        """
            一条边的信息
        """
        self.gid_x = gid_x
        self.gid_y = gid_y
        self.similarity = int(similarity * 100)


    def generate_insert_tuple(self):
        """
        """
        result = (self.gid_x, self.gid_y, self.similarity)
        return result


class NovelContentInfo(object):
    """
        一本小说的章节信息
    """

    def __init__(self, rid=0, align_id=0, dir_id=0, chapter_id=0, chapter_url='', chapter_title=''):
        """
        """
        self.rid = rid
        self.align_id = align_id
        self.dir_id = dir_id
        self.chapter_id = chapter_id
        self.chapter_url = chapter_url
        self.chapter_title = chapter_title

        self.site_id = 0
        self.site_status = 0

        self.chapter_page = ''
        self.raw_chapter_content = ''  # spider爬取的正文
        self.fmt_chapter_content = ''  # 过滤和处理过Html后的正文，包含p标签
        self.pure_chapter_content = ''  # 去杂之后的正文

        self.paragraph_list = None  # 在fmt_chapter_content的基础上用于做去杂
        self.valid_word_sum = 0  # 通过html过滤和处理，以及一些公共杂质的处理之后的汉字、数字、字母的总数
        self.valid_cn_sum = 0  # 中文字符数
        self.valid_para_count = -1  # 因为paragraph_list可能包含需要被删除的段落，valid_para_count为有效段落数

        self.there_impurity = False


class NovelParagraph(object):
    """
        正文去杂中，一本小说段落的信息
    """
    def __init__(self, raw_content='', fmt_content='', para_index=0, before_word_sum=0):
        """
        """
        self.raw_content = raw_content  # html过滤和处理后的段落内容

        # 在raw_content的基础上，过滤站点级、公共串杂质之后的内容。
        # 如果段落need_remove为False，最终输出的正文为fmt_content
        self.fmt_content = fmt_content
        self.para_index = para_index  # 第几章，从0开始，便于用para_list直接索引
        self.before_word_sum = before_word_sum  # 本章之前的总字符数

        # 对应句子序列中句子的起始索引和终止索引
        self.sentence_start_index = -1
        self.sentence_end_index = -1

        self.freq = 1  # 段落在最大簇中出现的次数
        self.need_remove = False  # 表明段落整体都是杂质
        self.there_remove = False  # 表明段落中有句子需要去杂

    def __eq__(self, other):
        if type(other) is not NovelParagraph:
            return False

        if other.fmt_content == self.fmt_content:
            return True
        else:
            return False


class NovelSentence(object):
    """
        正文去杂中，一本小说句子的信息
    """

    def __init__(self, raw_content='', fmt_content='', para_index=0, before_word_sum=0):
        """
        一个句子是连续的汉字、字母和数字

        句子由两部分组成，连续的汉字、字母和数字，以及其后所有的非汉字、字母和数字
        """
        self.raw_content = raw_content  # 段落原文中句子的内容，不包含其后的符号。
        self.fmt_content = fmt_content  # 将raw_content中的数字全角转半角，字母全角转半角，并全部变小写
        self.after_punctuation = ''  # 句子后的所有标点符号
        self.para_index = para_index  # 句子所在段落的编号
        self.before_word_sum = before_word_sum  # 句子之前所有字母、数字、汉字的个数

        # 句子在需要对齐的章节中出现的次数
        self.freq = 1

        self.there_remove = False  # 为True表示句子可能包含杂质
        self.need_remove = False  # 为True表示整句是杂质
        self.need_replace = False  # 如果当前句子的内容需要被替换，其所有的内容都在fmt_content中，包括标点符号

    def __eq__(self, other):
        if type(other) is not NovelSentence:
            return False

        if other.fmt_content == self.fmt_content:
            return True
        else:
            return False


if __name__ == '__main__':
    here()







