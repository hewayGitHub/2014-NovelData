#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-03-16 18:40'

from collections import defaultdict
from novel.cluster.ClusterDB import *

def here():
    print('PrimeMusic')


if __name__ == '__main__':

    cluster_db = ClusterDBModule()
    novel_info_list = cluster_db.get_noveldata_all('novel_cluster_dir_info', 'book_name, pen_name')

    book_name_dict = defaultdict(int)
    pen_name_dict = defaultdict(int)
    for (book_name, pen_name) in novel_info_list:
        book_name_dict[book_name] += 1
        pen_name_dict[pen_name] += 1

    for (pen_name, pen_name_count) in pen_name_dict.items():
        if pen_name_count > 1000:
            print(pen_name)

    for (book_name, book_name_count) in book_name_dict.items():
        if book_name_count > 1000:
            print(book_name)







