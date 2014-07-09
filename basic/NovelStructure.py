#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-02 14:05'

from public.BasicStringMethod import *


def here():
    print('PrimeMusic')


class Singleton(type):
    """
        ����ģʽ
    """

    def __call__(self, *args, **kwargs):
        if '_instance' not in vars(self):
            self._instance = super(Singleton, self).__call__(*args, **kwargs)
        return self._instance


class NovelNodeInfo(object):
    """
        һ��С˵�Ļ�����Ϣ����Ӧ��С˵�����е�һ����
    """

    def __init__(self, site_id=0, site="", site_status=0,
                 dir_id=0, dir_url="",
                 gid=0, book_name="", pen_name="",
                 chapter_count=0, chapter_word_sum=0, last_chapter_title=''):
        self.site_id = site_id
        self.site = site
        self.site_status = site_status
        self.dir_id = dir_id
        self.dir_url = dir_url
        self.gid = gid
        self.rid = gid
        self.book_name = book_name
        self.pen_name = pen_name
        self.chapter_count = chapter_count
        self.chapter_word_sum = chapter_word_sum
        self.last_chapter_title = last_chapter_title
        self.chapter_list = []


    def generate_insert_tuple(self):
        """
        """
        result = (
            self.site_id, self.site, self.site_status,
            self.dir_id, url_format(self.dir_url),
            self.gid, self.rid, string_format(self.book_name), string_format(self.pen_name),
            self.chapter_count, self.chapter_word_sum, string_format(self.last_chapter_title)
        )
        return result


    def generate_update_tuple(self):
        """
        """
        result = (
            self.gid, self.rid,
            string_format(self.book_name), string_format(self.pen_name),
            self.chapter_count, string_format(self.last_chapter_title),
            self.dir_id
        )
        return result



class NovelChapterInfo(object):
    """
        һ���½ڵĻ�����Ϣ���½���Ϣ��Ϊ������һ������
    """

    def __init__(self, gid=0, site_id=0, dir_id=0, chapter_sort=0,
                 chapter_id=0, chapter_url="", chapter_title="", chapter_status=0, word_sum=0):
        self.gid = gid
        self.site_id = site_id
        self.dir_id = dir_id
        self.chapter_sort = chapter_sort
        self.chapter_id = chapter_id
        self.chapter_url = chapter_url
        self.chapter_title = chapter_title
        self.raw_chapter_title = chapter_title
        self.chapter_status = chapter_status
        self.word_sum = word_sum


    def generate_insert_tuple(self):
        """
        """
        result = (
            self.gid, self.site_id, self.dir_id, self.chapter_sort, self.chapter_id,
            url_format(self.chapter_url), string_format(self.chapter_title), string_format(self.raw_chapter_title),
            self.chapter_status, self.word_sum
        )
        return result


    def generate_delete_tuple(self):
        """
        """
        result = (self.dir_id, self.chapter_sort)
        return result


    def generate_update_tuple(self):
        """
        """
        result = (
            self.gid, string_format(self.chapter_title), string_format(self.raw_chapter_title),
            self.dir_id, self.chapter_sort
        )
        return result



class NovelClusterInfo(object):
    """
        һ���صĻ�����Ϣ������gid��ͬ������С˵
    """

    def __init__(self, gid=0):
        """
        """
        self.gid = gid
        self.novel_node_list = []

        self.book_name = ''
        self.pen_name = ''


class ClusterEdgeInfo(object):
    """
        ����ֱ�ӵıߵ���Ϣ��������С˵�����ƶ�
    """

    def __init__(self, gid_x=0, gid_y=0, similarity=0):
        """
            һ���ߵ���Ϣ
        """
        self.gid_x = gid_x
        self.gid_y = gid_y
        self.similarity = int(similarity * 100)


    def generate_insert_tuple(self):
        """
        """
        result = (self.gid_x, self.gid_y, self.similarity)
        return result


class NovelContentInfo(object):
    """
        һ��С˵���½���Ϣ
    """

    def __init__(self, rid=0, align_id=0, dir_id=0, chapter_id=0, chapter_url='', chapter_title=''):
        """
        """
        self.rid = rid
        self.align_id = align_id
        self.dir_id = dir_id
        self.chapter_id = chapter_id
        self.chapter_url = chapter_url
        self.chapter_title = chapter_title

        self.site_id = 0
        self.site_status = 0

        self.chapter_page = ''
        self.raw_chapter_content = ''  # spider��ȡ������
        self.fmt_chapter_content = ''  # ���˺ʹ����Html������ģ�����p��ǩ
        self.pure_chapter_content = ''  # ȥ��֮�������

        self.paragraph_list = None  # ��fmt_chapter_content�Ļ�����������ȥ��
        self.valid_word_sum = 0  # ͨ��html���˺ʹ����Լ�һЩ�������ʵĴ���֮��ĺ��֡����֡���ĸ������
        self.valid_cn_sum = 0  # �����ַ���
        self.valid_para_count = -1  # ��Ϊparagraph_list���ܰ�����Ҫ��ɾ���Ķ��䣬valid_para_countΪ��Ч������

        self.there_impurity = False


class NovelParagraph(object):
    """
        ����ȥ���У�һ��С˵�������Ϣ
    """
    def __init__(self, raw_content='', fmt_content='', para_index=0, before_word_sum=0):
        """
        """
        self.raw_content = raw_content  # html���˺ʹ����Ķ�������

        # ��raw_content�Ļ����ϣ�����վ�㼶������������֮������ݡ�
        # �������need_removeΪFalse���������������Ϊfmt_content
        self.fmt_content = fmt_content
        self.para_index = para_index  # �ڼ��£���0��ʼ��������para_listֱ������
        self.before_word_sum = before_word_sum  # ����֮ǰ�����ַ���

        # ��Ӧ���������о��ӵ���ʼ��������ֹ����
        self.sentence_start_index = -1
        self.sentence_end_index = -1

        self.freq = 1  # �����������г��ֵĴ���
        self.need_remove = False  # �����������嶼������
        self.there_remove = False  # �����������о�����Ҫȥ��

    def __eq__(self, other):
        if type(other) is not NovelParagraph:
            return False

        if other.fmt_content == self.fmt_content:
            return True
        else:
            return False


class NovelSentence(object):
    """
        ����ȥ���У�һ��С˵���ӵ���Ϣ
    """

    def __init__(self, raw_content='', fmt_content='', para_index=0, before_word_sum=0):
        """
        һ�������������ĺ��֡���ĸ������

        ��������������ɣ������ĺ��֡���ĸ�����֣��Լ�������еķǺ��֡���ĸ������
        """
        self.raw_content = raw_content  # ����ԭ���о��ӵ����ݣ����������ķ��š�
        self.fmt_content = fmt_content  # ��raw_content�е�����ȫ��ת��ǣ���ĸȫ��ת��ǣ���ȫ����Сд
        self.after_punctuation = ''  # ���Ӻ�����б�����
        self.para_index = para_index  # �������ڶ���ı��
        self.before_word_sum = before_word_sum  # ����֮ǰ������ĸ�����֡����ֵĸ���

        # ��������Ҫ������½��г��ֵĴ���
        self.freq = 1

        self.there_remove = False  # ΪTrue��ʾ���ӿ��ܰ�������
        self.need_remove = False  # ΪTrue��ʾ����������
        self.need_replace = False  # �����ǰ���ӵ�������Ҫ���滻�������е����ݶ���fmt_content�У�����������

    def __eq__(self, other):
        if type(other) is not NovelSentence:
            return False

        if other.fmt_content == self.fmt_content:
            return True
        else:
            return False


if __name__ == '__main__':
    here()







