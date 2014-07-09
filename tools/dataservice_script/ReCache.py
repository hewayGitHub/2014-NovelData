#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-04-02 20:25'

import threading
import requests
import logging
import time
import json


def here():
    print('PrimeMusic')


logger = logging.getLogger("work")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class counter(object) :
    def __init__(self, start = 0):
        self.lock = threading.Lock()
        self.value = start

    def increment(self):
        self.lock.acquire()
        try:
            self.value += 1
        finally:
            self.lock.release()


def send_get_requests(url):
    try :
        result = requests.get(url, timeout=2.0).json()
    except Exception, e :
        logger.info('timeout')
        return False
    return result


def get_gid(gid, nocache, error_count):
    """
    """
    src = 'http://10.57.249.19:8080/open/dataservice/novel/aggregation/gid?lcid=mco_ds&query={0}&nocache={1}'.format(gid, nocache)
    result = send_get_requests(src)

    if result is False:
        error_count.increment()
        #logger.info('error: {0}'.format('no'))
        return False
    if result.has_key('error_code'):
        error_count.increment()
        logger.info('error: {0}'.format(result['error_code']))
        return False

    return True

def gid():
    """
    """
    rid_list = []
    for index in xrange(0, 2000):
        rid_list.append(3994882921)

    error_count = counter()
    frequency = 5000
    for index, rid in enumerate(rid_list):
        get_request = threading.Thread(name=index, target=get_gid, args=(rid, 0, error_count))
        get_request.start()
        if index % frequency == 0 :
            time.sleep(1.0)

    main_thread = threading.currentThread()
    for t in threading.enumerate() :
        if t is main_thread :
            continue
        t.join()
    print(error_count.value, len(rid_list))


if __name__ == '__main__':
    gid()
    #dirurl()
    #chapter()
    here()


