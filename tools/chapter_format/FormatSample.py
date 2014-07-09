#!/usr/bin/env python
# -*- coding:GBK -*-

__author__ = 'hewei13'
__date__ = '2014-6-17 9:37'


import logging
import codecs
import os

cur_linesep = os.linesep
cur_delimiter = str(chr(1))  # 存储文件的分隔符


def init_log(name, debug=True):
    """
    初始化log，如果是debug模式，直接输出到终端
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


def format_sample(debug=True):
    """
    """
    logger = init_log('novel.chapter', debug)
    err = init_log('err.chapter', debug)

    for site_id in os.listdir('data/select_sample/'):
        fmt_file = codecs.open('data/fmt_sample/' + site_id, 'a', encoding='gbk')
        with codecs.open('data/select_sample/' + site_id, encoding='gbk') as site_file:
            for line in site_file:
                line = line.replace(u'</p><p style="text-indent:2em;">', u'[分段]')
                line = line.replace(u'<p style="text-indent:2em;">', '')
                line = line.replace(u'</p>', '')

                fmt_file.write(line.strip() + cur_linesep)


def format_sample_2(debug=True):
    """
    """
    logger = init_log('novel.chapter', debug)
    err = init_log('err.chapter', debug)

    for site_id in os.listdir('data/select_sample/'):
        fmt_file = codecs.open('data/csv_sample/' + site_id + '.csv', 'a', encoding='gbk')
        with codecs.open('data/select_sample/' + site_id, encoding='gbk') as site_file:
            for line in site_file:
                items = line.split('\t')[:5]

                fmt_file.write(','.join(items) + cur_linesep)

if __name__ == '__main__':
    format_sample_2()
