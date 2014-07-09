#!/usr/bin/env python
# -*- coding:GBK -*-
from tools.chapter_format.SampleChapter import SampleChapter

__author__ = 'hewei13'
__date__ = '2014-05-26 17:16'

from tools.chapter_format.ChapterFormatter import *
from novel.chapter.ChapterHtmlFilter import *
from novel.chapter.ChapterContentFilter import *
from novel.chapter.ChapterOptimizeModule import *
import random
import logging
import os


def init_log(name):
    """
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # fh = logging.FileHandler('./log/{0}.log'.format(name))
    fh = logging.FileHandler('./log/recover.log')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.info('{0} log init successful!'.format(name))


# init_log('novel')
#init_log('err')
cur_linesep = os.linesep
cur_delimiter = str(chr(1))  # 存储文件的分隔符
#logger = logging.getLogger('novel.chapter')


def diff_chinese(cid, raw_chapter_content, format_chapter_content):
    """
    比较格式化前后正文中中文字符个数是否相等
    若不相等，将其存于根目录下format文件夹中
    """
    if not os.path.isdir('format'):
        os.mkdir('format')

    #检测字符为非中文
    not_chinese_pattern = re.compile(u'[^\u4e00-\u9fa5]')

    raw_chinese = not_chinese_pattern.sub('', raw_chapter_content)
    fmt_chinese = not_chinese_pattern.sub('', format_chapter_content)
    #print "中文字符数：", len(raw_chinese), len(fmt_chinese)
    if len(raw_chinese) != len(fmt_chinese):
        print "格式化前后章节正文中文字符数目不相等"
        with open('format/' + cid + '_raw', 'w') as raw_file:
            raw_file.write(raw_chinese.encode('gbk', 'ignore'))
        with open('format/' + cid + '_fmt', 'w') as fmt_file:
            fmt_file.write(fmt_chinese.encode('gbk', 'ignore'))
    else:
        pass


def test_chapter_format_cid(cid):
    #从pageDB根据章节的cid读取其章节内容
    silk_server = SilkServer()
    chapter_page = silk_server.get(src='http://test.com', pageid=cid)
    if not chapter_page or 'novel_chapter_type' not in chapter_page or chapter_page['novel_chapter_type'] != 0 \
            or 'blocks' not in chapter_page:
        logger.info('cid:{0} not exists in pageDB'.format(cid))
        return cid, '', '', ''

    chapter_title = None
    for block in chapter_page['blocks']:
        if 'type' in block and block['type'] == 'NOVELCONTENT':
            raw_chapter_content = block['data_value']
            format_chapter_content = my_html_filter.chapter_html_filter(raw_chapter_content)

            #处理完章节正文即可退出
            break
        elif 'type' in block and block['type'] == 'TITLE':
            chapter_title = block['data_value']

    if chapter_title is None:
        chapter_title = chapter_page['page_title'].strip()

    return cid, chapter_title, raw_chapter_content, format_chapter_content


def test_chapter_format_rid(rid, cid_sample_num=-1):
    """
    格式化一个rid对应的权威目录所有的章节
    """
    os.system('rm result.txt')

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
    count = 1
    for (align_id, chapter_index, chapter_url, chapter_status) in sample_dirs:
        print count
        count += 1

        cid = u'{0}|{1}'.format(rid, align_id)
        fmt_result = test_chapter_format_cid(cid)  # (cid, chapter_title, raw_chapter_content, format_chapter_content)

        #章节正文为空，表明其当前未固化
        if fmt_result[2] == '':
            continue

        result_tuple = [u'' + str(rid)]
        result_tuple.extend(fmt_result)

        #计算前后中文字符个数
        raw_cn_count = count_chinese(fmt_result[2])
        fmt_cn_count = count_chinese(fmt_result[3])
        diff_cn_count = u'' + str(fmt_cn_count - raw_cn_count)
        result_tuple.append(diff_cn_count)

        #如果前后中文字符不相等，保存
        if diff_cn_count != u'0':
            print '中文字符不相等'
            diff_chinese(cid, fmt_result[2], fmt_result[3])

        result_tuple.append(u'' + str(chapter_index))
        #(rid, cid, chapter_title, raw_chapter_content, format_chapter_content, diff_cn_count, chapter_sort)
        with codecs.open('result.txt', 'a', encoding='gbk', errors='ignore') as result_file:
            result_file.write(cur_delimiter.join(result_tuple) + cur_linesep)

    return True


def test_batch_cid(cids):
    os.system('rm result.txt')

    print 'num of cid:', len(cids)

    count = 1
    for cid in cids:
        print count
        count += 1
        fmt_result = test_chapter_format_cid(cid)  # (cid, chapter_title, raw_chapter_content, format_chapter_content)

        #章节正文为空，表明其当前未固化
        if fmt_result[2] == '':
            continue

        result_tuple = [cid.split('|')[0]]
        result_tuple.extend(fmt_result)

        #计算前后中文字符个数
        raw_cn_count = count_chinese(fmt_result[2])
        fmt_cn_count = count_chinese(fmt_result[3])
        diff_cn_count = u'' + str(fmt_cn_count - raw_cn_count)
        result_tuple.append(diff_cn_count)

        #如果前后中文字符不相等，保存
        if diff_cn_count != u'0':
            print '中文字符不相等'
            diff_chinese(cid, fmt_result[2], fmt_result[3])

        result_tuple.append(u'-1')
        #(rid, cid, chapter_title, raw_chapter_content, format_chapter_content, diff_cn_count, chapter_sort)
        with codecs.open('result.txt', 'a', encoding='gbk', errors='ignore') as result_file:
            result_file.write(cur_delimiter.join(result_tuple) + cur_linesep)


def test_batch_rid(rids, rid_sample_num=-1, cid_sample_num=-1):
    if rid_sample_num != -1:
        sample_rids = random.sample(rids, rid_sample_num)
    else:
        sample_rids = rids

    print 'num of rid:', len(sample_rids)
    for rid in sample_rids:
        test_chapter_format_rid(rid, cid_sample_num)


def restore_from_url(cids):
    """
    根据url从pageDB中读取对应的原始章节正文，比较格式化前后的
    """
    for cid in cids:
        #从pageDB根据章节的cid读取其章节内容
        silk_server = SilkServer()
        chapter_page = silk_server.get(src='http://test.com', pageid=cid)
        if not chapter_page or 'novel_chapter_type' not in chapter_page or chapter_page['novel_chapter_type'] != 0 \
                or 'blocks' not in chapter_page:
            logger.info('cid:{0} not exists in pageDB'.format(cid))
            continue

        url = chapter_page['url']

        chapter_page = silk_server.get(src=url)
        if not chapter_page or 'novel_chapter_type' not in chapter_page or chapter_page['novel_chapter_type'] != 0 \
                or 'blocks' not in chapter_page:
            logger.info('cid:{0} not exists in pageDB'.format(cid))
            continue

        fmt_chapter_page = my_html_filter.run(chapter_page, cid)
        if not silk_server.save(cid, fmt_chapter_page):
            logger.info('cid:{0} failed to save to pageDB'.format(cid))
        else:
            logger.info('cid:{0} OK'.format(cid))


def count_time():
    count = 0
    str_count = 0
    time_count = 0
    with open('time_sum') as time_f:
        for line in time_f:
            items = line.strip().split('\t')
            time_count += float(items[0])
            str_count += int(items[1])
            count += 1
    print 'chapter_num   char_num   sum_time   avg_chapter_time'
    print count, str_count, time_count, time_count / count


def test_reg():
    """
    构造测试用例，测试chapter_format中正则表达式是否正确
    """
    raw_chapter_content = u"&nbsp;before anything<div class='div_class'>" \
                          u"<p class='p_class'>&nbsp;&nbsp;  \u3000p1</p><pre></pre><br style='br_style'/>" \
                          u"after br" \
                          u"<p> <span>p2</span> <br/>p3</p>" \
                          u"<other style='other_style'>other</other>我们都是<第一章><1><>" \
                          u"<a>link_data</a>a_middle<a href>link_data2</a>" \
                          u"<script>link_data</script>a_middle<script href>link_data2</script>" \
                          u"<div style='display:none'> <p> <span> hidden </p><div></div> </div>" \
                          u"div end</div>"
    print raw_chapter_content.encode('gbk')
    print my_html_filter.chapter_html_filter(raw_chapter_content).encode('gbk')


def test_get_paras():
    chapter_content_filter = ChapterContentFilter()
    site_id = '1'
    chapter_title = ''
    with codecs.open('data/select_sample/' + site_id, encoding='gbk') as sample_file:
        for line in sample_file:
            raw_chapter_content = line.strip().split('\t')[5]
            para_list = chapter_content_filter.get_paras(raw_chapter_content, site_id, chapter_title)
            raw_cn_count = count_chinese(raw_chapter_content)
            fmt_cn_count = 0
            for para in para_list:
                fmt_cn_count += count_chinese(para.fmt_content)

            if raw_cn_count != fmt_cn_count:
                print 'not equal {0} vs {1}'.format(raw_cn_count, fmt_cn_count)

                last_index = line.rfind('\t')
                print line[:last_index].encode('gbk')

            sentences = chapter_content_filter.get_sentences(para_list)
            for para_index, para in enumerate(para_list):
                print para_index, para.fmt_content.encode('gbk')
                if para.para_index == -1:
                    continue

                for index in range(para.sentence_start_index, para.sentence_end_index):
                    print sentences[index].fmt_content.encode('gbk')
                    raw_input('next_sentences')


def run_chapter():
    #test_format_batch(rid_sample_num=5, cid_sample_num=-1)
    #test_url()
    #test_badcase()
    #count_time()
    # log_handle()

    #从日志中提取logger.info('cid:{0} failed to save to pageDB'.format(cid))的cid
    # with open('redo.cid') as redo_file:
    #     for line in redo_file:
    #         cid = line.strip()
    #         chapter_format_cid(cid)

    #分析前后差距超过1半的原因
    # cids = []
    # with open('half_zh.cid') as half_zh_file:
    #     for line in half_zh_file:
    #         cid = line.strip().split('\t')[0]
    #         cids.append(cid)
    #
    # test_batch_cid(cids)
    #restore_from_url(cids)
    with codecs.open('data/sample_cid', encoding='gbk') as cid_file:
        count = 0
        valid_count = 0
        for line in cid_file:
            items = line.strip().split(cur_delimiter)
            if len(items) == 2:
                rid = items[0]
                align_id = items[1]
                res_tuple = evaluate(rid, align_id)

                print count
                count += 1

                if not res_tuple:
                    continue
                else:
                    valid_count += 1
                store_chapter_content, raw_chapter_content, pure_chapter_content, site_id, candidate_chapter_num, \
                cluster_chapter_num, rank_chapter_num = res_tuple
                with codecs.open('data/result.txt', 'a', encoding='gbk', errors='ignore') as result_file:
                    result_file.write(str(rid) + cur_delimiter + str(align_id) + cur_delimiter + str(site_id)
                                          + cur_delimiter + str(candidate_chapter_num) + cur_delimiter + str(cluster_chapter_num)
                                          + cur_delimiter + str(rank_chapter_num)
                                          + cur_delimiter + pure_chapter_content + cur_delimiter + store_chapter_content
                                          + cur_delimiter + raw_chapter_content
                                          + cur_linesep)

            if valid_count > 5:
                break


def batch_chapter_run():
    """
    """
    parser = SafeConfigParser()
    parser.read('./conf/NovelChapterModule.conf')
    start_id = parser.getint('chapter_module', 'proc_start_rid_id')
    end_id = parser.getint('chapter_module', 'proc_end_rid_id')

    count = 0
    with codecs.open('data/sample_cid', encoding='gbk') as sample_cid_file:
        for line in sample_cid_file:
            items = line.strip().split(cur_delimiter)
            if len(items) == 2:
                rid = items[0]
                align_id = items[1]
                if start_id <= count % 256 <= end_id:
                    res_tuple = evaluate(rid, align_id)
                    if not res_tuple:
                        continue
                    store_chapter_content, raw_chapter_content, pure_chapter_content, site_id, candidate_chapter_num, \
                    cluster_chapter_num, rank_chapter_num = res_tuple
                    with codecs.open('data/result.txt', 'a', encoding='gbk', errors='ignore') as result_file:
                        result_file.write(str(rid) + cur_delimiter + str(align_id) + cur_delimiter + str(site_id)
                                          + cur_delimiter + str(candidate_chapter_num) + cur_delimiter + str(cluster_chapter_num)
                                          + cur_delimiter + str(rank_chapter_num)
                                          + cur_delimiter + pure_chapter_content + cur_delimiter + store_chapter_content
                                          + cur_delimiter + raw_chapter_content
                                          + cur_linesep)

            count += 1


def evaluate(rid, align_id):
    """
    提取已固化的正文、本次选取的正文、以及去杂之后的正文

    添加几个需要返回的字段
    """
    module = ChapterOptimizeModule()

    rid = int(rid)

    cid = '{0}|{1}'.format(rid, align_id)

    # 从pageDB根据章节的cid读取其章节内容
    silk_server = SilkServer()
    chapter_page = silk_server.get(src='http://test.com', pageid=cid)
    if not chapter_page or 'novel_chapter_type' not in chapter_page or chapter_page['novel_chapter_type'] != 0 \
            or 'blocks' not in chapter_page:
        module.logger.info('cid:{0} not exists in pageDB'.format(cid))
        return False

    store_chapter_content = u''
    for block in chapter_page['blocks']:
        if 'type' in block and block['type'] == 'NOVELCONTENT':
            raw_chapter_content = block['data_value']
            store_chapter_content = ChapterHtmlFilter().chapter_html_filter(raw_chapter_content)

    module.logger.info('rid: {0}, align_id: {1}'.format(rid, align_id))

    total_candidate_chapter_list = module.candidate_chapter_collecion(rid, align_id)
    current_chapter_status = len(total_candidate_chapter_list)
    module.logger.info('total_candidate_chapter_length: {0}'.format(len(total_candidate_chapter_list)))

    candidate_chapter_list = module.candidate_chapter_generate(rid, align_id, total_candidate_chapter_list)
    if len(candidate_chapter_list) == 0:
        module.logger.info('candidate_chapter_list is empty')
        return False

    candidate_chapter_num = len(candidate_chapter_list)

    candidate_chapter_list = module.candidate_chapter_filter(candidate_chapter_list)

    cluster_chapter_num = len(candidate_chapter_list)

    selected_index, candidate_chapter_list = module.candidate_chapter_rank(candidate_chapter_list)

    rank_chapter_num = len(candidate_chapter_list)

    selected_chapter = module.selected_chapter_content_filter(selected_index, candidate_chapter_list)

    if not selected_chapter.there_impurity:
        return False

    raw_chapter_content = selected_chapter.raw_chapter_content
    pure_chapter_content = selected_chapter.pure_chapter_content

    return store_chapter_content, raw_chapter_content, pure_chapter_content, selected_chapter.site_id, \
           candidate_chapter_num, cluster_chapter_num, rank_chapter_num


def evaluate_rid(rid):
    rid = int(rid)

    chapter_db = ChapterDBModule()
    aggregate_dir_list = chapter_db.get_novelaggregationdir_list(rid)
    count = 0
    for (align_id, chapter_index, chapter_url, chapter_status, optimize_chapter_status,
         optimize_chapter_wordsum) in aggregate_dir_list:
        res_tuple = evaluate(rid, align_id)
        if not res_tuple:
            continue
        store_chapter_content, raw_chapter_content, pure_chapter_content, site_id, candidate_chapter_num, \
        cluster_chapter_num, rank_chapter_num = res_tuple
        with codecs.open('data/result.txt', 'a', encoding='gbk', errors='ignore') as result_file:
            result_file.write(str(rid) + cur_delimiter + str(align_id) + cur_delimiter + str(site_id)
                                          + cur_delimiter + str(candidate_chapter_num) + cur_delimiter + str(cluster_chapter_num)
                                          + cur_delimiter + str(rank_chapter_num)
                                          + cur_delimiter + pure_chapter_content + cur_delimiter + store_chapter_content
                                          + cur_delimiter + raw_chapter_content
                                          + cur_linesep)
        count += 1
        if count > 50:
            break


def test_pure():
    print 'test pure begin'
    with codecs.open('data/sample_1') as sample_file:
        for index, line in enumerate(sample_file):
            if index != 5:
                continue
            if line.find(cur_delimiter) >= 0:
                rid, align_id = line.strip().split(cur_delimiter)
                res_tuple = evaluate(rid, align_id)
                if not res_tuple:
                    continue
                store_chapter_content, raw_chapter_content, pure_chapter_content, site_id, candidate_chapter_num, \
                cluster_chapter_num, rank_chapter_num = res_tuple
                with codecs.open('data/result.txt', 'a', encoding='gbk', errors='ignore') as result_file:
                    result_file.write(str(rid) + cur_delimiter + str(align_id) + cur_delimiter + str(site_id)
                                          + cur_delimiter + str(candidate_chapter_num) + cur_delimiter + str(cluster_chapter_num)
                                          + cur_delimiter + str(rank_chapter_num)
                                          + cur_delimiter + pure_chapter_content + cur_delimiter + store_chapter_content
                                          + cur_delimiter + raw_chapter_content
                                          + cur_linesep)

                    break
