#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-03-09 16:32'


#!/usr/bin/env python
# -*- coding: GBK
# author: zhangjianrong
# desc:
import json
import socket
import os
import time
import traceback

#=========== 用户修改项 ================
# 部署配置文件
DEPLOY_CONF_FILE = "./cluster_deploy.json"

# 时间配置文件
TIME_CONF_FILE = "./NovelData/data/NovelClusterModule.time"
# 模块配置文件
MODULE_CONF_FILE = "./{0}/conf/NovelClusterModule.conf"


def set_module_conf_file(unit):
    """
        修改当前进程的配置信息
    """
    try:
        raw_file = open(MODULE_CONF_FILE.format('NovelData'), 'r')
        target_file = open(MODULE_CONF_FILE.format(unit['id']), 'w')
        for line in raw_file:
            if line.find("proc_start_site_id") >= 0 :
                target_file.write("proc_start_site_id: {0}\n".format(unit["proc_start_site_id"]))
            elif line.find("proc_end_site_id") >= 0 :
                target_file.write("proc_end_site_id: {0}\n".format(unit["proc_end_site_id"]))
            elif line.find("proc_start_gid_id") >= 0 :
                target_file.write("proc_start_gid_id: {0}\n".format(unit["proc_start_gid_id"]))
            elif line.find("proc_end_gid_id") >= 0 :
                target_file.write("proc_end_gid_id: {0}\n".format(unit["proc_end_gid_id"]))
            else :
                target_file.write(line)
        raw_file.close()
        target_file.close()
    except IOError as e:
        print "error: {0}".format(e)
        return False

    return True


def deploy_unit(unit):
    """
        拷贝进程目录
    """
    if os.path.exists("./{0}".format(unit["id"])):
        os.system("rm -rf {0}".format(unit["id"]))
    res = os.system("cp -r dataframe {0}".format(unit["id"]))
    if res != 0:
        print "Failed to cp dataframe to {0}".format(unit["id"])
        return False

    if not set_module_conf_file(unit):
        print "Failed to set module conf file"
        return False

    return True


def deploy_units(machine):
    """
        修改模块基础配置信息
    """
    try :
        #start_time = int(time.time()) - 120
        start_time = 0
        time_conf_file = open(TIME_CONF_FILE, "w")
        for table_id in xrange(0, machine["proc_table_num"]) :
            time_conf_file.write("{0}{1}:{2}\n".format(machine["proc_table_name"], table_id, start_time))
        time_conf_file.close()
    except Exception, e :
        print "error: {0}".format(e)
        return False

    units = machine["units"]
    for unit in units:
        if not deploy_unit(unit):
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







