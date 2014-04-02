#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-03-26 15:35'

import os
import sys

def here():
    print('PrimeMusic')

process_number = 32

def start(module):
    """
    """
    for unit in xrange(0, process_number):
        if os.path.exists('./{0}/data/status'.format(unit)):
            print('failed start [unit: {0}, module: {1}]'.format(unit, module))
            continue

        res = os.system('cd {0} && python NovelData.py {1} &'.format(unit, module))
        if res != 0:
            print('failed start [unit: {0}, module: {1}]'.format(unit, module))
            return False
        else:
            print('success start [unit: {0}, module: {1}]'.format(unit, module))


def stop():
    """
    """
    for unit in xrange(0, process_number):
        try:
            pid = open('./{0}/data/status'.format(unit), 'r').read()
        except Exception, e:
            pid = 0
        if pid == 0:
            print('no need to stop module {0}'.format(unit))
        else:
            os.system('kill -9 {0}'.format(pid))
            print('stop module {0}'.format(unit))


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('no module selected !')
        exit()

    module = sys.argv[1]
    if module not in ['stop', 'node', 'edge', 'cluster', 'update', 'chapter', 'test']:
        print('no module selected !')
        exit()

    if module == 'stop':
        stop()
    else:
        start(module)






