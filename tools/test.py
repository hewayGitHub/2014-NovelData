#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-04 02:10'

import time
import random
from collections import defaultdict


def here():
    print('PrimeMusic')


if __name__ == '__main__':

    d = {}
    d[1] = 2
    d[2] = 3
    d[3] = 0
    print(sorted(d.items(), lambda a, b: cmp(a[1], b[1])))

    d = [1, 2, 3, 4, 5]
    random.shuffle(d)
    print(d)
    for index in xrange(0, 256):
        print('alter table novel_data{0} add sub_category varchar(128) not null;'.format(index))
        #print('select sleep(30);')
        #print('drop table if exists novel_cluster_rid_info{0};'.format(index))
        #print('create table novel_cluster_rid_info{0} like novel_cluster_rid_info;'.format(index))
        #print('dir_fmt_info{0}:0'.format(index))
    here()    







