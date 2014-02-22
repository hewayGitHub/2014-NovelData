#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-05 13:15'

import logging
from novel.cluster.ClusterNodeModule import *
from novel.cluster.ClusterEdgeModule import *

def here():
    print('PrimeMusic')


def init_log(name):
    """
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('./log/{0}.log'.format(name))
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info('{0} log init successful!'.format(name))


def cluster_node_module():
    """
    """
    novel_module = ClusterNodeModule()
    novel_module.init()
    novel_module.run()


def cluster_edge_module():
    """
    """
    novel_module = ClusterEdgeModule()
    novel_module.init()
    novel_module.run()


if __name__ == '__main__':
    init_log('novel')
    init_log('err')

    #cluster_node_module()
    #cluster_edge_module()
