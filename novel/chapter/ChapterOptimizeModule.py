#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-03-17 16:36'

import logging
import random
from collections import defaultdict

from basic.NovelStructure import *
from basic.SilkServerModule import *
from novel.chapter.ChapterDB import *
from novel.chapter.NovelChapterFilter import *
from novel.chapter.ChapterContentFilter import *
import codecs


def here():
    print('PrimeMusic')


class ChapterOptimizeModule(object):
    """
    """

    def __init__(self):
        """
        """
        self.logger = logging.getLogger('novel.chapter')
        self.err = logging.getLogger('err.chapter')

        parser = SafeConfigParser()
        parser.read('./conf/NovelChapterModule.conf')
        self.start_rid_id = parser.getint('chapter_module', 'proc_start_rid_id')
        self.end_rid_id = parser.getint('chapter_module', 'proc_end_rid_id')


    def chapter_content_generate(self, chapter):
        """
            获取一个章节的正文信息

            修改为如果中文字数少于20，过滤掉
        """
        silk_server = SilkServer()

        chapter_page = silk_server.get(src=chapter.chapter_url)
        if not chapter_page:
            return False
        if not chapter_page.has_key('novel_chapter_type'):
            return False
        if chapter_page['novel_chapter_type'] != 0:
            return False
        if not chapter_page.has_key('blocks'):
            return False

        raw_chapter_content = ''
        for block in chapter_page['blocks']:
            if 'type' in block and block['type'] == 'NOVELCONTENT':
                raw_chapter_content = block['data_value']

        if len(raw_chapter_content) == 0:
            return False

        # 返回段落列表
        chapter_content_filter = ChapterContentFilter()
        chapter.fmt_chapter_content, chapter.paragraph_list, chapter.valid_para_count \
            = chapter_content_filter.get_paras(raw_chapter_content, chapter.site_id, chapter.chapter_title)

        if len(chapter.fmt_chapter_content) == 0 or len(chapter.paragraph_list) == 0:  # 有些情况下，raw_chapter_content中只有html标签，为内容，通过html过滤之后，文本是空
            return False
        # chapter.valid_word_sum = chapter.paragraph_list[-1].before_word_sum + len(
        #     chapter.paragraph_list[-1].fmt_content)
        chapter.valid_word_sum, chapter.valid_cn_sum = count_word(chapter.fmt_chapter_content)

        if chapter.valid_cn_sum < 20:
            self.logger.info('count of chinese is less than 20 url:{0}'.format(chapter.chapter_url))
            return False

        chapter.chapter_page = chapter_page
        chapter.raw_chapter_content = raw_chapter_content
        return chapter


    def candidate_chapter_collecion(self, rid, align_id):
        """
            获取一个章节的所有候选章节的基础信息
        """
        chapter_db = ChapterDBModule()

        candidate_chapter_list = []
        result = chapter_db.get_integratechapterinfo_list(rid, align_id)
        for (dir_id, chapter_id, chapter_url, chapter_title) in result:
            chapter = NovelContentInfo(rid, align_id, dir_id, chapter_id, chapter_url, chapter_title)
            candidate_chapter_list.append(chapter)
        if len(candidate_chapter_list) == 0:
            return candidate_chapter_list

        dir_id_list = [chapter.dir_id for chapter in candidate_chapter_list]
        result = chapter_db.get_novelclusterdirinfo_dir(dir_id_list)
        dir_id_dict = {}
        for (dir_id, site, site_id, site_status) in result:
            dir_id_dict[dir_id] = (site, site_id, site_status)

        for chapter in candidate_chapter_list:
            dir_id = chapter.dir_id
            if not dir_id_dict.has_key(dir_id):
                chapter.site_id = -1
                chapter.site_status = 0
                continue
            (site, site_id, site_status) = dir_id_dict[dir_id]
            chapter.site_id = site_id
            chapter.site_status = site_status
        return candidate_chapter_list


    def candidate_chapter_generate(self, rid, align_id, total_candidate_chapter_list):
        """
            根据rid和align_id获取候选章节

            一个站点只选取一个候选，如果已选取超过15个候选，除非是正版站资源，否则忽略
        """
        random.shuffle(total_candidate_chapter_list)

        candidate_chapter_list = []
        site_id_dict = {}
        for index, chapter in enumerate(total_candidate_chapter_list):
            site_id = chapter.site_id
            site_status = chapter.site_status
            if site_id_dict.has_key(site_id):
                continue
            if site_status == 1 or len(candidate_chapter_list) < 15:
                chapter = self.chapter_content_generate(chapter)
                if not chapter:
                    continue
                candidate_chapter_list.append(chapter)
                site_id_dict[site_id] = True

        self.logger.info('candidate_chapter_length: {0}'.format(len(candidate_chapter_list)))
        for chapter in candidate_chapter_list:
            self.logger.info('chapter_title: {0}, chapter_url: {1}, chapter_length: {2}'.format(
                chapter.chapter_title,
                chapter.chapter_url,
                chapter.valid_word_sum
            ))
        return candidate_chapter_list


    def basic_chapter_filter(self, candidate_chapter_list):
        """
           为了方便后面段落和句子的对齐，根据中文字数和段落数过滤最大簇的候选章节

           过滤最大簇中字数特别少的（小于平均的80%），以及段落数特别少和特别大的
           同时保证如果候选章节数不少于5，返回的候选章节数不少于3个候选
        """
        if len(candidate_chapter_list) < 4:
            return candidate_chapter_list

        cn_sum_list = sorted([chapter.valid_cn_sum for chapter in candidate_chapter_list])
        cn_average_count = 1.0 * sum(cn_sum_list) / len(candidate_chapter_list)
        cn_threshold_count = 0.8 * cn_average_count

        self.logger.info('average chinese length: {0}, chinese length threshold: {1}'
                         .format(cn_average_count, cn_threshold_count))
        word_chapter_list = []
        for chapter in candidate_chapter_list:
            if chapter.valid_cn_sum < cn_threshold_count:
                self.logger.info('filter chapter for chinese url: {0} chinese length: {1}'.
                                 format(chapter.chapter_url, chapter.valid_cn_sum))
                continue
            word_chapter_list.append(chapter)

        if len(word_chapter_list) < 4:
            return word_chapter_list

        para_count_list = sorted([chapter.valid_para_count for chapter in word_chapter_list])
        valid_num = len(para_count_list) * 3 / 4 - len(para_count_list) / 4
        avg_para_count = sum(para_count_list[len(para_count_list) / 4:len(para_count_list) * 3 / 4]) / valid_num
        lower_threshold_count = min(0.6 * avg_para_count, para_count_list[len(para_count_list) / 4])
        upper_threshold_count = max(1.3 * avg_para_count, para_count_list[len(para_count_list) * 3 / 4])
        self.logger.info('average para count: {0}, para threshold: {1}-{2}'
                         .format(avg_para_count, lower_threshold_count, upper_threshold_count))

        para_chapter_list = []
        for chapter in word_chapter_list:
            if chapter.valid_para_count < lower_threshold_count or chapter.valid_para_count > upper_threshold_count:
                self.logger.info('filter chapter for para url: {0} para count: {1}'.
                                 format(chapter.chapter_url, chapter.valid_para_count))
                continue
            para_chapter_list.append(chapter)

        if len(para_chapter_list) < 3:
            return word_chapter_list
        else:
            return para_chapter_list


    def candidate_chapter_filter(self, candidate_chapter_list):
        """
            候选章节过滤
        """
        if len(candidate_chapter_list) < 3:
            return candidate_chapter_list

        chapter_filter = NovelChapterFilter()
        candidate_chapter_list = chapter_filter.filter(candidate_chapter_list)

        self.logger.info('selected_candidate_chapter_length: {0}'.format(len(candidate_chapter_list)))
        for chapter in candidate_chapter_list:
            self.logger.info('chapter_url: {0}, feature_point: {1}, nosiy_point: {2}'.format(
                chapter.chapter_url,
                sum(chapter.feature_list),
                chapter.nosiy_point
            ))
        return candidate_chapter_list


    def candidate_chapter_rank(self, candidate_chapter_list):
        """
            从最大簇中挑选一个最优的候选章节

            首先过滤最大簇中字数特别少的，以及段落数特别少和特别多的，
            然后按照中文字符率排序，挑选最优的
        """
        candidate_chapter_list = self.basic_chapter_filter(candidate_chapter_list)

        selected_chapter = candidate_chapter_list[0]
        selected_chapter.chinese_rate = 1.0 * selected_chapter.valid_cn_sum / selected_chapter.valid_word_sum
        selected_index = 0
        for index in range(1, len(candidate_chapter_list)):
            chapter = candidate_chapter_list[index]
            chapter.chinese_rate = 1.0 * chapter.valid_cn_sum / chapter.valid_word_sum
            if chapter.chinese_rate > selected_chapter.chinese_rate \
                    or chapter.valid_cn_sum > selected_chapter.valid_cn_sum + 20:
                selected_chapter = chapter
                selected_index = index

        self.logger.info('chapter_title: {0}, chapter_url: {1}, chapter_length: {2}/{3}'.format(
            selected_chapter.chapter_title,
            selected_chapter.chapter_url,
            selected_chapter.valid_cn_sum,
            selected_chapter.valid_word_sum
        ))
        return selected_index, candidate_chapter_list


    def selected_chapter_content_filter(self, selected_chapter_index, candidate_chapter_list):
        """
        去除挑选的最优正文中的杂质

        根据统计selected_chapter和最大簇中其它候选中的句子，对于只出现在selected_chapter中的句子，认为可能是杂质。
        然后通过对齐句子的上下文和分类模型，进一步确认是否为杂质。

        段落对齐和句子对齐的数据结构是，每个候选对应一个列表，list(selected_index)存储的是最优正文中第selected_index个段落或者句子
        在其他候选正文中对应的段落和句子的index
        :return: 去杂之后的最优章节
        """
        self.logger.info('start selected content filter number of candidate: {0} selected_index:{1}'.
                         format(len(candidate_chapter_list), selected_chapter_index))

        selected_chapter = candidate_chapter_list[selected_chapter_index]
        if len(candidate_chapter_list) < 3:
            return selected_chapter

        chapter_content_filter = ChapterContentFilter()

        # 先做段落的对齐，返回段落对齐的词典
        para_align_dict = chapter_content_filter.align_paras(selected_chapter_index, candidate_chapter_list)

        # freq小于para_freq_threshold的需要做句子的对齐
        para_freq_threshold = 3
        if len(candidate_chapter_list) < 6:
            para_freq_threshold = 2

        # 检测有多少个没有对齐的段落
        para_freq_count = {}  # 不同freq对应的段落数
        need_align_para_index = []  # 需要做句子对齐的段落索引
        for selected_para in selected_chapter.paragraph_list:
            para_freq_count[selected_para.freq] = para_freq_count.get(selected_para.freq, 0) + 1

            # 如果外包发现其实显示对齐的段落也包含杂质，那么可以调高需要做句子对齐的freq
            if selected_para.freq < para_freq_threshold:
                need_align_para_index.append(selected_para.para_index)

        self.logger.info('paragraph not align count:{0}/{1}({2}) freq_dict:{3} align_dict:{4} not_align_index:{5}'.
                         format(para_freq_count.get(1, 0), len(selected_chapter.paragraph_list),
                                1.0 * para_freq_count.get(1, 0) / len(selected_chapter.paragraph_list),
                                para_freq_count, para_align_dict, need_align_para_index))

        #如果总段落数大于9，未对齐的段落数超过1/3，认为其它候选资源可能分段有问题，通过对齐去杂的成本太高
        #测试阶段统计这样的case有多少个
        # not_align_para_count = para_freq_count.get(1, 0)
        # if len(selected_chapter.paragraph_list) > 9 and not_align_para_count > len(selected_chapter.paragraph_list) / 2:
        #     self.logger.info('paragraph not align over 1/3, no action has been taken')
        #     return selected_chapter

        #对于freq小于para_freq_threshold的段落，进行句子的对齐
        for selected_para_index in xrange(0, len(selected_chapter.paragraph_list)):
            selected_para = selected_chapter.paragraph_list[selected_para_index]
            # need_remove为True表示为整段杂质，there_remove为true表示段中包含杂质，并且已经被处理
            if selected_para.need_remove or selected_para.there_remove:
                continue

            if selected_para.freq < para_freq_threshold:
                selected_para.there_remove = True

                #检查段落是整段都是杂质，还是一部分为杂质，如果一部分为杂质，返回可能需要进行对齐去杂的句子和起始段落的索引
                need_align_sentences, para_start_index, para_end_index = chapter_content_filter.check_para(
                    selected_para_index, selected_chapter_index, para_align_dict, candidate_chapter_list)

                self.logger.info('para_index:{0} need handle para_index:{1}-{2} align_candidate:{3}'.
                                 format(selected_para_index, para_start_index, para_end_index, len(need_align_sentences))
                )

                #更新para_start_index和para_end_index之间所有章节的there_remove和freq，标记它们已被处理，避免同一段被多次处理
                for para_index in xrange(para_start_index, para_end_index):
                    selected_chapter.paragraph_list[para_index].there_remove = True
                    selected_chapter.paragraph_list[para_index].freq = len(need_align_sentences)

                if len(need_align_sentences) == 0:
                    self.logger.info('whole paragraph impurity')
                    for para_index in xrange(para_start_index, para_end_index):
                        selected_chapter.paragraph_list[para_index].need_remove = True
                else:
                    #对未对齐段落对应的句子，进行句子对齐
                    sentence_align_dict = chapter_content_filter.align_sentences(selected_chapter_index,
                                                                                 need_align_sentences
                    )

                    selected_sentence_list = need_align_sentences[selected_chapter_index]

                    # freq小于sentence_freq_threshold的句子需要检测是否为杂质
                    sentence_freq_threshold = 3
                    if len(need_align_sentences) < 6:  # 如果只偶遇6个以下的候选用来做句子对齐，只检测freq为1的句子
                        sentence_freq_threshold = 2

                    sentence_freq_count = {}
                    need_check_sentence_index = []
                    for sentence_index, selected_sentence in enumerate(selected_sentence_list):
                        sentence_freq_count[selected_sentence.freq] = \
                            sentence_freq_count.get(selected_sentence.freq, 0) + 1
                        if selected_sentence.freq < sentence_freq_threshold:
                            need_check_sentence_index.append(sentence_index)

                    self.logger.info(
                        'para_index:{0}-{1} sentence not align count:{2}/{3} freq_dict:{4} align_dict:{5} not_check_index:{6}'.format(
                            para_start_index, para_end_index, sentence_freq_count.get(1, 0),
                            len(selected_sentence_list), sentence_freq_count, sentence_align_dict, need_check_sentence_index
                        ))
                    #根据句子对齐的结果，进一步判断句子是否是整句杂质，还是句子的一部分是杂质
                    for selected_sentence_index in xrange(0, len(selected_sentence_list)):
                        selected_sentence = selected_sentence_list[selected_sentence_index]
                        if selected_sentence.need_remove or selected_sentence.there_remove:
                            continue

                        if selected_sentence.freq < sentence_freq_threshold:
                            selected_sentence.there_remove = True

                            #检查句子是整句都是杂质，还是一部分为杂质，如果一部分为杂质，返回可能需要进一步去杂的句子
                            need_check_sentences, sentence_start_index, sentence_end_index = chapter_content_filter. \
                                check_sentence(selected_sentence_index, selected_chapter_index,
                                               sentence_align_dict, need_align_sentences, sentence_freq_threshold)
                            self.logger.info('sen_index:{0} need handle sen_index:{1}-{2}'.
                                             format(selected_sentence_index, sentence_start_index, sentence_end_index))

                            between_sentence_content = u''
                            for sentence_index in xrange(sentence_start_index, sentence_end_index):
                                selected_sentence_list[sentence_index].there_remove = True
                                selected_sentence_list[sentence_index].freq = len(need_check_sentences)
                                between_sentence_content += selected_sentence_list[sentence_index].fmt_content

                            selected_chapter.there_impurity = True
                            if len(need_check_sentences) == 0:
                                for sentence_index in xrange(sentence_start_index, sentence_end_index):
                                    selected_sentence_list[sentence_index].need_remove = True

                                self.logger.info('whole sentence impurity')

                                #将整句杂质输出，用于补充分类器的负例
                                #连续几个杂质句作为一个整体。
                                #杂质句，site_id，分类器判断是否是杂质，分类器输出的概率
                                with codecs.open('data/whole_sen.csv', 'a', encoding='gbk',
                                                 errors='ignore') as whole_impurity_file:
                                    prob = chapter_content_filter.classifier.classify(between_sentence_content)
                                    whole_impurity_file.write(
                                        between_sentence_content + ',' + str(selected_chapter.site_id) + ','
                                        + str(prob > 0.5 and 1 or 0) + ',' + str(prob) + '\n')
                            else:
                                #表明当前这些句子在其它候选都有对应的句子存在
                                self.logger.info('part is impurity')

                                chapter_content_filter.remove_part_impurity(need_check_sentences)
                                with codecs.open('data/impurity', 'a', encoding='gbk', errors='ignore') as impurity_file:
                                    for sentence_list in need_check_sentences.values():
                                        impurity_file.write(u'[' + str(len(sentence_list)) + u']' + u''.join([s.fmt_content + s.after_punctuation for s in sentence_list]) + u'=')
                                    impurity_file.write('\n')
                                pass

                                with codecs.open('data/part_sen.csv', 'a', encoding='gbk',
                                                 errors='ignore') as part_impurity_file:
                                    prob = chapter_content_filter.classifier.classify(between_sentence_content)
                                    part_impurity_file.write(
                                        between_sentence_content + ',' + str(prob > 0.5 and 1 or 0) + ',' + str(prob) + '\n')

                    #将去杂之后的句子转换会段落正文，放入对应段落的fmt_content中
                    chapter_content_filter.sentence_to_paragraph(selected_chapter.paragraph_list, para_start_index,
                                                                 para_end_index, selected_sentence_list)

        selected_chapter.pure_chapter_content = chapter_content_filter.back_to_html(selected_chapter.paragraph_list,
                                                                                    selected_chapter.site_id)
        return selected_chapter

    def selected_chapter_update(self, current_chapter_status, chapter_url, chapter):
        """
        """
        if debug:
            print('rid: {0}'.format(chapter.rid))
            print('chapter_title: {0}, chapter_url: {1}'.format(chapter.chapter_title, chapter.chapter_url))
            print(chapter.chapter_content.encode('GBK', 'ignore'))
            return

        for block in chapter.chapter_page['blocks']:
            if 'type' in block and block['type'] == 'NOVELCONTENT':
                block['data_value'] = chapter.fmt_chapter_content

        flag = True
        silk_server = SilkServer()
        flag = silk_server.save('{0}|{1}'.format(chapter.rid, chapter.align_id), chapter.chapter_page)

        if flag is True:
            chapter_db = ChapterDBModule()
            chapter.chapter_url = "'{0}'".format(url_format(chapter.chapter_url))
            chapter_db.update_novelaggregationdir_info(current_chapter_status, chapter)


    def novel_chapter_optimize(self, rid):
        """
            一本小说章节选取入口
        """
        chapter_db = ChapterDBModule()
        aggregate_dir_list = chapter_db.get_novelaggregationdir_list(rid)
        for (align_id, chapter_index, chapter_url, chapter_status, optimize_chapter_status, optimize_chapter_wordsum) in aggregate_dir_list:
            if chapter_status == 210:
                continue
            if optimize_chapter_status >= 10 and optimize_chapter_wordsum >= 100:
                continue
            self.logger.info('rid: {0}, index: {1}/{2}, align_id: {3}, chapter_status: {4}'.format(
                rid, chapter_index, len(aggregate_dir_list), align_id, chapter_status))

            total_candidate_chapter_list = self.candidate_chapter_collecion(rid, align_id)
            current_chapter_status = len(total_candidate_chapter_list)
            self.logger.info('total_candidate_chapter_length: {0}'.format(len(total_candidate_chapter_list)))
            if optimize_chapter_status >= current_chapter_status:
                continue

            candidate_chapter_list = self.candidate_chapter_generate(rid, align_id, total_candidate_chapter_list)
            if len(candidate_chapter_list) == 0:
                continue
            candidate_chapter_list = self.candidate_chapter_filter(candidate_chapter_list)
            selected_index, candidate_chapter_list = self.candidate_chapter_rank(candidate_chapter_list)
            selected_chapter = self.selected_chapter_content_filter(selected_index, candidate_chapter_list)
            self.selected_chapter_update(current_chapter_status, selected_chapter.chapter_url, selected_chapter)


    def run_test(self):
        """
        """
        rid_list = []
        for line in open('./data/rid.txt', 'r').readlines():
            rid = int(line.strip())
            rid_list.append(rid)

        for index, rid in enumerate(rid_list):
            if index < self.start_rid_id or index > self.end_rid_id:
                continue
            self.novel_chapter_optimize(rid)
        self.logger.info('chapter module end !')


    def run(self):
        """
        """
        chapter_db = ChapterDBModule()

        rid_list = []
        for table_id in xrange(self.start_rid_id, self.end_rid_id + 1):
            result = chapter_db.get_novelaggregationdir_rid(table_id)
            rid_list.extend(result)

        random.shuffle(rid_list)
        for index, rid in enumerate(rid_list):
            self.logger.info('chapter module rid: {0}/{1}'.format(index, len(rid_list)))
            self.novel_chapter_optimize(rid)
        self.logger.info('chapter module end !')


if __name__ == '__main__':
    here()    







