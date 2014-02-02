#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-02 14:05'

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

class NovelChapterInfo(object):
    """
        一个章节的基础信息，章节信息作为聚类点的一个特征
    """
    def __init__(self, dir_id = 0, chapter_id = 0, chapter_url = "",
                 chapter_title = "", raw_chapter_title = "",
                 chapter_index = 0, chapter_status = 0, word_sum = 0):
        self.dir_id = dir_id
        self.chapter_id = chapter_id
        self.chapter_url = chapter_url
        self.chapter_title = chapter_title
        self.raw_chapter_title = raw_chapter_title
        self.chapter_index = chapter_index
        self.chapter_status = chapter_status
        self.word_sum = word_sum


if __name__ == '__main__':
    here()







