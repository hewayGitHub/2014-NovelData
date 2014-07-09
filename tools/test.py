#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-04 02:10'

import time
import random
import hashlib
import md5
import re


def here():
    print('PrimeMusic')

def md64(str):
    """
    """
    str_md5 = md5.new(str).hexdigest()
    str_md5_reverse = ''
    for i in xrange(0, 16):
        str_md5_reverse += str_md5[(16 - i - 1) * 2]
        str_md5_reverse += str_md5[(16 - i) * 2 - 1]
    value = (int(str_md5_reverse[0 : 8], 16) + int(str_md5_reverse[8 : 16], 16)) & 0xffffffff
    value = (value << 32) | (int(str_md5_reverse[16 : 24], 16) + int(str_md5_reverse[24 : 32], 16)) & 0xffffffff

    return value


def auth(word, form = '100000', cip = '61.135.169.80', key = 'nishiwogege123'):
    """
    """
    str_md5 = md5.new(form + word + cip + key).hexdigest()
    value = str_md5[7] + str_md5[3] + str_md5[17] + str_md5[13] + str_md5[1] + str_md5[21]
    return value



if __name__ == '__main__':

    chapter_title = u''
    chapter_title = re.sub(u'^0?第?0[章|回|节]', '', chapter_title)
    print(chapter_title.encode('GBK'))


    #for index in xrange(0, 64):
        #print('/home/work/opscript/backuplog.sh -P /home/work/primesky/{0}/log -F novel.log,err.log -B /home/work/primesky/{0}/log/bak_log'.format(index))
        #print('alter table novel_data{0} add sub_category varchar(128) not null;'.format(index))
        #print('select sleep(30);')
        #print('drop table if exists novel_cluster_rid_info{0};'.format(index))
        #print('create table novel_cluster_rid_info{0} like novel_cluster_rid_info;'.format(index))
        #print('dir_fmt_info{0}:0'.format(index))
    here()    







