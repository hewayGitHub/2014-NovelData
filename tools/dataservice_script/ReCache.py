#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-04-02 20:25'

import requesets


def here():
    print('PrimeMusic')


def get(gid, nocache = 0):
    """
    """
    src = 'http://m.baidu.com/open/dataservice/novel/aggregation/gid?lcid=mco_ds&query={0}&nocache={1}'.format(gid, nocache)
    try:
        result = requests.get(src).json()
    except Exception, e:
        print('Failed to request dataservice, exception: {0}, src: {1}'.format(e, src))
        return False
    if result.has_key('error_code'):
        print('Failed to get data from dataservice, src: {0}'.format(src))
        return False

    return True


if __name__ == '__main__':


    rid_list = []
    for line in open('./data/rid.txt', 'r').readlines():
        rid = int(line.strip())
        rid_list.append(rid)

    for index, rid in enumerate(rid_list):
        result = get(rid, 0)
        if not result:
            print('error rid: {0}'.format(rid))


    here()







