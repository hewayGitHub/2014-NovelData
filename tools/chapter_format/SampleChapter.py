#!/usr/bin/env python
# -*- coding:GBK -*-

__author__ = 'hewei13'
__date__ = '2014-6-17 9:37'

from basic.NovelStructure import Singleton
from novel.chapter.ChapterDB import ChapterDBModule
from novel.chapter.ChapterOptimizeModule import ChapterOptimizeModule
from random import sample, shuffle, randint
import logging
import codecs
import os
import re
from ConfigParser import SafeConfigParser

cur_linesep = os.linesep
cur_delimiter = str(chr(1))  # �洢�ļ��ķָ���


def init_log(name, debug=True):
    """
    ��ʼ��log�������debugģʽ��ֱ��������ն�
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if debug:
        fh = logging.StreamHandler()
    else:
        fh = logging.FileHandler('./log/{0}.log'.format(name))

    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.info('{0} log init successful!'.format(name))

    return logger


class SampleChapter(object):
    """

    """
    __metaclass__ = Singleton

    def __init__(self, debug=True):
        self.debug = debug
        self.logger = init_log('novel.chapter', debug)
        self.err = init_log('err.chapter', debug)

    @staticmethod
    def sample_list(data_list, sample_num=-1, sep_num=0, head_num=0):
        """
        ��data_list���������sample_num������seq_index֮ǰѡȡhead_num������seq_index��ѡȡʣ��sample_num - head_num��

        :param data_list:
        :param sample_num: ����������-1��ʾ������
        :param sep_num: �Ӱ���seq_num�Լ�֮ǰ��ȡhead_num����0��ʾ�������sample_num��
        :param head_num: �Ӱ���seq_num�Լ�֮ǰ��ȡhead_num����0��ʾ�������sample_num��
        :return:�������sample_data list
        """
        sample_data = []
        if sample_num == -1:
            sample_data = data_list
        else:
            data_len = len(data_list)

            if data_len <= sample_num:
                sample_data = data_list
            else:
                head_num = min(head_num, sep_num, sample_num)
                sep_num = min(sep_num, data_len)
                if sep_num + sample_num - head_num >= data_len or sep_num <= 0 or head_num <= 0:
                    sample_data.extend(sample(data_list, sample_num))
                else:
                    sample_data.extend(sample(data_list[:sep_num], head_num))
                    sample_data.extend(sample(data_list[sep_num:], sample_num - head_num))

        shuffle(sample_data)
        return sample_data

    def sample_chapter_rid(self, rid):
        """
        ��һ�����������ѡ20���½ڣ�����֮ǰ�½�ѡȡ��˼·��������ѡ�½�д���Ӧ��վ��������ļ���
        :return:
        """
        rid = int(rid)

        # ���rid��Ӧ��Ȩ��Ŀ¼��Ȼ����������ѡ10���½�
        chapter_db = ChapterDBModule()
        agg_dir_list = chapter_db.get_novelaggregationdir_list(rid)

        #�����100�»������20%������ѡ
        sample_seq_num = min(len(agg_dir_list) - 100, len(agg_dir_list) * 4/5)
        sample_agg_dir_list = SampleChapter.sample_list(agg_dir_list, sample_num=20,
                                                        sep_num=sample_seq_num, head_num=10
        )

        chapter_module = ChapterOptimizeModule()
        for (align_id, chapter_index, chapter_url, chapter_status) in sample_agg_dir_list:
            self.logger.info('rid: {0}, sample_index: {1}/{2}, align_id: {3}, chapter_status: {4}'.format(
                rid, chapter_index, len(sample_agg_dir_list), align_id, chapter_status))

            total_candidate_chapter_list = chapter_module.candidate_chapter_collecion(rid, align_id)
            self.logger.info('total_candidate_chapter_length: {0}'.format(len(total_candidate_chapter_list)))

            candidate_chapter_list = chapter_module.candidate_chapter_generate(rid, align_id, total_candidate_chapter_list)
            if len(candidate_chapter_list) == 0:
                continue

            if len(candidate_chapter_list) >= 3:
                candidate_chapter_list = chapter_module.basic_chapter_filter(candidate_chapter_list)

            self.logger.info('selected_candidate_chapter_length: {0}'.format(len(candidate_chapter_list)))

            with codecs.open('data/sample_cid', 'a', encoding='gbk') as sample_cid_file:
                sample_cid_file.write(str(rid) + cur_delimiter + str(align_id) + cur_linesep)

            for candidate_chapter in candidate_chapter_list:
                with codecs.open('data/sample/' + str(candidate_chapter.site_id), 'a',
                                 encoding='gbk', errors='ignore') as sample_file:
                    sample_file.write(str(candidate_chapter.rid) + cur_delimiter
                                      + str(candidate_chapter.align_id) + cur_delimiter
                                      + str(candidate_chapter.chapter_id) + cur_delimiter
                                      + str(candidate_chapter.site_id) + cur_delimiter
                                      + str(candidate_chapter.site_status) + cur_delimiter
                                      + candidate_chapter.chapter_content + cur_linesep)

    def sample_chapter_cid(self, rid, align_id):
        rid = int(rid)

        chapter_module = ChapterOptimizeModule()
        total_candidate_chapter_list = chapter_module.candidate_chapter_collecion(rid, align_id)
        self.logger.info('rid: {0} align_id: {1} total_candidate_chapter_length: {2}'.format(
            rid, align_id, len(total_candidate_chapter_list)))

        candidate_chapter_list = chapter_module.candidate_chapter_generate(rid, align_id, total_candidate_chapter_list)
        if len(candidate_chapter_list) == 0:
            return

        if len(candidate_chapter_list) >= 3:
            candidate_chapter_list = chapter_module.basic_chapter_filter(candidate_chapter_list)

        self.logger.info('rid: {0} align_id: {1} selected_candidate_chapter_length: {2}'.format(
            rid, align_id, len(candidate_chapter_list)))

        for candidate_chapter in candidate_chapter_list:
            with codecs.open('data/sample/' + str(candidate_chapter.site_id), 'a',
                             encoding='gbk', errors='ignore') as sample_file:
                sample_file.write(str(candidate_chapter.rid) + cur_delimiter
                                  + str(candidate_chapter.align_id) + cur_delimiter
                                  + str(candidate_chapter.chapter_id) + cur_delimiter
                                  + str(candidate_chapter.site_id) + cur_delimiter
                                  + str(candidate_chapter.site_status) + cur_delimiter
                                  + candidate_chapter.chapter_content + cur_linesep)

    def sample_cid(self):
        """
        ��top 10W�������ȡ1000���飬��һ�����������ѡ20���½ڡ�
        :return:
        """
        if not os.path.isdir('data/sample/'):
            os.makedirs('data/sample/')

        #��ȡtop 10W���id
        rid_list = []
        with codecs.open('../rid.txt.100k') as top_100k_file:
            for line in top_100k_file:
                rid = line.strip()
                if rid != '':
                    rid_list.append(line.strip())

        if self.debug:
            sample_book_num = 1
        else:
            sample_book_num = 2000

        #��top 10W�������ȡ1000���飬ǰ1Wѡȡ100����9Wѡȡ900
        sample_rid_list = SampleChapter.sample_list(rid_list, sample_num=sample_book_num, sep_num=10000, head_num=100)

        sample_size = 1000
        sample_count = 0
        for rid in sample_rid_list:
            rid = int(rid)

            # ���rid��Ӧ��Ȩ��Ŀ¼��Ȼ����������ѡ20���½�
            chapter_db = ChapterDBModule()
            agg_dir_list = chapter_db.get_novelaggregationdir_list(rid)

            #�����100�»������20%������ѡ
            sample_seq_num = min(len(agg_dir_list) - 100, len(agg_dir_list) * 4/5)
            sample_agg_dir_list = SampleChapter.sample_list(agg_dir_list, sample_num=20,
                                                            sep_num=sample_seq_num, head_num=10
            )

            if len(sample_agg_dir_list) == 0:
                continue

            sample_count += 1
            if sample_count > sample_size:
                break

            self.logger.info('rid: {0}, sample_num/chapter_sum: {1}/{2}'.format(
                rid, len(sample_agg_dir_list), len(agg_dir_list)))

            with codecs.open('data/sample_cid', 'a', encoding='gbk') as sample_cid_file:
                for (align_id, chapter_index, chapter_url, chapter_status) in sample_agg_dir_list:
                    sample_cid_file.write(str(rid) + cur_delimiter + str(align_id) + cur_linesep)

    def run(self):
        """
        ��top 10W�������ȡ100���飬

        :return:
        """
        if not os.path.isdir('data/sample/'):
            os.makedirs('data/sample/')

        #��ȡtop 10W���id
        rid_list = []
        with codecs.open('../rid.txt.100k') as top_100k_file:
            for line in top_100k_file:
                rid = line.strip()
                if rid != '':
                    rid_list.append(line.strip())

        if self.debug:
            sample_book_num = 1
        else:
            sample_book_num = 200

        #��top 10W�������ȡ200���飬ǰ1Wѡȡ100����1Wѡȡ100
        sample_rid_list = SampleChapter.sample_list(rid_list, sample_num=sample_book_num, sep_num=10000, head_num=100)

        for rid in sample_rid_list:
            self.sample_chapter_rid(rid)


def extract_sample(debug=True):
    """
    ��
    :return:
    """
    logger = init_log('novel.chapter', debug)
    err = init_log('err.chapter', debug)

    if not os.path.isdir('data/select_sample/'):
        os.makedirs('data/select_sample/')

    #��ȡ������ѡȡ��cid
    cid_list = []
    with codecs.open('data/sample_cid', encoding='gbk') as cid_file:
        for record in cid_file:
            cid = record.strip()
            if cid != '':
                cid_list.append(cid)
    logger.info('sum no of sample cid:{0}'.format(len(cid_list)))

    #��1000*20���г�ѡ10�£�ѡȡ�����еĺ�ѡ�½�
    cid_size = 10
    shuffle(cid_list)
    sample_cid_list = sample(cid_list, cid_size)
    with codecs.open('data/sample_1', 'a', encoding='gbk') as select_sample_file:
        for cid in sample_cid_list:
            select_sample_file.write(cid + cur_linesep)

    #ÿ��վ�����ѡȡ15��
    sample_size = 15
    newline_pattern = re.compile(r'[\n\r]+')
    for site_id in os.listdir('../sample/'):
        chapter_num = os.popen('wc -l ../sample/' + site_id).read().split(' ')[0]
        chapter_num = int(chapter_num)
        logger.info('site:{0} chapter_num:{1}'.format(site_id, chapter_num))

        sample_count = 0
        sample_file = codecs.open('data/select_sample/' + site_id, 'a', encoding='gbk', errors='ignore')
        with codecs.open('../sample/' + site_id, encoding='gbk') as site_file:
            pre_line = '\n'
            while True:
                if pre_line == '':
                    break

                record = pre_line.strip()
                line = site_file.readline()
                while line != '' and line.find(cur_delimiter) < 0:
                    record += line.strip()
                    line = site_file.readline()
                pre_line = line

                first_del = record.find(cur_delimiter)
                if first_del > 0:
                    second_del = record.find(cur_delimiter, first_del + 1)
                    cid = record[:second_del]

                    if cid in sample_cid_list:
                        logger.info('site:{0} cid:{1} all be selected'.format(site_id, cid))
                        record = newline_pattern.sub('', record)
                        record = record.replace('\t', ' ')
                        record = record.replace(cur_delimiter, '\t')
                        sample_file.write(record + cur_linesep)

                        sample_count += 1
                    else:
                        if sample_count < sample_size and randint(1, chapter_num) <= 3 * sample_size:
                            logger.info('site:{0} cid:{1} candidate be selected'.format(site_id, cid))
                            record = newline_pattern.sub('', record)
                            record = record.replace('\t', ' ')
                            record = record.replace(cur_delimiter, '\t')
                            sample_file.write(record + cur_linesep)

                            with codecs.open('data/sample_1', 'a', encoding='gbk') as select_sample_file:
                                third_del = record.find(cur_delimiter, second_del + 1)
                                select_sample_file.write(record[:third_del] + cur_linesep)
                            sample_count += 1
                else:
                    pass

        sample_file.close()
        logger.info('site:{0} select_chapter_num:{1}'.format(site_id, sample_count))

        #debugģʽ�Դ���һ��վ��
        if debug:
            break


def sample_chapter_run():
    """
    """
    parser = SafeConfigParser()
    parser.read('./conf/NovelChapterModule.conf')
    start_id = parser.getint('chapter_module', 'proc_start_rid_id')
    end_id = parser.getint('chapter_module', 'proc_end_rid_id')

    count = 0
    sample_chapter_module = SampleChapter(debug=False)
    with codecs.open('data/sample_cid', encoding='gbk') as sample_cid_file:
        for line in sample_cid_file:
            rid, align_id = line.strip().split(cur_delimiter)
            if start_id <= count % 256 <= end_id:
                sample_chapter_module.sample_chapter_cid(rid, align_id)

            count += 1

if __name__ == '__main__':
    print 'tools.chapter_format.SampleChapter'
