#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-04 02:10'

from collections import defaultdict


def here():
    print('PrimeMusic')


if __name__ == '__main__':
    for index in xrange(0, 256):
        print('alter table novel_data{0} add sub_category varchar(128) not null;'.format(index))
        #print('drop table if exists novel_cluster_rid_info{0};'.format(index))
        #print('create table novel_cluster_rid_info{0} like novel_cluster_rid_info;'.format(index))
        #print('dir_fmt_info{0}:0'.format(index))
    here()    







