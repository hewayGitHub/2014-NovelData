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
                 chapter_count = 0, chapter_word_sum = 0, last_chapter_title = ''):
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
            self.gid,
            string_format(self.book_name), string_format(self.pen_name),
            self.chapter_count, string_format(self.last_chapter_title),
            self.dir_id
        )
        return result



class NovelChapterInfo(object):
    """
        一个章节的基础信息，章节信息作为聚类点的一个特征
    """
    def __init__(self, gid = 0, site_id = 0, dir_id = 0, chapter_sort = 0,
                 chapter_id = 0, chapter_url = "", chapter_title = "", chapter_status = 0, word_sum = 0):
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



class NovelClusterInfo(object):
    """
        一个簇的基础信息，包含gid相同的所有小说
    """
    def __init__(self, gid = 0):
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
    def __init__(self, gid_x = 0, gid_y = 0, similarity = 0):
        """
            一条边的信息
        """
        self.gid_x = gid_x
        self.gid_y = gid_y
        self.similarity = int(similarity * 10)


    def generate_insert_tuple(self):
        """
        """
        result = (min(self.gid_x, self.gid_y), max(self.gid_x, self.gid_y), self.similarity)
        return result


class NovelContentInfo(object):
    """
        一本小说的章节信息
    """
    def __init__(self, rid = 0, align_id = 0, dir_id = 0, chapter_id = 0, chapter_url = '', chapter_title = ''):
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
        self.chapter_content = ''
        self.raw_chapter_content = ''




if __name__ == '__main__':
    here()







