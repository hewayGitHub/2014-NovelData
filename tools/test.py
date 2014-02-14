#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-04 02:10'

from collections import defaultdict


def here():
    print('PrimeMusic')


if __name__ == '__main__':

    if 'a' not in ['a', 'n', 'b']:
        here()
    string = 'abcdefg'
    print(string[-6 : ])

    string = ''
    if not string:
        here()
    for index in xrange(0, 0):
        print('drop table if exists novel_cluster_edge_info{0};'.format(index))
        print('create table novel_cluster_edge_info{0} like novel_cluster_edge_info;'.format(index))
        #print('dir_fmt_info{0}:0'.format(index))
    here()    







