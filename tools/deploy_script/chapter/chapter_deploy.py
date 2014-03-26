#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-03-26 15:36'

import json
import socket
import os
import time
import traceback

#=========== �û��޸��� ================
# ���������ļ�
DEPLOY_CONF_FILE = "./chapter_deploy.json"

# ģ�������ļ�
MODULE_CONF_FILE = "./{0}/conf/NovelChapterModule.conf"


def set_module_conf_file(unit):
    """
        �޸ĵ�ǰ���̵�������Ϣ
    """
    try:
        raw_file = open(MODULE_CONF_FILE.format('NovelData'), 'r')
        target_file = open(MODULE_CONF_FILE.format(unit['id']), 'w')
        for line in raw_file:
            if line.find("proc_start_rid_id") >= 0 :
                target_file.write("proc_start_rid_id: {0}\n".format(unit["proc_start_rid_id"]))
            elif line.find("proc_end_rid_id") >= 0 :
                target_file.write("proc_end_rid_id: {0}\n".format(unit["proc_end_rid_id"]))
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
        ��������Ŀ¼
    """
    if os.path.exists("./{0}".format(unit["id"])):
        os.system("rm -rf {0}".format(unit["id"]))
    res = os.system("cp -r NovelData {0}".format(unit["id"]))
    if res != 0:
        print "Failed to cp NovelData to {0}".format(unit["id"])
        return False

    if not set_module_conf_file(unit):
        print "Failed to set module conf file"
        return False

    return True


def deploy_units(machine):
    """
        �޸�ģ�����������Ϣ
    """
    units = machine["units"]
    for unit in units:
        if not deploy_unit(unit):
            print "Failed to deploy unit: {0}".format(unit["id"])
            return False

    return True


def create_env(conf_file):
    """
        ��������������ģ�鲿�𷽰�
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







