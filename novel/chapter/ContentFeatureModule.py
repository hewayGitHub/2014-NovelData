#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-03-05 17:26'


def here():
    print('PrimeMusic')


class ContentFeatureModule(object):
    """
        ����������Ϣ����ȡ�����е�������Ϣ
    """

    def __init__(self):
        """
        """

    def novel_content_generate(self, gid, local = False):
        """
            ��ȡ���gid��Ӧ��С˵��������
        """
        if local is True:
            content = open('./data/{0}.txt'.format(gid), 'r').read()
            content = content.decode('GBK', 'ignore')
            return content

        resul =


if __name__ == '__main__':
    here()    







