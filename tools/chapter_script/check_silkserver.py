#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-04-03 20:45'

from basic.SilkServerModule import *

def here():
    print('PrimeMusic')


if __name__ == '__main__':

    cid = '3278655874|12313662799987017181'
    src = 'http://www.shushuw.cn/shu/30523/5784287.html'

    silkserver = SilkServer()
    chapter_page = silkserver.get(src, cid)

    if not chapter_page:
        print('no source !')
    if not chapter_page.has_key('blocks'):
        print('no source !')

    raw_chapter_content = ''
    for block in chapter_page['blocks']:
        if block['type'] == 'NOVELCONTENT':
            raw_chapter_content = block['data_value']
    raw_chapter_content = html_filter(raw_chapter_content)
    if len(raw_chapter_content) < 50:
        print('no source !')
    print(raw_chapter_content.encode('GBK', 'ignore'))







