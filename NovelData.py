#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-05 13:15'

import logging
from novel.cluster.ClusterNodeModule import *

def here():
    print('PrimeMusic')

def init_log(name):
    """
    """
    logger = logging.getLogger(name)
    fh = logging.FileHandler('./log/{0}.log'.format(name))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info('{0} log init successful!'.format(name))

if __name__ == '__main__':
   init_log('novel')
   init_log('err')

   node_module = ClusterNodeModule()
   node_module.generate_novel_node_list(6, 0)







