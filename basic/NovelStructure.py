#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-02 14:05'

from public.BasicStringMethod import *


def here():
    print('PrimeMusic')


class Singleton(type) :
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
    def __init__(self, site_id = 0, site = "", site_status = 0,
                 dir_id = 0, dir_url = "",
                 gid = 0, book_name = "", pen_name = "",
                 chapter_count = 0, valid_chapter_count = 0, chapter_word_sum = 0):
        self.site_id = site_id
        self.site = site
        self.site_status = site_status
        self.dir_id = dir_id
        self.dir_url = dir_url
        self.gid = gid
        self.book_name = book_name
        self.pen_name = pen_name
        self.chapter_count = chapter_count
        self.valid_chapter_count = valid_chapter_count
        self.chapter_word_sum = chapter_word_sum
        self.chapter_list = []


    def equal(self, node):
        """
            判断两个点是否完全相同
        """
        if self.book_name != node.book_name or self.pen_name != node.pen_name or self.site_status != node.site_status:
            return False
        if len(self.chapter_list) != len(node.chapter_list):
            return False
        for index, chapter in enumerate(self.chapter_list):
            if chapter.equal(node.chapter_list[index]) is False:
                return False
        return True


    def generate_insert_tuple(self):
        """
        """
        result = (
            self.site_id, self.site, self.site_status,
            self.dir_id, self.dir_url,
            self.gid, string_format(self.book_name), string_format(self.pen_name),
            self.chapter_count, self.valid_chapter_count, self.chapter_word_sum
        )
        return result



class NovelChapterInfo(object):
    """
        一个章节的基础信息，章节信息作为聚类点的一个特征
    """
    def __init__(self, dir_id = 0, chapter_id = 0, chapter_sort = 0,
                 chapter_url = "", chapter_title = "", chapter_status = 0, word_sum = 0):
        self.dir_id = dir_id
        self.chapter_id = chapter_id
        self.chapter_sort = chapter_sort
        self.chapter_url = chapter_url
        self.chapter_title = chapter_title
        self.raw_chapter_title = chapter_title
        self.chapter_status = chapter_status
        self.word_sum = word_sum


    def equal(self, chapter):
        """
            判断两个章节是否完全相同
        """
        if self.chapter_id != chapter.chapter_id or self.chapter_title != chapter.chapter_title:
            return False
        return True


    def generate_insert_tuple(self):
        """
        """
        result = (
            self.dir_id, self.chapter_id, self.chapter_sort,
            self.chapter_url, string_format(self.chapter_title), string_format(self.raw_chapter_title),
            self.chapter_status, self.word_sum
        )
        return result



class NovelEdgeInfo(object):
    """
        两点直接的边的信息，即两本小说的相似度
    """
    def __init__(self, dir_id_i = 0, dir_id_j = 0, similarity = 0):
        """
            一条边的信息
        """
        self.dir_id_i = dir_id_i
        self.dir_id_j = dir_id_j
        self.similarity = similarity

    def generate_insert_tuple(self):
        """
        """
        result = (self.dir_id_i, self.dir_id_j, self.similarity)
        return result

if __name__ == '__main__':
    here()







