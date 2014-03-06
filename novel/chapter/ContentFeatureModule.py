#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-03-05 17:26'

import logging

from basic.NovelStructure import *
from basic.SilkServerModule import *
from novel.chapter.ChapterDB import *
from public.BasicStringMethod import *

def here():
    print('PrimeMusic')


class ContentFeatureModule(object):
    """
        根据正文信息，提取出其中的特征信息
    """

    def __init__(self):
        """
        """
        self.logger = logging.getLogger('novel.chapter.feature')
        self.err = logging.getLogger('err.chapter.feature')


    def chapter_content_generate(self, chapter_content):
        """
        """
        if chapter_content is False:
            return False
        if not chapter_content.has_key('block'):
            return False

        data = ''
        for block in chapter_content['block']:
            if block['type'] == 'NOVELCONTENT':
                data = block['data_value']
                break
        data = html_filter(data)
        return data


    def novel_content_generate(self, rid, local = False):
        """
            获取这个gid对应的小说正文内容
        """
        if local is True:
            content = open('./data/{0}.txt'.format(rid), 'r').read()
            content = content.decode('GBK', 'ignore')
            return content

        chapter_db = ChapterDBModule()
        silk_server = SilkServer()

        content = ''
        result = chapter_db.get_novelauthoritydir_list(rid)
        for (rid, align_id, chapter_id, chapter_url) in result:
            chapter_content = silk_server.get(src = chapter_url, pageid = '{0}|{1}'.format(rid, align_id))
            chapter_content = self.chapter_content_generate(chapter_content)
            content += chapter_content
        try:
            file = open('./data/{0}'.format(rid), 'w')
            file.write(content.encode('GBK', 'ignore'))
        except Exception, e:
            self.err.warning('[error: {0}]'.format(e))



if __name__ == '__main__':
    here()    







