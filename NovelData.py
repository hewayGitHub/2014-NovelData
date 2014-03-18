#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-05 13:15'

import logging
import sys
import os
from novel.cluster.ClusterNodeModule import *
from novel.cluster.ClusterEdgeModule import *
from novel.cluster.ClusterModule import *
from novel.chapter.ChapterOptimizeModule import *

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


def set_status_file():
    """
    """
    if os.path.exists('./data/status'):
        return False
    try:
        f = open('./data/status', 'w')
        pid = os.getpid()
        f.write('{0}'.format(pid))
        f.close()
    except Exception, e:
        return False

    return True


def remove_status_file():
    """
    """
    try:
        os.remove('./data/status')
    except Exception, e:
        return True
    return True


def cluster_node_module():
    """
    """
    novel_module = ClusterNodeModule()
    novel_module.run()


def cluster_edge_module():
    """
    """
    novel_module = ClusterEdgeModule()
    novel_module.run()


def cluster_update_module():
    """
    """
    novel_module = ClusterNodeModule()
    novel_module.run(True)


def cluster_module():
    """
    """
    novel_modoule = ClusterModule()
    novel_modoule.run()


def debug():
    """
    """
    remove_status_file()
    novel_module = ChapterOptimizeModule()
    novel_module.run()


if __name__ == '__main__':
    init_log('novel')
    init_log('err')

    if len(sys.argv) != 2:
        print('no module selected !')
        exit()

    module = sys.argv[1]
    if module not in ['node', 'edge', 'cluster', 'update', 'test']:
        print('no module selected !')
        exit()

    if not set_status_file():
        print('some process is running !')
        exit()

    if module == 'node':
        cluster_node_module()
    if module == 'edge':
        cluster_edge_module()
    if module == 'cluster':
        cluster_module()
    if module == 'update':
        cluster_update_module()
    if module == 'test':
        debug()

    remove_status_file()
