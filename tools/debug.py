#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-17 14:06'


def here():
    print('PrimeMusic')


def debug_novel_node(novel_node):
    """
    """
    print('book_name: {0}, pen_name: {1}, dir_url: {2}'.format(novel_node.book_name.encode('GBK'), novel_node.pen_name.encode('GBK'), novel_node.dir_url))
    print(',  '.join('%s' % chapter.chapter_title.encode('GBK') for chapter in novel_node.chapter_list))


def debug_cluster_node(cluster_node):
    """
    """
    print('gid: {0}, book_name: {1}, pen_name: {2}'.format(cluster_node.gid, cluster_node.book_name.encode('GBK'), cluster_node.pen_name.encode('GBK')))
    for novel_node in cluster_node.novel_node_list:
        print(', '.join('%s' % chapter.chapter_title.encode('GBK') for chapter in novel_node.chapter_list))


def debug_cluster_similarity(cluster_node_x, cluster_node_y, match_number):
    """
    """
    print(match_number, len(cluster_node_x.novel_node_list), len(cluster_node_y.novel_node_list))
    debug_cluster_node(cluster_node_x)
    debug_cluster_node(cluster_node_y)
    print('---')
    print('---')
    print('---')


if __name__ == '__main__':
    here()    







