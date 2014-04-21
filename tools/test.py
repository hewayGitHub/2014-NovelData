#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-04 02:10'

import time
import random
import hashlib
from collections import defaultdict


def here():
    print('PrimeMusic')

class dd(object):
    """
    """
    def __init__(self):
        """
        """
        self.a = ''


if __name__ == '__main__':

    book_name = '唯一的小宇'
    m = hashlib.md5()
    m.update(book_name)
    table_id = int(m.hexdigest(), 16) % 256
    print(table_id)

    for index in xrange(0, 0):
        print('alter table novel_data{0} add sub_category varchar(128) not null;'.format(index))
        #print('select sleep(30);')
        #print('drop table if exists novel_cluster_rid_info{0};'.format(index))
        #print('create table novel_cluster_rid_info{0} like novel_cluster_rid_info;'.format(index))
        #print('dir_fmt_info{0}:0'.format(index))
    here()    







