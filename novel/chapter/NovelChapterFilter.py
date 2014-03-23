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


    def chapter_initialize(self, candidate_chapter_list):
        """
        """
        for chapter in candidate_chapter_list:
            chapter.sentence_set = set()
            chapter.feature_list = []
            chapter.nosiy_point = 0
            chapter.edge_list = []


    def chapter_sentence_generate(self, chapter):
        """
            单个章节章节特征句提取
        """
        sentence_list = []

        sentence = ''
        for char in chapter.chapter_content:
            if is_legal(char):
                sentence += char
            else:
                if len(sentence) > 5 and len(sentence) < 50:
                    sentence_list.append(sentence)
                sentence = ''

        chapter.sentence_set.update(sentence_list)
        return sentence_list


    def feature_sentence_generate(self, candidate_chapter_list):
        """
            计算所有章节的公共特征句，生成每个章节的特征向量和噪音点
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
        for (sentence, (site_id, site_count, total_count)) in chapter_feature_list[::-1][0: 50]:
            for chapter in candidate_chapter_list:
                if sentence in chapter.sentence_set:
                    chapter.feature_list.append(1)
                else:
                    chapter.feature_list.append(0)

        threshold = max(len(candidate_chapter_list) * 0.3, 1.0)
        for (sentence, (site_id, site_count, total_count)) in chapter_feature_list:
            if site_count > threshold:
                break
            for chapter in candidate_chapter_list:
                if sentence in chapter.sentence_set:
                    chapter.nosiy_point += 1


    def chapter_similarity_caculation(self, vector_x, vector_y):
        """
            计算两个章节内容的相似度
        """
        count_x = sum(vector_x)
        count_y = sum(vector_y)
        count = sum([vector_x[index] * vector_y[index] for index in xrange(0, len(vector_x))])

        return 1.0 * count * count / (count_x * count_y + 1)


    def chapter_cluster_generate(self, candidate_chapter_list):
        """
            选出最大簇内的章节，过滤小簇的章节
        """
        max_count = 0
        candidate_chapter = None
        for chapter_x in candidate_chapter_list:
            count = 0
            for chapter_y in candidate_chapter_list:
                similarity = self.chapter_similarity_caculation(chapter_x.feature_list, chapter_y.feature_list)
                if similarity >= 0.9:
                    count += 1
                chapter_x.edge_list.append(similarity)
            if count > max_count:
                max_count = count
                candidate_chapter = chapter_x
        self.logger.info('max_cluster_count: {0}/{1}'.format(max_count, len(candidate_chapter_list)))
        if max_count < 2:
            return candidate_chapter_list

        candidate_chapter_cluster = []
        for index, similarity in enumerate(candidate_chapter.edge_list):
            if similarity < 0.9:
                self.logger.info('filter chapter url: {0}'.format(candidate_chapter_list[index].chapter_url))
                continue
            chapter = candidate_chapter_list[index]
            candidate_chapter_cluster.append(chapter)

        return candidate_chapter_cluster


    def nosiy_point_filter(self, candidate_chapter_list):
        """
            过滤一些噪音点
        """
        candidate_chapter_list = sorted(candidate_chapter_list, key = lambda x: x.nosiy_point)
        if len(candidate_chapter_list) <= 3:
            return candidate_chapter_list
        return candidate_chapter_list[0 : len(candidate_chapter_list) / 2]


    def filter(self, candidate_chapter_list):
        """
            过滤错误章节
        """
        self.chapter_initialize(candidate_chapter_list)
        self.feature_sentence_generate(candidate_chapter_list)

        candidate_chapter_list = self.chapter_cluster_generate(candidate_chapter_list)
        candidate_chapter_list = self.nosiy_point_filter(candidate_chapter_list)

        return candidate_chapter_list


if __name__ == '__main__':
    here()    







