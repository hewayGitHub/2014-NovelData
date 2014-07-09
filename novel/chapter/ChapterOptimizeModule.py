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
            ��ȡһ���½ڵ�������Ϣ

            �޸�Ϊ���������������20�����˵�
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

        # ���ض����б�
        chapter_content_filter = ChapterContentFilter()
        chapter.fmt_chapter_content, chapter.paragraph_list, chapter.valid_para_count \
            = chapter_content_filter.get_paras(raw_chapter_content, chapter.site_id, chapter.chapter_title)

        if len(chapter.fmt_chapter_content) == 0 or len(chapter.paragraph_list) == 0:  # ��Щ����£�raw_chapter_content��ֻ��html��ǩ��Ϊ���ݣ�ͨ��html����֮���ı��ǿ�
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
            ��ȡһ���½ڵ����к�ѡ�½ڵĻ�����Ϣ
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
            ����rid��align_id��ȡ��ѡ�½�

            һ��վ��ֻѡȡһ����ѡ�������ѡȡ����15����ѡ������������վ��Դ���������
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
           Ϊ�˷���������;��ӵĶ��룬�������������Ͷ������������صĺ�ѡ�½�

           ���������������ر��ٵģ�С��ƽ����80%�����Լ��������ر��ٺ��ر���
           ͬʱ��֤�����ѡ�½���������5�����صĺ�ѡ�½���������3����ѡ
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
            ��ѡ�½ڹ���
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
            ����������ѡһ�����ŵĺ�ѡ�½�

            ���ȹ��������������ر��ٵģ��Լ��������ر��ٺ��ر��ģ�
            Ȼ���������ַ���������ѡ���ŵ�
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
        ȥ����ѡ�����������е�����

        ����ͳ��selected_chapter��������������ѡ�еľ��ӣ�����ֻ������selected_chapter�еľ��ӣ���Ϊ���������ʡ�
        Ȼ��ͨ��������ӵ������ĺͷ���ģ�ͣ���һ��ȷ���Ƿ�Ϊ���ʡ�

        �������;��Ӷ�������ݽṹ�ǣ�ÿ����ѡ��Ӧһ���б�list(selected_index)�洢�������������е�selected_index��������߾���
        ��������ѡ�����ж�Ӧ�Ķ���;��ӵ�index
        :return: ȥ��֮��������½�
        """
        self.logger.info('start selected content filter number of candidate: {0} selected_index:{1}'.
                         format(len(candidate_chapter_list), selected_chapter_index))

        selected_chapter = candidate_chapter_list[selected_chapter_index]
        if len(candidate_chapter_list) < 3:
            return selected_chapter

        chapter_content_filter = ChapterContentFilter()

        # ��������Ķ��룬���ض������Ĵʵ�
        para_align_dict = chapter_content_filter.align_paras(selected_chapter_index, candidate_chapter_list)

        # freqС��para_freq_threshold����Ҫ�����ӵĶ���
        para_freq_threshold = 3
        if len(candidate_chapter_list) < 6:
            para_freq_threshold = 2

        # ����ж��ٸ�û�ж���Ķ���
        para_freq_count = {}  # ��ͬfreq��Ӧ�Ķ�����
        need_align_para_index = []  # ��Ҫ�����Ӷ���Ķ�������
        for selected_para in selected_chapter.paragraph_list:
            para_freq_count[selected_para.freq] = para_freq_count.get(selected_para.freq, 0) + 1

            # ������������ʵ��ʾ����Ķ���Ҳ�������ʣ���ô���Ե�����Ҫ�����Ӷ����freq
            if selected_para.freq < para_freq_threshold:
                need_align_para_index.append(selected_para.para_index)

        self.logger.info('paragraph not align count:{0}/{1}({2}) freq_dict:{3} align_dict:{4} not_align_index:{5}'.
                         format(para_freq_count.get(1, 0), len(selected_chapter.paragraph_list),
                                1.0 * para_freq_count.get(1, 0) / len(selected_chapter.paragraph_list),
                                para_freq_count, para_align_dict, need_align_para_index))

        #����ܶ���������9��δ����Ķ���������1/3����Ϊ������ѡ��Դ���ֶܷ������⣬ͨ������ȥ�ӵĳɱ�̫��
        #���Խ׶�ͳ��������case�ж��ٸ�
        # not_align_para_count = para_freq_count.get(1, 0)
        # if len(selected_chapter.paragraph_list) > 9 and not_align_para_count > len(selected_chapter.paragraph_list) / 2:
        #     self.logger.info('paragraph not align over 1/3, no action has been taken')
        #     return selected_chapter

        #����freqС��para_freq_threshold�Ķ��䣬���о��ӵĶ���
        for selected_para_index in xrange(0, len(selected_chapter.paragraph_list)):
            selected_para = selected_chapter.paragraph_list[selected_para_index]
            # need_removeΪTrue��ʾΪ�������ʣ�there_removeΪtrue��ʾ���а������ʣ������Ѿ�������
            if selected_para.need_remove or selected_para.there_remove:
                continue

            if selected_para.freq < para_freq_threshold:
                selected_para.there_remove = True

                #�����������ζ������ʣ�����һ����Ϊ���ʣ����һ����Ϊ���ʣ����ؿ�����Ҫ���ж���ȥ�ӵľ��Ӻ���ʼ���������
                need_align_sentences, para_start_index, para_end_index = chapter_content_filter.check_para(
                    selected_para_index, selected_chapter_index, para_align_dict, candidate_chapter_list)

                self.logger.info('para_index:{0} need handle para_index:{1}-{2} align_candidate:{3}'.
                                 format(selected_para_index, para_start_index, para_end_index, len(need_align_sentences))
                )

                #����para_start_index��para_end_index֮�������½ڵ�there_remove��freq����������ѱ���������ͬһ�α���δ���
                for para_index in xrange(para_start_index, para_end_index):
                    selected_chapter.paragraph_list[para_index].there_remove = True
                    selected_chapter.paragraph_list[para_index].freq = len(need_align_sentences)

                if len(need_align_sentences) == 0:
                    self.logger.info('whole paragraph impurity')
                    for para_index in xrange(para_start_index, para_end_index):
                        selected_chapter.paragraph_list[para_index].need_remove = True
                else:
                    #��δ��������Ӧ�ľ��ӣ����о��Ӷ���
                    sentence_align_dict = chapter_content_filter.align_sentences(selected_chapter_index,
                                                                                 need_align_sentences
                    )

                    selected_sentence_list = need_align_sentences[selected_chapter_index]

                    # freqС��sentence_freq_threshold�ľ�����Ҫ����Ƿ�Ϊ����
                    sentence_freq_threshold = 3
                    if len(need_align_sentences) < 6:  # ���ֻż��6�����µĺ�ѡ���������Ӷ��룬ֻ���freqΪ1�ľ���
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
                    #���ݾ��Ӷ���Ľ������һ���жϾ����Ƿ����������ʣ����Ǿ��ӵ�һ����������
                    for selected_sentence_index in xrange(0, len(selected_sentence_list)):
                        selected_sentence = selected_sentence_list[selected_sentence_index]
                        if selected_sentence.need_remove or selected_sentence.there_remove:
                            continue

                        if selected_sentence.freq < sentence_freq_threshold:
                            selected_sentence.there_remove = True

                            #�����������䶼�����ʣ�����һ����Ϊ���ʣ����һ����Ϊ���ʣ����ؿ�����Ҫ��һ��ȥ�ӵľ���
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

                                #������������������ڲ���������ĸ���
                                #�����������ʾ���Ϊһ�����塣
                                #���ʾ䣬site_id���������ж��Ƿ������ʣ�����������ĸ���
                                with codecs.open('data/whole_sen.csv', 'a', encoding='gbk',
                                                 errors='ignore') as whole_impurity_file:
                                    prob = chapter_content_filter.classifier.classify(between_sentence_content)
                                    whole_impurity_file.write(
                                        between_sentence_content + ',' + str(selected_chapter.site_id) + ','
                                        + str(prob > 0.5 and 1 or 0) + ',' + str(prob) + '\n')
                            else:
                                #������ǰ��Щ������������ѡ���ж�Ӧ�ľ��Ӵ���
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

                    #��ȥ��֮��ľ���ת����������ģ������Ӧ�����fmt_content��
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
            һ��С˵�½�ѡȡ���
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







