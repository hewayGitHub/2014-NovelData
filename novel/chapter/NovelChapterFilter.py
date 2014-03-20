#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-03-17 16:38'

import logging

from public.BasicStringMethod import *

def here():
    print('PrimeMusic')


class NovelChapterFilter(object):
    """
    """
    def __init__(self):
        """
        """
        self.logger = logging.getLogger('novel.chapter.filter')
        self.err = logging.getLogger('err.chapter.filter')


    def chapter_sentence_generate(self, chapter):
        """
        """
        sentence_list = []

        sentence = ''
        for char in chapter.chapter_content:
            if is_legal(char):
                sentence += char
            else:
                if len(sentence) >= 2:
                    sentence_list.append(sentence)
                sentence = ''
        return sentence_list


    def feature_sentence_generate(self, candidate_chapter_list):
        """
        """
        chapter_feature_dict = {}
        for chapter in candidate_chapter_list:
            sentence_list = self.chapter_sentence_generate(chapter)
            for sentence in sentence_list:
                if chapter_feature_dict.has_key(sentence):
                    (site_id, site_count, total_count) = chapter_feature_dict[sentence]
                else:
                    (site_id, site_count, total_count) = (-1, 0, 0)
                if site_id != chapter.site_id:
                    site_id = chapter.site_id
                    site_count += 1
                total_count += 1
                chapter_feature_dict[sentence] = (site_id, site_count, total_count)

        chapter_feature_list = sorted(chapter_feature_dict.items(), key = lambda x: (x[1][1], x[1][2]))
        for (sentence, (site_id, site_count, total_count)) in chapter_feature_list:
            print('sentence: {0}, site_id: {1}, site_count: {2}, total_count: {3}'.format(
                sentence.encode('GBK'), site_id, site_count, total_count
            ))


    def filter(self, candidate_chapter_list):
        """
        """
        self.feature_sentence_generate(candidate_chapter_list)


if __name__ == '__main__':
    here()    







