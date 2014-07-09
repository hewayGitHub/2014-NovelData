#!/usr/bin/env python
# -*- coding:GBK -*-
import codecs
from snownlp import sentiment

__author__ = 'hewei13'
__date__ = '2014-06-20 15:42'

from basic.NovelStructure import *
from public.BasicStringMethod import *
from novel.cluster.NovelCleanModule import *
from novel.chapter.ChapterHtmlFilter import *
import logging
import re

debug = False
cur_delimiter = str(chr(1))  # �洢�ļ��ķָ���

number_char_list = [
    u'0', u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9',
    u'��', u'һ', u'��', u'��', u'��', u'��', u'��', u'��', u'��', u'��', u'ʮ', u'��', u'ǧ'
]

sentiment.load('data/impurity_classifier')

def number_char_format(raw_chapter_title):
    """
    ���½ڱ����е�����������0���棬���ڽ��бȽ�
    """
    fmt_chapter_title = u''
    flag = True
    for char in raw_chapter_title:
        if char not in number_char_list:
            fmt_chapter_title += char
            flag = True
        else:
            if flag:
                fmt_chapter_title += u'0'
            flag = False
    return fmt_chapter_title


def is_same_kind(char_a, char_b):
    """
    �ж������ַ��Ƿ�Ϊ���֡���ĸ���ߺ���
    :param char_a:
    :param char_b:
    :return:
    """
    if char_a == u'' or char_b == u'':
        return True

    return (is_chinese(char_a) and is_chinese(char_b)) \
           or (is_alphabet(char_a) and is_alphabet(char_b)) \
           or (is_number(char_a) and is_number(char_b))


class ChapterContentFilter(object):
    """
    ����վ�㼶������ʣ��Լ��������������
    """
    __metaclass__ = Singleton

    def __init__(self):
        """
        ��ʼ�����������������ʽ
        """
        self.logger = logging.getLogger('novel.chapter.html')
        self.err = logging.getLogger('err.chapter.html')

        self.title_prefix_pattern = re.compile(ur'��?0[��|��|��]')

        # ��ʼ��������
        # �����������磧��������������������������������������������!��#"%$'&)(+*-,/.���ۡ���;:=<?>@����������[]\_^`�ࣤ�ݡ��ܣ���{��}|~
        punctuation_list = u'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        for p in punctuation_list:
            punctuation_list += unichr(ord(p) + 0xfee0)
        punctuation_list += u'�����������������������������������������ܣ�����������������������������'
        #punctuation_list += u'����������������������{}������������������%��'
        self.punctuation_set = set(punctuation_list)

        self.classifier = sentiment.classifier

    def get_paras(self, raw_chapter_content, site_id, chapter_title):
        """
        ���ض����list
        1���ȹ��˺ʹ����½������е�html��ǩ��
        2��Ȼ�����ÿһ�Σ�����վ�㼶��͹�������ʣ���Ҫ����ַ����βͨ������ֵ����ʾ�

        ע��:ȫ��Ϊunicode
        :param raw_chapter_content:
        :return:
        """
        # �ȹ��˺ʹ����½������е�html��ǩ��
        chapter_html_filter = ChapterHtmlFilter()
        fmt_chapter_content = chapter_html_filter.chapter_html_filter(raw_chapter_content)

        p_tag = u'<p style="text-indent:2em;">'
        back_p_tag = u'</p>'
        p_len = len(p_tag)
        back_p_len = len(back_p_tag)

        para_list = []
        valid_para_count = 0  # ��Щ�����ڹ���վ�㼶��͹��������ʱ��ɾ���ˣ��������������������ǡ��Ա�֮����ݶ���������
        para_index = 0  # ��Ӧ�����б������
        cur_index = 0
        before_word_sum = 0  # ��ǰ����֮ǰ�����ַ�����Ŀ
        while cur_index < len(fmt_chapter_content):
            p_index = fmt_chapter_content.find(p_tag, cur_index)
            if p_index < 0:
                self.err.error('site_id:{0} content:{1} content not be surrounded by <p>'.format(
                    site_id, fmt_chapter_content[cur_index:].encode('gbk', 'ignore')))
                para_start = cur_index
            else:
                para_start = p_index + p_len

            back_p_index = fmt_chapter_content.find(back_p_tag, para_start)
            if back_p_index < 0:
                self.err.error('site_id:{0} content:{1} <p> is not closed'.format(
                    site_id, fmt_chapter_content[p_index:].encode('gbk', 'ignore')))
                para_end = len(fmt_chapter_content)
                back_p_index = para_end - back_p_len  # ���Ҳ���</p>ʱ�������cur_index��ֵΪback_p_index + back_p_len
            else:
                para_end = back_p_index

            raw_para_content = fmt_chapter_content[para_start:para_end]

            #�Զ������վ�㼶�𡢹�����������
            fmt_para_content = self.common_filter(raw_para_content, site_id, chapter_title)
            if len(fmt_para_content) == 0:  # ��ǰ�½ڱ����˵���
                para = NovelParagraph(raw_content=raw_para_content, fmt_content=u'',
                                      para_index=para_index, before_word_sum=before_word_sum)
                para.need_remove = True
            else:
                para = NovelParagraph(raw_content=raw_para_content, fmt_content=fmt_para_content,
                                      para_index=para_index, before_word_sum=before_word_sum)

                valid_para_count += 1
                before_word_sum += para_end - para_start

            para_index += 1
            para_list.append(para)
            cur_index = back_p_index + back_p_len

        return fmt_chapter_content, para_list, valid_para_count

    def common_filter(self, raw_content, site_id, chapter_title):
        """
        ����վ�㼶�������������ʣ��������ַ���ƥ��ȥ�����������


        �˴�ȥ�ӵ�Ŀ���ǣ�
            * ��������к�ѡ���Ĵ���3����ô��������ֻ������common_filter
            * ��Ϊ���������ʾ��й��ԣ����������ĵ�ǰ���κ�󼸶Σ�����һЩ���ʾ��þ��Ӷ���ʱ��Ƶ�β��������������ʵ�����������www��http����ʹ�÷��ʱ�վ
            * ����һЩ��������ʣ��������ַ�����ȫƥ���ǿ����ȥ�����������һЩ�޷������bad case������ӹ���
            * ע�⣺����ʱҪ˼���Ƿ��Ӱ��֮��������;��Ӷ���ȡ�



        ������
        1.����������ַ������ַ�滻�ɿո񣬱�֤�־䲻�ᱻӰ�죬���Ҳ���Ӱ���������ĵ���ʾ��
        2.���˹�������ͨ���ܽ�������ͨ���Ĺ����Ӿ䣬ͨ���ַ���ƥ����й���
        3.����һЩ��������ʣ����������case
        4,�Զ��׶�β�����ж�
        ע�⣺
        1��Ҫ��������ǰ��ı����š���Ϊ�����Ű����ܶ�����ϲ����ڵ��ַ���̫���ڸ��ӣ����Խ��������滻Ϊվ���id
        :return:
        """
        return raw_content

        #�����е���ĸ������ת��Ϊ���
        raw_content = ''.join((is_number(char) or is_alphabet(char)) and Q2B(char) or char for char in raw_content)

        #������ַ�����ܹ��˵���ȷ�����ģ�����ֻ���ù���֤���˵���ȷ��
        # 1����www��http��wap��ͷ���������з��š����֡���ĸ
        # 2����net��com��me�Ƚ�β�ģ��������з��š����֡���ĸ
        # 3������վ������ֵģ������ܿ������е����
        # ע�⣺
        # ���֡���ĸ�ͷ��š��ո� [\u0021-\u007e\uff01-\uff5e\s]
        before_punctuation = u'''�����������磧��������������������������������������������!��#"%$'&)(+*-,/.���ۡ���;:=<?>@����������[]\_^`�ࣤ�ݡ��ܣ���{��}|~'''
        after_punctuation = u'''�����������磧��������������������������������������������!��#"%$'&)(+*-,/.���ۡ���;:=<?>@����������[]\_^`�ࣤ�ݡ��ܣ���{��}|~'''
        url_pattern = re.compile(r'(http|www|wap)[a-zA-Z0-9\s]*', re.U)
        fmt_content = raw_content

        return fmt_content

    def is_chapter_header(self, para, chapter_title):
        """
        ���ĳһ���Ƿ����½ڱ���

        ȫ��ת��ǣ��������ġ���ĸ�����֣�Ȼ�󣬽�������������0���棬���ڱȽ�
        :param para:
        :return:
        """
        para = string_Q2B(para)
        para = string_filter(para)
        para = number_char_format(para)

        chapter_title = string_Q2B(chapter_title)
        chapter_title = string_filter(chapter_title)
        chapter_title = number_char_format(chapter_title)

        if len(para) > len(chapter_title) * 2:
            return False

        para = self.title_prefix_pattern.sub('', para)
        chapter_title = self.title_prefix_pattern.sub('', chapter_title)

        if para == chapter_title:
            return True

        return string_similarity(para, chapter_title) > 0.8

    def get_sentences(self, paras):
        """
        ���½ڵĶ����б�ת��Ϊ�����б�
        :param paras:
        :return:
        """
        sentences = []

        cur_before_word_sum = 0
        for para in paras:
            if para.need_remove:
                continue

            para_sentences, cur_before_word_sum = \
                self.cut_into_sentences(para.fmt_content, para.para_index, cur_before_word_sum)
            para.sentence_start_index = len(sentences)
            para.sentence_end_index = len(sentences) + len(para_sentences)

            sentences.extend(para_sentences)

        return sentences

    def cut_into_sentences(self, chapter_content, para_index, before_word_sum):
        """
        �������ĺ��֡���ĸ��������Ϊһ�����ӣ����ӵ����ݽṹ��basic.NovelStructure.NovelSentence

        ����raw_content������ӵĳ���������֮���ԭ�ģ�
        fmt_contentֻ���������еĺ��֡���ĸ�����֣�
        after_punctuation�Ǿ��Ӻ����еı�����

        �����зֵĲ����ǣ�
        1�������������еķ����Լ��ո���Ϊ�����зֵı�׼���Լ������ʺ��½����ݱ��ֵ�һ�����ӵ����

        ע�⣺
        1�������ַ���ȫ��ת��ǣ����ڶ���ʱ�ıȽϺ��ж��Ƿ�Ϊ��ĸ�����ֺ����ġ�
        :param before_word_sum:��ǰ�½�֮ǰ�ĺ��֡����֡���ĸ���ۻ�����
        :return: ���ؾ����б��Լ�����֮ǰ�����������к��֡����֡���ĸ���ۻ�����
        """
        sentences = []

        start = 0  # ��ʶ���ӵ���ʼ
        cur_index = 0  # ָ����һ��δ�����ַ�����
        before_word_sum = before_word_sum
        fmt_content = u''  # ֻ�������֡���ĸ������
        while True:
            if cur_index >= len(chapter_content):
                break

            char = chapter_content[cur_index]
            if is_number(char):  # ����ȫ��ת���
                char = Q2B(char)
                fmt_content += char
                cur_index += 1
            elif is_alphabet(char):  # ��ĸȫ��ת��ǣ�����ȫת��ΪСд
                char = Q2B(char)
                char = char.lower()
                fmt_content += char
                cur_index += 1
            elif is_chinese(char):
                fmt_content += char
                cur_index += 1
            else:  # ���֡���ĸ������������ַ���Ϊ���ӵķָ���
                temp_sentence = NovelSentence(raw_content=chapter_content[start:cur_index], fmt_content=fmt_content,
                                              para_index=para_index, before_word_sum=before_word_sum)

                #���Ҿ��Ӻ����еı�����
                temp_sentence.after_punctuation += char
                for i in xrange(cur_index + 1, len(chapter_content)):
                    if chapter_content[i].isspace():  # ���Ա�����֮��Ŀո�
                        cur_index += 1
                        continue
                    elif not is_legal(chapter_content[i]):
                        temp_sentence.after_punctuation += chapter_content[i]
                        continue
                    else:
                        break
                cur_index += len(temp_sentence.after_punctuation)  # ָ����֮����һ���ַ�

                # ���ζ�û����ĸ�����֡����ֻ���һ�εĿ�ͷ�б����ŵ������Ϊ�˱��ھ��Ӷ��룬��������������Ϊ��������
                if len(fmt_content) == 0:
                    temp_sentence.fmt_content = string_Q2B(temp_sentence.after_punctuation)
                    temp_sentence.raw_content = temp_sentence.after_punctuation
                    temp_sentence.after_punctuation = u''

                sentences.append(temp_sentence)
                before_word_sum += len(fmt_content)
                start = cur_index
                fmt_content = u''

        #��������ĩβû�з�����Ϊ���ӽ���ʱ
        if start != cur_index:
            temp_sentence = NovelSentence(raw_content=chapter_content[start:cur_index], fmt_content=fmt_content,
                                          para_index=para_index, before_word_sum=before_word_sum)

            sentences.append(temp_sentence)
            before_word_sum += len(fmt_content)

        return sentences, before_word_sum

    def exact_align_paras(self, selected_chapter_index, candidate_chapter_list):
        """
        ��������bug ˼·ͬ���Ӷ��룬������޸ĸ��¡�
        �����������ĺ������������ģ���Ҫ���ض���ľ���dict

        ����ľ���dict����chapter_indexΪkey�ģ�listΪvalue��list������������ÿ���ں�ѡ�����ж�Ӧ���ӵ�sentence_index��
        ���Ϊ�ҵ�ƥ�䣬��Ӧ��ֵΪNone

        ͬʱ�������ľ��ӵ�freq�����£������м���ƥ��
        :param need_align_sentences:
        :param selected_chapter_index:
        :return:
        """
        selected_chapter = candidate_chapter_list[selected_chapter_index]

        para_align_dict = {}
        for chapter_index in xrange(0, len(candidate_chapter_list)):
            if chapter_index == selected_chapter_index:
                continue

            para_align_dict.setdefault(chapter_index, [])

        #����������������Ƿ��ж����ظ�����
        for selected_para_index, selected_para in enumerate(selected_chapter.paragraph_list):
            if selected_para.need_remove:
                continue

            selected_para.there_dup = False

            for other_index, other_para in enumerate(selected_chapter.paragraph_list):
                if other_index == selected_para_index:
                    continue
                if other_para.fmt_content == selected_para.fmt_content:
                    selected_para.there_dup = True
                    break

        #ͳ�����ź�ѡ�и�����������������ѡ�ж�Ӧ�Ķ����������ں�ѡ���ĵ�ȫ���в��ң������ж��Ƿ��ظ�����
        for selected_para_index, selected_para in enumerate(selected_chapter.paragraph_list):
            for chapter_index in para_align_dict:
                para_list = candidate_chapter_list[chapter_index]

                para_align_dict[chapter_index].append([])
                cur_start = 0
                while True:
                    align_index = -1
                    try:
                        align_index = para_list.index(selected_para, cur_start)
                    except ValueError:
                        pass

                    if align_index >= 0:
                        para_align_dict[chapter_index][selected_para_index].append(align_index)
                    else:
                        break

                    cur_start = align_index + 1

                if len(para_align_dict[chapter_index][selected_para_index]) > 0:
                    selected_para.freq += 1
                    if len(para_align_dict[chapter_index][selected_para_index]) > 1:
                        selected_para.there_dup = True

        #��Щ������3����ѡ�У��Ҳ������ظ��Ķ��������Ϊ����ȫƥ���
        exact_match_list = []
        for selected_para_index, selected_para in enumerate(selected_chapter.paragraph_list):
            if selected_para.freq >= 3 and not selected_para.there_dup:
                exact_match_list.append(selected_para_index)
        self.logger.info('exact match paragraph index:{0}'.format(exact_match_list))

        #��ʼ�����½ڵĲ�����ʼλ��
        align_start_sentence_index = {}
        align_end_sentence_index = {}
        for chapter_index in para_align_dict:
            align_start_sentence_index[chapter_index] = 0
            if len(exact_match_list) == 0:
                align_end_sentence_index[chapter_index] = len(candidate_chapter_list[chapter_index].paragraph_list)
            else:
                for match_para_index in exact_match_list:
                    if len(para_align_dict[chapter_index][match_para_index]) != 0:
                        align_end_sentence_index[chapter_index] = para_align_dict[chapter_index][match_para_index][0]
                        break
                    else:
                        align_end_sentence_index[chapter_index] = len(candidate_chapter_list[chapter_index].paragraph_list)

        #����û����ȫƥ��Ķ��䣬����ǰ��������ȫƥ��Ķ���ķ�Χ�ڲ����Ƿ����ƥ��
        for selected_para_index, selected_para in enumerate(selected_chapter.paragraph_list):
            #������ȫƥ��ģ����¶�Ӧ�½ں�ѡ����ʼindex
            if selected_para_index in exact_match_list:
                before_match_index = exact_match_list.index(selected_para_index)
                for chapter_index in para_align_dict:
                    #�������ֵ��ֵ��listת��Ϊ����ֵ
                    if len(para_align_dict[chapter_index][selected_para_index]) != 0:
                        align_start_sentence_index[chapter_index] = para_align_dict[chapter_index][selected_para_index][0] + 1

                    if before_match_index == len(exact_match_list) - 1:
                        align_end_sentence_index[chapter_index] = len(candidate_chapter_list[chapter_index].paragraph_list)
                    else:
                        if len(para_align_dict[chapter_index][exact_match_list[before_match_index + 1]]) != 0:
                            align_end_sentence_index[chapter_index] = para_align_dict[chapter_index][exact_match_list[before_match_index + 1]][0]
                        else:
                            align_end_sentence_index[chapter_index] = len(candidate_chapter_list[chapter_index].paragraph_list)
                continue

            #����δ��ȫƥ��ģ��������ƥ�䣬�������Щ��start��end��Χ��
            for chapter_index in para_align_dict:
                #δ�����ź�ѡ�����л��������κκ�ѡ�������ظ��������䲻��Ҫ�ٴβ���
                if not selected_para.there_dup:
                    if len(para_align_dict[chapter_index][selected_para_index]) == 0:
                        para_align_dict[chapter_index][selected_para_index] = None
                    else:
                        if align_start_sentence_index[chapter_index] <= para_align_dict[chapter_index][selected_para_index][0] < align_end_sentence_index[chapter_index]:
                            para_align_dict[chapter_index][selected_para_index] = para_align_dict[chapter_index][selected_para_index][0]
                            align_start_sentence_index[chapter_index] = para_align_dict[chapter_index][selected_para_index] + 1
                        else:
                            para_align_dict[chapter_index][selected_para_index] = None
                            selected_para.freq -= 1
                else:
                    if len(para_align_dict[chapter_index][selected_para_index]) == 0:
                        para_align_dict[chapter_index][selected_para_index] = None
                    else:
                        exists_count = 0
                        exists_index = 0
                        #print (align_start_sentence_index[chapter_index], align_end_sentence_index[chapter_index])
                        for temp_index in xrange(align_start_sentence_index[chapter_index], align_end_sentence_index[chapter_index]):
                            if temp_index in para_align_dict[chapter_index][selected_para_index]:
                                exists_count += 1
                                exists_index = temp_index
                        if exists_count != 1:
                            para_align_dict[chapter_index][selected_para_index] = None
                            selected_para.freq -= 1
                        else:
                            para_align_dict[chapter_index][selected_para_index] = exists_index

        return para_align_dict

    def align_paras(self, selected_chapter_index, candidate_chapter_list):
        """
        �����������ĺ������������ģ���Ҫ���ض���Ķ���dict

        ����Ķ���dict����chapter_indexΪkey�ģ�listΪvalue��list������������ÿ���ں�ѡ�����ж�Ӧ�����para_index��
        ���δ�ҵ�ƥ�䣬��Ӧ��ֵΪNone

        ͬʱ�������ĵ�freq�����£������м���ƥ��
        :param selected_chapter_index:
        :param candidate_chapter_list:
        :return: �������Ĵʵ�
        """
        selected_chapter = candidate_chapter_list[selected_chapter_index]

        para_align_dict = {}  # {chapter_index: list of para_index, ...}
        align_cur_para_index = {}  # ���������������ѡ���ĵ�ǰƥ�䵽�Ķ�������
        for chapter_index in xrange(0, len(candidate_chapter_list)):
            if chapter_index == selected_chapter_index:
                continue

            para_align_dict.setdefault(chapter_index, [])
            align_cur_para_index.setdefault(chapter_index, 0)

        #ͳ������������ÿһ����������ѡ���������ֵ�Ƶ��
        for selected_para in selected_chapter.paragraph_list:
            if selected_para.need_remove:
                continue

            for chapter_index, chapter in enumerate(candidate_chapter_list):
                if chapter_index == selected_chapter_index:
                    continue

                align_index = self.find_align_para(selected_para, chapter.paragraph_list,
                                                   align_cur_para_index[chapter_index])
                if align_index >= 0:
                    selected_para.freq += 1
                    para_align_dict[chapter_index].append(align_index)
                    align_cur_para_index[chapter_index] = align_index + 1
                else:
                    para_align_dict[chapter_index].append(None)

        return para_align_dict

    def find_align_para(self, selected_para, paragraph_list, cur_para_index):
        """
        �ж϶����б����Ƿ��к͸ö���ƥ��Ķ��䣬����ƥ���para_index����ƥ�䷵��-1
        ��cur_para_index��ʼ���ң�paragraph_list���Ƿ��к�selected_para������ȫ��ͬ�Ķ��䣬����Ҫ��֤�����ڸ�����

        �ظ�������ֵĸ��ʺ�С��ͬʱcur_para_index֮ǰ���Ѿ�ƥ���ˣ������ظ����䣬��������һ��ǡ��ȱʧ�ĸ��ʺ�С��
        ͬʱ��Ϊ���Է���������С�����¼������ұ���ÿ�ζ���Ҫ�����ж�����бȽϣ��������para_index����6��������֮ǰ�����6����������
        :param selected_para:
        :param paragraph_list:
        :param cur_para_index:
        :return:
        """
        align_index = -1
        for index in xrange(cur_para_index, len(paragraph_list)):
            cur_para = paragraph_list[index]

            if cur_para.need_remove:  #����basic_chapter_filter�б����˵��Ķ��䣬������벻��������
                continue

            # ��������ÿ�ζ���Ҫ�����ж�����бȽϣ�ͬʱ��һ���̶��ϱ����ظ��ε����
            if abs(cur_para.para_index - selected_para.para_index) > 6:
                break

            if cur_para.fmt_content == selected_para.fmt_content:
                align_index = index

        return align_index

    def check_para(self, selected_para_index, selected_chapter_index, para_align_dict, candidate_chapter_list):
        """
        �����������ζ������ʣ�����һ����Ϊ���ʣ����һ����Ϊ���ʣ����ؿ�����Ҫ���ж���ȥ�ӵľ���

        Ѱ�����������Ƶ�γ����ܺ�ѡ1/2�Ķ���A��B��
        ���������ѡ��A��B��Ӧ����֮�䲻�����������䣬��ΪA��B֮�����еĶ��䶼���������ʡ�
        ����A��B֮��Ķ�����ܰ������ʣ��������зֳɾ��ӣ������ӵĶ��롣
        :param selected_para_index:
        :param selected_chapter_index:
        :param para_align_dict:
        :param candidate_chapter_list:
        :return: ������Ҫ���ж���ȥ�ӵľ��Ӻ���ʼ���������
        """
        selected_chapter = candidate_chapter_list[selected_chapter_index]

        #�ҳ���ǰ��ǰ������ڳ���һ���ѡ�еĶ��䣬��ȡ����ƥ��Ķ���index�����⣬there_removeΪTrue��ʾĳ�������ѱ�����
        before_index = -1
        after_index = len(selected_chapter.paragraph_list)
        for para_index in xrange(selected_para_index - 1, -1, -1):
            if selected_chapter.paragraph_list[para_index].freq * 2 > len(candidate_chapter_list) \
                    or selected_chapter.paragraph_list[para_index].there_remove:
                before_index = para_index
                break
        for para_index in xrange(selected_para_index + 1, len(selected_chapter.paragraph_list)):
            if selected_chapter.paragraph_list[para_index].freq * 2 > len(candidate_chapter_list) \
                    or selected_chapter.paragraph_list[para_index].there_remove:
                after_index = para_index
                break

        #��������ǰ����ƥ��ĺ�ѡ�½ڣ�������Ƕ����ڣ���ʾ���ζ������ʣ�����ȡ����֮������ݣ����з־�Ƚ�
        need_align_sentences = {}
        match_count = 0
        remove_count = 0
        for chapter_index, chapter in enumerate(candidate_chapter_list):
            if chapter_index == selected_chapter_index:
                continue

            if before_index == -1:  # �ڵ�ǰ����֮ǰδ�ҵ�freq�����ܺ�ѡ1/2�Ķ���
                temp_before = -1
            else:
                temp_before = para_align_dict[chapter_index][before_index]

                if temp_before is None:  # �����ڵ�chapter_index��û����ȫƥ����½�
                    continue

            if after_index == len(selected_chapter.paragraph_list):  # �ڵ�ǰ����֮��δ�ҵ�freq�����ܺ�ѡ1/2�Ķ���
                temp_after = len(chapter.paragraph_list)
            else:
                temp_after = para_align_dict[chapter_index][after_index]

                if temp_after is None:  # �����ڵ�chapter_index��û����ȫƥ����½�
                    continue

            if temp_before + 1 == temp_after:
                match_count += 1
                remove_count += 1
            elif temp_before >= temp_after:
                continue
            else:
                match_count += 1
                need_align_sentences[chapter_index] = self.get_sentences(
                    chapter.paragraph_list[temp_before + 1:temp_after])

        self.logger.info('check_para sign_of_remove/sign_of_match is {0}/{1}, num of candidate chapters:{2}'.format(
            remove_count, match_count, len(candidate_chapter_list)))
        if match_count == 0:  # �����������ѡδ�ҵ�ǰ��ƥ��ģ���ôֻ�ܶ����еľ�����������
            self.logger.info('paragraph no match has been found')
            before_index = -1
            after_index = len(selected_chapter.paragraph_list)
            for chapter_index, chapter in enumerate(candidate_chapter_list):
                need_align_sentences[chapter_index] = self.get_sentences(chapter.paragraph_list)
        elif remove_count >= 2:  # ��Ϊ����ȱʧ��������ټ������������������ѡ�иöβ����ڣ���ô����п��������ʡ����ͨ���������ٴ��жϡ�
            need_align_sentences = {}
        else:  # ��Ҫ�Զ�����о��Ӷ��룬�������¶�Ӧ�ľ�����ӵ�need_align_sentences��
            need_align_sentences[selected_chapter_index] = self.get_sentences(
                selected_chapter.paragraph_list[before_index + 1:after_index])

        return need_align_sentences, before_index + 1, after_index

    def align_sentences(self, selected_chapter_index, need_align_sentences):
        """
        �����������ĺ������������ģ���Ҫ���ض���ľ���dict

        ����ľ���dict����chapter_indexΪkey�ģ�listΪvalue��list������������ÿ���ں�ѡ�����ж�Ӧ���ӵ�sentence_index��
        ���Ϊ�ҵ�ƥ�䣬��Ӧ��ֵΪNone

        ͬʱ�������ľ��ӵ�freq�����£������м���ƥ��
        :param need_align_sentences:
        :param selected_chapter_index:
        :return:
        """
        selected_sentence_list = need_align_sentences[selected_chapter_index]

        # ��ʼ�����Ӷ����ֵ䣬ÿ��chapter_index��Ӧһ���б���ʼ����������������Ҫ�������������None
        sentence_align_dict = {}
        init_list = [None for i in xrange(0, len(selected_sentence_list))]
        for chapter_index in need_align_sentences:
            if chapter_index == selected_chapter_index:
                continue

            sentence_align_dict[chapter_index] = init_list

        #����������������Ƿ��о����ظ�����
        for selected_sentence_index, selected_sentence in enumerate(selected_sentence_list):
            selected_sentence.there_dup = False

            # �˶��߼�������־䲿�� self.cut_into_sentences
            # if selected_sentence.fmt_content == '':  # ���ζ�û����ĸ�����֡����ֻ���һ�εĿ�ͷ�б����ŵ������������Ϊ�����е���ȫƥ��
            #     selected_sentence.fmt_content = selected_sentence.after_punctuation
            #     selected_sentence.raw_content = selected_sentence.after_punctuation
            #     selected_sentence.after_punctuation = u''

            for other_index, other_sentence in enumerate(selected_sentence_list):
                if other_index == selected_sentence_index:
                    continue
                if other_sentence.fmt_content == selected_sentence.fmt_content:
                    selected_sentence.there_dup = True
                    break

        #����������ÿ�����Ӽ�����Ƿ���ĳ����ѡ�����г��ֶ�Σ�����У���Ƶ��Ϊ1�����û�У�ͳ������ֵ�Ƶ��
        for selected_sentence_index, selected_sentence in enumerate(selected_sentence_list):
            for chapter_index in sentence_align_dict:
                sentence_list = need_align_sentences[chapter_index]

                cur_start = 0
                while True:
                    align_index = -1
                    try:
                        align_index = sentence_list.index(selected_sentence, cur_start)
                    except ValueError:
                        pass

                    if align_index >= 0:
                        if cur_start == 0:
                            sentence_align_dict[chapter_index][selected_sentence_index] = align_index
                        else:
                            selected_sentence.there_dup = True
                            break
                    else:
                        break

                    cur_start = align_index + 1

                if not selected_sentence.there_dup:
                    selected_sentence.freq += 1
                else:
                    selected_sentence.freq = 1
                    break

        #��Щ���������к�ѡ�У��Ҳ������ظ��ľ��ӿ�����Ϊ����ȫƥ���
        exact_match_list = []
        for selected_sentence_index, selected_sentence in enumerate(selected_sentence_list):
            if selected_sentence.freq == len(need_align_sentences) and not selected_sentence.there_dup:
                exact_match_list.append(selected_sentence_index)
        self.logger.info('exact match sentence index:{0}'.format(exact_match_list))

        #��ʼ�����½ڵĲ�����ʼλ��
        align_start_sentence_index = {}
        align_end_sentence_index = {}
        for chapter_index in sentence_align_dict:
            align_start_sentence_index[chapter_index] = 0
            if len(exact_match_list) == 0:
                align_end_sentence_index[chapter_index] = len(need_align_sentences[chapter_index])
            else:
                align_end_sentence_index[chapter_index] = sentence_align_dict[chapter_index][exact_match_list[0]]

        #����û����ȫƥ��ľ��ӣ�����ǰ��������ȫƥ��ľ��ӵķ�Χ�ڲ����Ƿ����ƥ��
        for selected_sentence_index, selected_sentence in enumerate(selected_sentence_list):
            #������ȫƥ��ģ����²�����һ�����ӵ���ֹ��Χ
            if selected_sentence_index in exact_match_list:
                before_match_index = exact_match_list.index(selected_sentence_index)
                for chapter_index in sentence_align_dict:
                    align_start_sentence_index[chapter_index] = sentence_align_dict[chapter_index][selected_sentence_index] + 1
                    if before_match_index == len(exact_match_list) - 1:
                        align_end_sentence_index[chapter_index] = len(need_align_sentences[chapter_index])
                    else:
                        align_end_sentence_index[chapter_index] = sentence_align_dict[chapter_index][exact_match_list[before_match_index + 1]]

                continue

            #����δ��ȫƥ��ģ��������ƥ�䣬������Ƿ�����ȫƥ���Ӧ��������Χ��
            for chapter_index in sentence_align_dict:
                #����δ�ظ������ڵ�ǰ�½�����ƥ�䣬ֻ��Ҫ��⵱ǰ�������Ƿ�����ȫƥ���Ӧ��������Χ�ڼ���
                if not selected_sentence.there_dup:
                    if sentence_align_dict[chapter_index][selected_sentence_index] is not None:
                        # ����ڷ�Χ�ڣ��޸Ŀ�ʼ��ΧΪ��Ӧ����+1.���򣬽����ӵ�Ƶ�μ�1�����ҽ����Ӧ��������ֵΪNone
                        if align_start_sentence_index[chapter_index] <= sentence_align_dict[chapter_index][selected_sentence_index] < align_end_sentence_index[chapter_index]:
                            align_start_sentence_index[chapter_index] = sentence_align_dict[chapter_index][selected_sentence_index] + 1
                        else:
                            sentence_align_dict[chapter_index][selected_sentence_index] = None
                            selected_sentence.freq -= 1
                else:
                    sentence_align_dict[chapter_index][selected_sentence_index] = None
                    # ����ʼ��Χ�ڲ��Ҹþ��ӣ�����������ظ�����Ϊ�ҵ�ƥ�䡣��������ظ�����Ϊû��ƥ�䡣
                    exists_count = 0
                    exists_index = 0
                    for between_index in xrange(align_start_sentence_index[chapter_index],
                                             align_end_sentence_index[chapter_index]):
                        if selected_sentence.fmt_content == need_align_sentences[chapter_index][between_index].fmt_content:
                            exists_count += 1
                            exists_index = between_index

                        if exists_count > 1:
                            break

                    if exists_count == 1:
                        sentence_align_dict[chapter_index][selected_sentence_index] = exists_index
                        selected_sentence.freq += 1

        return sentence_align_dict

    def check_sentence(self, selected_sentence_index, selected_chapter_index,
                       sentence_align_dict, need_align_sentences, sentence_freq_threshold):
        """
        �����������䶼�����ʣ�����һ����Ϊ���ʣ����һ����Ϊ���ʣ����ؿ�����Ҫ��һ��ȥ�ӵľ���

        ͨ������þ���ǰ��ľ��ӣ����һ����Χ��
        ����þ��ӵ�ǰ����������ڵģ���ô�þ���������ܶ������ʣ�ͨ����������һ�����࣬����ȥ����
        ������Ҫ�����ӷ��أ���һ���Ծ��ӽ���ȥ�ӡ�

        :param selected_sentence_index:
        :param selected_chapter_index:
        :param sentence_align_dict: ���Ӷ���Ľ����ÿ����ѡ�½ڶ�Ӧһ��list���洢selected��Ӧ���Ӷ�Ӧ������
        :param need_align_sentences: ���������ѡ�½�����������ľ���
        :param sentence_freq_threshold: freqС��sentence_freq_threshold�ľ�����Ҫ����Ƿ�Ϊ����
        :return:
        """
        selected_sentence_list = need_align_sentences[selected_chapter_index]

        #�ҳ���ǰ��ǰ�����ڽ���freq���ڵ���sentence_freq_threshold�ľ��ӣ���ȡ����ƥ���sentence_index
        before_index = -1
        after_index = len(selected_sentence_list)
        for sentence_index in xrange(selected_sentence_index - 1, -1, -1):
            if selected_sentence_list[sentence_index].freq >= sentence_freq_threshold:
                before_index = sentence_index
                break
        for sentence_index in xrange(selected_sentence_index + 1, len(selected_sentence_list)):
            if selected_sentence_list[sentence_index].freq >= sentence_freq_threshold:
                after_index = sentence_index
                break

        need_check_sentences = {}
        match_chapter_index = None
        match_before_index = None
        match_after_index = None
        match_count = 0
        remove_count = 0
        for chapter_index in sentence_align_dict:
            if before_index != -1:
                temp_before = sentence_align_dict[chapter_index][before_index]

                if temp_before is None:
                    continue
            else:
                temp_before = -1

            if after_index != len(selected_sentence_list):
                temp_after = sentence_align_dict[chapter_index][after_index]

                if temp_after is None:
                    continue
            else:
                temp_after = len(need_align_sentences[chapter_index])

            if temp_before + 1 == temp_after:
                remove_count += 1
                match_count += 1
                match_chapter_index = chapter_index
                match_before_index = temp_before
                match_after_index = temp_after
            elif temp_before >= temp_after:
                continue
            else:
                match_count += 1
                need_check_sentences[chapter_index] = need_align_sentences[chapter_index][temp_before + 1: temp_after]

        self.logger.info('check_sentence sign_of_remove/sign_of_match is {0}/{1}, num of align chapter:{2}'.format(
            remove_count, match_count, len(need_align_sentences)))
        if match_count == 0:
            self.logger.info('sentence no match has been found')
            need_check_sentences = need_align_sentences
            before_index = -1
            after_index = len(selected_sentence_list)
        elif remove_count * 2 > match_count:  # �����Ϊ���������ʣ�������ȫƥ����½ڵı���滻���������Բ��������ļ��
            if before_index != -1:
                #ǰһ���������ֻ���������ţ������ŵ�������fmt_content��
                if len(need_align_sentences[match_chapter_index][match_before_index].after_punctuation) == 0:
                    selected_sentence_list[before_index].fmt_content = need_align_sentences[match_chapter_index][match_before_index].fmt_content
                    selected_sentence_list[before_index].raw_content = need_align_sentences[match_chapter_index][match_before_index].raw_content
                else:
                    selected_sentence_list[before_index].after_punctuation = need_align_sentences[match_chapter_index][match_before_index].after_punctuation

            need_check_sentences = {}
        else:  # ���ӵ�һ����������
            need_check_sentences[selected_chapter_index] = selected_sentence_list[before_index + 1:after_index]

        return need_check_sentences, before_index + 1, after_index

    def remove_part_impurity(self, selected_chapter_index, need_check_sentences):
        """
        ������ʱδ����

        need_replace��ʶ�����ΪTrue������������ʱ���������������Ϊfmt_content���������raw_content+after_punctuation
        ���ԣ�������֮��ľ���Ҫ��need_replace��ΪTrue����������������д��fmt_content
        :param need_check_sentences:
        :return:
        """
        selected_sentence_list = need_check_sentences[selected_chapter_index]

        for sentence in selected_sentence_list:
            sentence.need_replace = False

        # ͳ�ƾ��ӵĸ������ַ����������������Լ����ģ�������㣩��Ȼ�����о��ӵ�������Ϊ�ա�����һ�����ӵ���������Ϊ�������ݵ�����
        selected_sen_num = len(selected_sentence_list)
        selected_word_count = 0
        selected_punc_count = 0
        selected_text = u''
        if selected_sen_num == 1:
            selected_word_count = len(selected_sentence_list[0].fmt_content)
            selected_text = selected_sentence_list[0].fmt_content + selected_sentence_list[0].after_punctuation

            selected_sentence_list[0].fmt_content = u''
            selected_sentence_list[0].after_punctuation = u''
        else:
            for sentence in selected_sentence_list:
                selected_word_count += len(sentence.fmt_content)
                selected_text += sentence.fmt_content + sentence.after_punctuation
                selected_punc_count += len(sentence.after_punctuation)

                sentence.fmt_content = u''
                sentence.after_punctuation = u''

            selected_punc_count -= len(selected_sentence_list[-1].after_punctuation)  # ���ñȽ����ı�����

        selected_sentence_list[0].fmt_content = selected_text  # ����there_removeΪTrue�ľ��ӣ������ݶ�ֱ�Ӷ�ȡfmt_content

        sen_num_dict = {}  # ���ӵĸ���
        word_count_dict = {}  # ���֡���ĸ�����ֵĸ���
        text_dict = {}
        clean_text_dict = {}  # ���о����еĺ��֡���ĸ������

        is_content_equal = True
        is_word_count_equal = True
        is_max_word_count = True
        max_word_chapter_index = selected_chapter_index
        min_word_chapter_index = selected_chapter_index

        is_max_punc_count = True
        max_punc_chapter_index = selected_chapter_index
        for chapter_index, sentence_list in need_check_sentences.itmes():
            if chapter_index == selected_chapter_index:
                continue

            temp_punc_count = 0  # �����ŵĸ���

            sen_num_dict[chapter_index] = len(sentence_list)
            if len(sentence_list) == 1:
                word_count_dict[chapter_index] = len(sentence_list[0].fmt_content)
                text_dict[chapter_index] = sentence_list[0].fmt_content + sentence_list[0].after_punctuation
            else:
                word_count_dict[chapter_index] = 0
                text_dict[chapter_index] = u''
                for sentence in sentence_list:
                    word_count_dict[chapter_index] += len(sentence.fmt_content)
                    temp_punc_count += len(sentence.after_punctuation)
                    text_dict[chapter_index] += sentence.fmt_content + sentence.after_punctuation
                temp_punc_count -= len(sentence_list[-1].after_punctuation)

            if text_dict[chapter_index] != selected_text:
                is_content_equal = False

            if word_count_dict[chapter_index] > selected_word_count:
                is_word_count_equal = False

                is_max_word_count = False
                max_word_chapter_index = chapter_index
            elif word_count_dict[chapter_index] < selected_word_count:
                is_word_count_equal = False

                min_word_chapter_index = chapter_index

            if temp_punc_count > selected_punc_count:
                is_max_punc_count = False
                max_punc_chapter_index = chapter_index

        text_dict[selected_chapter_index] = selected_text

        # 1, �����źͿո񣬵��·־䲻ͬ����ʱ����������ͬ�����Ǿ��Ӳ��ܶ��롣��ʱͨ�������б�������ȷ�ġ�
        # 2���и�������ʱ�����ĵĳ�����ͬ���޷��ж���һ�������������ã�����Ҳͬ����ѡ���������ġ�
        if is_content_equal or is_word_count_equal:
            selected_sentence_list[0].fmt_content = text_dict[max_punc_chapter_index]
            return

        # ���������������ʱ��������������а������ʣ����߽϶̵�����ȱ�����ݡ�
        # ��Ϊ����rankʱ��������ѡ�����ַ���ģ����ԣ�ͨ������£���ѡ�����ĵľ��������.
        # 3��ͨ���������ж�������Ƿ������ʣ�����ǣ��ж��Ƿ���ڰ�����ϵ���������ѡ��϶̵����ģ���������ڣ���Ϊ��Ϊ��������
        # 4, �����ľ��Ӳ������ʣ���ô�����ǽ϶̵�����ȱ�����ݣ����߽ϳ������İ���ƴ��.
        text_set = set(text_dict.values())

        word_set_dict = {}  # �ֵļ��ϣ�������ظ��ַ������������set�Ĵ�С��word_count���ܲ���ͬ
        for chapter_index, text in text_dict.items():
            word_set_dict[chapter_index] = set(string_filter(text))
        max_word_set = word_set_dict[max_word_chapter_index]

        if self.classifier.classify(clean_text_dict[max_word_chapter_index]) < 0.1:
            is_include = True
            for word_set in word_set_dict.values():
                if not len(max_word_set & word_set) * 2 > len(word_set):  # ����һ����ַ�����ͬ��
                    is_include = False
                    break

            if is_include:
                selected_sentence_list[0].fmt_content = text_dict[min_word_chapter_index]
            else:
                is_all_impurity = True
                for index, text in enumerate(clean_text_dict.values()):
                    if index == max_word_chapter_index:
                        continue

                    if self.classifier.classify(text) > 0.1:
                        is_all_impurity = False
                        break
                if is_all_impurity:
                    selected_sentence_list[0].need_remove = True
        else:
            #����Ƿ������ĸ�����������������תΪƴ��������Ƿ���ȣ������ȣ�ѡ�񲻰�����ĸ�ġ�����ֱ��ѡ����������
            selected_sentence_list[0].fmt_content = text_dict[max_word_chapter_index]

    def is_impurity(self, case_content):
        '''
        ͨ���������ж��Ƿ�Ϊ���ʡ����ڷ����������ܲ��ȶ�����Ҫ���һЩ����ʽ�����жϡ�

        ��ΪС˵���ĵ����ݱȽϸ��ӣ�û�к���Ĳ����ܹ�������Ҫ���ǵ����ġ����ԣ����������ܲ��ȶ���ĳЩ�������߾���һ���������ʵ������������������У���Ϊ�������ʡ�
        ��ˣ���������Ŀ�궨��Ϊ����Ϊ���Ӷ���ĸ�������ֵ��Ϊ0.1��������С��0.1��ʾ��Ϊ���ʣ��������ʵ��ٻ��ʴﵽ100%�������Ὣ�����ж�Ϊ�����ʡ�
        ���ԣ������²������ھ���δ�����ǰ����ʵʩ�ġ�

        * ���ڶ̾䣬������һ��������ͨ����Ϊ���������������ļ������ܰ������ʵľ�����Ϊһ�������÷������жϡ������������С��3�����ȫ�������ֻ�����ĸ��ֱ����Ϊ����
        * ������ĸ�����ֺͱ����ŵ������ж�Ϊ�������ж���������������ַ�����ֱ�ӵ������ʴ���
        * ��һЩ����ѵ������û�У�ͨ���������ʲ���ѵ������
        * �������µ��½ڱ���ȣ���Ҫ�����ѵ�����������˹����죬���е��º͵ڽڣ���Ϊ������ѵ����
        :return:
        '''
        return False

    def sentence_to_paragraph(self, paragraph_list, para_start_index, para_end_index, sentence_list):
        """

        ��ʱδ���������
        :param paragraph_list:
        :param para_start_index:
        :param para_end_index:
        :param sentence_list:
        :return:
        """
        for para_index in xrange(para_start_index, para_end_index):
            cur_para = paragraph_list[para_index]
            cur_para.fmt_content = u''
            for sentence_index in xrange(cur_para.sentence_start_index, cur_para.sentence_end_index):
                cur_sen = sentence_list[sentence_index]
                if cur_sen.need_remove:  # ��������������
                    # cur_para.fmt_content += u'<span style="display:none" class="is_impurity whole_sentence_remove">' + \
                    #                         cur_sen.raw_content + cur_sen.after_punctuation + u'</span>'
                    cur_para.fmt_content += u'<span class="whole_sentence_remove">���������� ' + \
                                            cur_sen.raw_content + cur_sen.after_punctuation + u'��</span>'

                elif not cur_sen.there_remove:  # ���ӵ�freq���ڵ���sentence_freq_threshold����������δ����Ķ�����
                    # cur_para.fmt_content += cur_sen.raw_content + cur_sen.after_punctuation
                    cur_para.fmt_content += u'��' + str(cur_sen.freq) + u'��' + \
                                            cur_sen.raw_content + cur_sen.after_punctuation
                else:  # ���ӵ�һ����������
                    if cur_sen.need_replace:
                        # cur_para.fmt_content += cur_sen.fmt_content
                        cur_para.fmt_content += u'<span class="part_sentence_remove"> ' + \
                                                u'��new ' + cur_sen.fmt_content + u' old ' \
                                                + cur_sen.raw_content + cur_sen.after_punctuation + u'��</span>'
                    else:
                        # cur_para.fmt_content += cur_sen.raw_content + cur_sen.after_punctuation
                        cur_para.fmt_content += u'<span class="not_handle_impurity">��δ�������� ' + \
                                                cur_sen.raw_content + cur_sen.after_punctuation + u'��</span>'

    def back_to_html(self, paragraph_list, site_id):
        """
        ��paras��ԭΪhtml����ʽ��para��para_indexΪ-1����ʾӦ�ñ�ɾ���Ķ��䡣sentence��need_removeΪtrue�ģ���ʾӦ�ñ�ɾ���ľ���
        :param paras:
        :return:
        """
        pure_chapter_content = u''
        p_tag = u'<p style="text-indent:2em;">'
        back_p_tag = u'</p>'

        for paragraph in paragraph_list:
            if paragraph.need_remove:
                if paragraph.there_remove:  # ��ʾ�ö��侭���������ȷ��Ϊ�������ʣ�ͨ����������һ����֤
                    if not self.is_impurity(string_filter(paragraph.fmt_content)):
                        self.logger.info('para_index:{0} is saved by the classifier'.format(paragraph.para_index))
                        pure_chapter_content += p_tag + paragraph.fmt_content + back_p_tag
                        continue

                # pure_chapter_content += u'<p style="text-indent:2em;" style="display:none" class="is_impurity whole_paragraph_impurity">' \
                #                        + paragraph.raw_content + u'</p>'
                pure_chapter_content += p_tag + u'���������� ' + paragraph.raw_content + u'��' + back_p_tag

                if len(paragraph.fmt_content) != 0:
                    with codecs.open('data/whole_para.csv', 'a', encoding='gbk', errors='ignore') as whole_impurity_file:
                        prob = self.classifier.classify(paragraph.fmt_content)
                        whole_impurity_file.write(
                            paragraph.fmt_content + ',' + str(site_id) + ',' + str(prob > 0.5 and 1 or 0) + ',' + str(prob) + '\n')
            else:
                pure_chapter_content += p_tag + paragraph.fmt_content + back_p_tag

        return pure_chapter_content
