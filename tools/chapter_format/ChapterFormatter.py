#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'hewei13'
__date__ = '2014-05-26 17:16'

from basic.SilkServerModule import *
from novel.chapter.ChapterDB import *
from novel.chapter.ChapterHtmlFilter import *
from time import time
import os
import codecs
import random
import logging
import re

cur_linesep = os.linesep
cur_delimiter = str(chr(1))  # 存储文件的分隔符
my_html_filter = ChapterHtmlFilter()
logger = logging.getLogger('novel.chapter')

def chapter_format_cid(cid):
    #start = time()

    #从pageDB根据章节的cid读取其章节内容
    silk_server = SilkServer()
    chapter_page = silk_server.get(src='http://test.com', pageid=cid)
    if not chapter_page or 'novel_chapter_type' not in chapter_page or chapter_page['novel_chapter_type'] != 0 \
            or 'blocks' not in chapter_page:
        logger.info('cid:{0} not exists in pageDB'.format(cid))
        return

    fmt_chapter_page = my_html_filter.run(chapter_page, cid)
    if not silk_server.save(cid, fmt_chapter_page):
        logger.error('cid:{0} failed to save to pageDB'.format(cid))
    else:
        logger.info('cid:{0} OK'.format(cid))

    # chapter_title = None
    # for block in chapter_page['blocks']:
    #     if 'type' in block and block['type'] == 'NOVELCONTENT':
    #         raw_chapter_content = block['data_value']
    #         format_chapter_content = my_html_filter.chapter_html_filter(raw_chapter_content)
    #
    #         #格式化章节内容后，写回pageDB
    #         block['data_value'] = format_chapter_content
    #         if not silk_server.save(cid, chapter_page):
    #             my_html_filter.logger.error('cid:{0} failed to save to pageDB'.format(cid))
    #
    #         #处理完章节正文即可退出
    #         break
    #     if 'type' in block and block['type'] == 'TITLE':
    #         chapter_title = block['data_value']
    #
    # end = time()
    # with open('time_sum', 'a+') as time_f:
    #     time_f.write(str(end - start) + '\t' + str(len(raw_chapter_content)) + cur_linesep)
    #
    # if chapter_title is None:
    #     chapter_title = chapter_page['page_title'].strip()
    # return cid, chapter_title, raw_chapter_content, format_chapter_content


def chapter_format_rid(rid, cid_sample_num=-1):
    """
    格式化一个rid对应的权威目录所有的章节
    """
    rid = int(rid)
    #根据rid获取权威目录
    chapter_db = ChapterDBModule()
    aggregate_dir_list = chapter_db.get_novelaggregationdir_list(rid)
    if len(aggregate_dir_list) == 0:
        return False
    logger.info('chapter number: {0}'.format(len(aggregate_dir_list)))

    #对cid进行抽样，取后20章，并在前面章节随机选取30章
    sample_dirs = []
    if cid_sample_num == -1:
        sample_dirs = aggregate_dir_list
    else:
        dir_sum = len(aggregate_dir_list)

        if dir_sum <= 20:
            sample_dirs = aggregate_dir_list
        else:
            sample_dirs.extend(aggregate_dir_list[dir_sum - 20:dir_sum])
            left_num = min(cid_sample_num - 20, dir_sum - 20)
            sample_dirs.extend(random.sample(aggregate_dir_list[0: dir_sum - 20], left_num))

    #格式化权威目录的每一个章节
    #count = 1
    for (align_id, chapter_index, chapter_url, chapter_status) in sample_dirs:
        #print count
        #count += 1

        cid = u'{0}|{1}'.format(rid, align_id)
        chapter_format_cid(cid)

        # fmt_result = chapter_format_cid(cid)  # (cid, chapter_title, raw_chapter_content, format_chapter_content)
        #
        # #章节正文为空，表明其当前未固化
        # if fmt_result[2] == '':
        #     continue
        #
        # result_tuple = [u'' + str(rid)]
        # result_tuple.extend(fmt_result)
        #
        # #计算前后中文字符个数
        # raw_cn_count = count_chinese(fmt_result[2])
        # fmt_cn_count = count_chinese(fmt_result[3])
        # diff_cn_count = u'' + str(fmt_cn_count - raw_cn_count)
        # result_tuple.append(diff_cn_count)
        #
        # #如果前后中文字符不相等，保存
        # if diff_cn_count != u'0':
        #     diff_chinese(cid, fmt_result[2], fmt_result[3])
        #
        # result_tuple.append(u'' + str(chapter_index))
        # #(rid, cid, chapter_title, raw_chapter_content, format_chapter_content, diff_cn_count, chapter_sort)
        # with codecs.open('result.txt', 'a+', encoding='gbk', errors='ignore') as result_file:
        #     result_file.write(cur_delimiter.join(result_tuple) + cur_linesep)

    return True


def chapter_format_run():
    """
    """
    parser = SafeConfigParser()
    parser.read('./conf/NovelChapterModule.conf')
    start_rid_id = parser.getint('chapter_module', 'proc_start_rid_id')
    end_rid_id = parser.getint('chapter_module', 'proc_end_rid_id')


    chapter_db = ChapterDBModule()

    rid_list = []
    for table_id in xrange(start_rid_id, end_rid_id + 1):
        result = chapter_db.get_novelaggregationdir_rid(table_id)
        rid_list.extend(result)

    random.shuffle(rid_list)
    for index, rid in enumerate(rid_list):
        logger.info('index: {0}/{1}, rid: {2}'.format(index, len(rid_list), rid))
        chapter_format_rid(rid)


def log_handle():
    """

    """
    #从日志中提取logger.info('cid:{0} failed to save to pageDB'.format(cid))的cid
    os.system("cat ../[0-9]*/log/novel.log | grep 'failed to save to pageDB' > redo.log")

    #2014-06-10 20:11:51,801 - novel.chapter - INFO - cid:2108321536|2003455025290766541 failed to save to pageDB
    redo_pattern = re.compile(r'cid:(\S+)')

    redo_cid_file = open('redo.cid', 'w')
    with open('redo.log') as redo_file:
        for line in redo_file:
            cid = redo_pattern.search(line).group(1)
            redo_cid_file.write(cid + cur_linesep)

    #从日志中提取self.logger.info('cid: {0}, raw_count: {1}, fmt_count: {2}'.format(cid, raw_zh_count, fmt_zh_count))
    #cid raw_count fmt_count
    os.system("cat ../[0-9]*/log/novel.log | grep 'raw_count' > zh.log")

    #2014-06-10 19:39:27,756 - novel.chapter.html - INFO - cid: 1272655104|3587686572048187349, raw_count: 386, fmt_count: 379
    zh_pattern = re.compile(r'cid: (\S+), raw_count: (\S+), fmt_count: (\S+)')

    zh_cid_file = open('zh.cid', 'w')
    half_zh_cid_file = open('half_zh.cid', 'w')
    with open('zh.log') as zh_file:
        for line in zh_file:
            match = zh_pattern.search(line)
            cid = match.group(1)
            raw_count = match.group(2)
            fmt_count = match.group(3)
            if int(raw_count) - int(fmt_count) > int(raw_count) / 2:
                half_zh_cid_file.write(cid + '\t' + raw_count + '\t' + fmt_count + cur_linesep)
            else:
                zh_cid_file.write(cid + '\t' + raw_count + '\t' + fmt_count + cur_linesep)

    os.system("rm *.log")

    # 2014-6-12 19:18

if __name__ == "__main__":
    pass
