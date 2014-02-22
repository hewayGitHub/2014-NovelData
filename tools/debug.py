#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-17 14:06'


def here():
    print('PrimeMusic')


def print_novel_node(novel_node):
    """
    """
    print('book_name: {0}, pen_name: {1}, dir_url: {2}'.format(novel_node.book_name.encode('GBK'), novel_node.pen_name.encode('GBK'), novel_node.dir_url))
    print(',  '.join('%s' % chapter.chapter_title.encode('GBK') for chapter in novel_node.chapter_list))


def print_cluster_node(cluster_node):
    """
    """
    print('book_name: {0}, pen_name: {1}'.format(cluster_node.book_name.encode('GBK'), cluster_node.pen_name.encode('GBK')))



def compare_similar_novel(novel_node_x, novel_node_y, similarity):
    """
    """
    print_novel_node(novel_node_x)
    print_novel_node(novel_node_y)
    print(similarity)

if __name__ == '__main__':
    here()    







