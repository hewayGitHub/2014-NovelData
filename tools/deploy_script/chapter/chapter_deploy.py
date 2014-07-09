#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-03-26 15:36'

import json
import socket
import os
import time
import traceback

#=========== 用户修改项 ================
# 部署配置文件
DEPLOY_CONF_FILE = "./chapter_deploy.json"

# 模块配置文件
MODULE_CONF_FILE = "./{0}/conf/NovelChapterModule.conf"


def set_module_conf_file(unit, proc_start_rid_id, proc_end_rid_id):
    """
        修改当前进程的配置信息
    """
    try:
        raw_file = open(MODULE_CONF_FILE.format('novel-data'), 'r')
        target_file = open(MODULE_CONF_FILE.format(unit), 'w')
        for line in raw_file:
            if line.find("proc_start_rid_id") >= 0 :
                target_file.write("proc_start_rid_id: {0}\n".format(proc_start_rid_id))
            elif line.find("proc_end_rid_id") >= 0 :
                target_file.write("proc_end_rid_id: {0}\n".format(proc_end_rid_id))
            else :
                target_file.write(line)
        raw_file.close()
        target_file.close()
    except IOError as e:
        print "error: {0}".format(e)
        return False

    return True


def deploy_unit(unit, proc_start_rid_id, proc_end_rid_id):
    """
        拷贝进程目录
    """
    if os.path.exists("./{0}".format(unit)):
        os.system("rm -rf {0}".format(unit))
    res = os.system("cp -r novel-data {0}".format(unit))
    if res != 0:
        print "Failed to cp novel-data to {0}".format(unit)
        return False

    if not set_module_conf_file(unit, proc_start_rid_id, proc_end_rid_id):
        print "Failed to set module conf file"
        return False

    return True


def deploy_units(machine):
    """
        修改模块基础配置信息
    """
    unit_num = machine["unit_num"]
    proc_start_rid_id = machine["proc_start_rid_id"]
    proc_end_rid_id = machine["proc_end_rid_id"]
    rid_segment = (proc_end_rid_id - proc_start_rid_id + 1) / unit_num
    for unit in xrange(0, unit_num):
        if not deploy_unit(unit, proc_start_rid_id + unit * rid_segment, proc_start_rid_id + (unit + 1) * rid_segment - 1):
            print "Failed to deploy unit: {0}".format(unit["id"])
            return False

    return True


def create_env(conf_file):
    """
        根据配置来生成模块部署方案
    """
    host_name = socket.gethostname()
    is_deploy_success = False
    with open(conf_file, "r") as f:
        deploy_json = json.load(f)
        for machine in deploy_json:
            if machine["host"] == host_name:
                if not deploy_units(machine):
                    print "Failed to deploy..."
                    return False
                else:
                    is_deploy_success = True
            else:
                print "meeting host_name: {0}".format(machine["host"])

    return is_deploy_success


if __name__ == "__main__":
    try:
        create_env(DEPLOY_CONF_FILE)
    except Exception, e :
        print("error: {0}".format(traceback.format_exc()))
        exit(1)
    exit(0)







