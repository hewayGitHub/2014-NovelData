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
        result = requests.get(url).json()
    except Exception, e :
        return False
    return result


def get_gid(gid, nocache, error_count):
    """
    """
    src = 'http://10.57.249.19:8080/open/dataservice/novel/aggregation/gid?lcid=mco_ds&query={0}&nocache={1}'.format(gid, nocache)
    result = send_get_requests(src)

    if result is False:
        error_count.increment()
        return False
    if result.has_key('error_code'):
        error_count.increment()
        return False

    return True


def get_dirurl(url, nocache, error_count):
    """
    """
    src = 'http://10.57.249.19:8080/open/dataservice/novel/aggregation/url?lcid=mco_ds&query={0}&nocache={1}'.format(url, nocache)
    result = send_get_requests(src)

    if result is False:
        error_count.increment()
        return False
    if result.has_key('error_code'):
        error_count.increment()
        return False

    return True


def get_chapterurl(url, nocache, error_count):
    """
    """
    src = 'http://10.212.84.58:8080/open/dataservice/novel/content/url?lcid=mco_ds&query={0}&nocache={1}'.format(url, nocache)
    #src = 'http://10.40.57.16:8080/open/dataservice/novel/content/url?lcid=mco_ds&query={0}&nocache={1}'.format(url, nocache)
    result = send_get_requests(src)

    if result is False:
        error_count.increment()
        return False
    if result.has_key('error_code'):
        error_count.increment()
        return False

    return True


def gid():
    """
    """
    rid_list = []
    for line in open('./data/rid.txt', 'r').readlines():
        rid = int(line.strip())
        rid_list.append(rid)

    error_count = counter()
    frequency = 5
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


def dirurl():
    """
    """
    dir_url_list = []
    for line in open('./data/dirurl.txt', 'r').readlines():
        dir_url = int(line.strip())
        dir_url_list.append(dir_url)

    error_count = counter()
    frequency = 5
    for index, dir_url in enumerate(dir_url_list):
        get_request = threading.Thread(name=index, target=get_dirurl, args=(dir_url, 0, error_count))
        get_request.start()
        if index % frequency == 0 :
            time.sleep(1.0)

    main_thread = threading.currentThread()
    for t in threading.enumerate() :
        if t is main_thread :
            continue
        t.join()
    print(error_count.value, len(dir_url_list))


def chapter():
    """
    """
    chapter_url_list = []
    for line in open('./data/chapter.txt', 'r').readlines():
        chapter_url = int(line.strip())
        chapter_url_list.append(chapter_url)

    error_count = counter()
    frequency = 5
    for index, chapter_url in enumerate(chapter_url_list):
        get_request = threading.Thread(name=index, target=get_chapterurl, args=(chapter_url, 0, error_count))
        get_request.start()
        if index % frequency == 0 :
            time.sleep(1.0)

    main_thread = threading.currentThread()
    for t in threading.enumerate() :
        if t is main_thread :
            continue
        t.join()
    print(error_count.value, len(chapter_url_list))


if __name__ == '__main__':
    #gid()
    #dirurl()
    #chapter()
    here()


