#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-27 17:56'

import os
import sys

def here():
    print('PrimeMusic')


process_number = 16

def deploy_unit(unit):
    """
    """
    if os.path.exists('./{0}'.format(unit)):
        os.system('mkdir -p BACKUP && rm -rf BACKUP/{0} && mv {0} BACKUP/'.format(unit))
    res = os.system('cp -r NovelData {0}'.format(unit))
    if res != 0:
        print('failed to cp dataframe to {0}'.format(unit))
        return False
    return True


def modify_unit(unit, start_site_id, end_site_id, start_gid_id, end_gid_id):
    """
    """
    try:
        source_file = open('./NovelData/conf/NovelClusterModule.conf', 'r')
        target_file = open('./{0}/conf/NovelClusterModule.conf'.format(unit), 'w')
        for line in source_file:
            if line.find('proc_start_site_id') >= 0:
                target_file.write('proc_start_site_id: {0}\n'.format(start_site_id))
            elif line.find('proc_end_site_id') >= 0:
                target_file.write('proc_end_site_id: {0}\n'.format(end_site_id))
            elif line.find('proc_start_gid_id') >= 0:
                target_file.write('proc_start_gid_id: {0}\n'.format(start_gid_id))
            elif line.find('proc_end_gid_id') >= 0:
                target_file.write('proc_end_gid_id: {0}\n'.format(end_gid_id))
            else:
                target_file.write(line)
        source_file.close()
        target_file.close()
    except Exception, e:
        print('modify error [unit: {0}, err: {1}]'.format(unit, e))
        return False
    return True


def deploy():
    """
    """
    node_segment = 10
    edge_segment = 16
    for unit in xrange(0, process_number):
        deploy_unit(unit)
        site_id = unit * node_segment
        gid_id = unit * edge_segment
        modify_unit(unit, site_id, site_id + node_segment - 1, gid_id, gid_id + edge_segment - 1)


def start(module):
    """
    """
    for unit in xrange(0, process_number):
        res = os.system('cd {0} && nohup python NovelData.py {1} & && cd ..'.format(unit, module))
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
    if module not in ['deploy', 'stop', 'node', 'edge', 'cluster', 'update']:
        print('no module selected !')
        exit()

    if module == 'deploy':
        deploy()
    elif module == 'stop':
        stop()
    else:
        start(module)






