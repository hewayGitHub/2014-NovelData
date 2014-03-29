#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-03-05 15:51'


import urllib
import requests
import time
import json
import logging

from basic.NovelStructure import *


def here():
    print('PrimeMusic')


class SilkServer(object):
    """
    """
    __metaclass__ = Singleton


    def __init__(self):
        self._pathPrefix = 'http://10.211.141.17:8851/webapp'
        self._timeout = 30
        self._defaultParam = {
            'structpage': 1,
            'siteappid' : 376409,
            'version' : 0,
            'platform' : 'other',
            'onlyspdebug' : 1,
            'srd' : 1
        }

        self.logger = logging.getLogger('novel.silkserver')
        self.err = logging.getLogger('err.silkserver')


    def get(self, src, pageid = None):
        param = {}
        param.update(self._defaultParam)
        if pageid != None :
            param['xs_pageid'] = pageid
        path = self._pathPrefix + '?' + urllib.urlencode(param) + '&' + urllib.urlencode({'src': src + '#reqtype=1'})
        header={'Host' : 'internal_wise_domain.baidu.com'}
        try:
            r = requests.get(path, headers = header, timeout = self._timeout)
            if r.status_code != requests.codes.ok:
                #self.err.warning("Failed to request silkserver.get, status_code:{0}, path:{1}".format(r.status_code, r.url))
                return False
            result = r.json()
            return result
        except Exception as e:
            #self.err.warning("Failed to request silkserver.get, exception:{0}".format(e))
            return False


    def save(self, pageid, data, expr = 315360000):
        data['page_expire_time'] = int(time.time()) + expr
        param = {}
        param.update(self._defaultParam)
        param['xs_pageid'] = pageid
        param['xs_pageexpiretime'] = int(time.time()) + expr
        path = self._pathPrefix + '?' + urllib.urlencode(param) + '&' + urllib.urlencode({'src': 'www.baidu.com'})
        try:
            str_data = json.dumps(data)
            header = {
                'content-type': 'application/json',
                'Host' : 'internal_wise_domain.baidu.com'
            }
            r = requests.post(path, data=str_data, headers=header)
            if r.status_code != requests.codes.ok:
                self.err.warning("Failed to request silkserver.save, status_code:{0}, path:{1}".format(r.status_code, r.url))
                return False
        except Exception as e:
            self.err.warning("Failed to request silkserver.save, exception:{0}, pageid:{1}".format(e, pageid))
            return False
        return True


if __name__ == '__main__':
    here()    







