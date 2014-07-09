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
cur_delimiter = str(chr(1))  # 存储文件的分隔符

number_char_list = [
    u'0', u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9',
    u'零', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九', u'十', u'百', u'千'
]

sentiment.load('data/impurity_classifier')

def number_char_format(raw_chapter_title):
    """
    将章节标题中的连续数字用0代替，便于进行比较
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
    判断两个字符是否都为数字、字母或者汉字
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
    过滤站点级别的杂质，以及其它共存的杂质
    """
    __metaclass__ = Singleton

    def __init__(self):
        """
        初始化过滤所需的正则表达式
        """
        self.logger = logging.getLogger('novel.chapter.html')
        self.err = logging.getLogger('err.chapter.html')

        self.title_prefix_pattern = re.compile(ur'第?0[章|回|节]')

        # 初始化标点符号
        # ！、＃＂％＄＇＆）（＋＊－，／．】【。—｜’‘；：＝＜？＞!＠#"%$'&)(+*-,/.“［·》;:=<?>@《～”｛×[]\_^`｀￥］…＼｝＿{＾}|~
        punctuation_list = u'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        for p in punctuation_list:
            punctuation_list += unichr(ord(p) + 0xfee0)
        punctuation_list += u'·～！＠＃￥％……＆×（）——＋－＝【】＼｛｝｜；：’‘“”，。、《》？'
        #punctuation_list += u'，。？《》；：”“’‘{}【】、——（）……%！'
        self.punctuation_set = set(punctuation_list)

        self.classifier = sentiment.classifier

    def get_paras(self, raw_chapter_content, site_id, chapter_title):
        """
        返回段落的list
        1，先过滤和处理章节正文中的html标签；
        2，然后针对每一段，过滤站点级别和共存的杂质，主要是网址、段尾通常会出现的杂质句

        注意:全部为unicode
        :param raw_chapter_content:
        :return:
        """
        # 先过滤和处理章节正文中的html标签；
        chapter_html_filter = ChapterHtmlFilter()
        fmt_chapter_content = chapter_html_filter.chapter_html_filter(raw_chapter_content)

        p_tag = u'<p style="text-indent:2em;">'
        back_p_tag = u'</p>'
        p_len = len(p_tag)
        back_p_len = len(back_p_tag)

        para_list = []
        valid_para_count = 0  # 有些段落在过滤站点级别和共存的杂质时被删除了，计算段落个数不考虑它们。以便之后根据段落数过滤
        para_index = 0  # 对应段落列表的索引
        cur_index = 0
        before_word_sum = 0  # 当前段落之前所有字符的数目
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
                back_p_index = para_end - back_p_len  # 当找不到</p>时，方便给cur_index赋值为back_p_index + back_p_len
            else:
                para_end = back_p_index

            raw_para_content = fmt_chapter_content[para_start:para_end]

            #对段落过滤站点级别、公共串等杂质
            fmt_para_content = self.common_filter(raw_para_content, site_id, chapter_title)
            if len(fmt_para_content) == 0:  # 当前章节被过滤掉了
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
        过滤站点级、公共串等杂质，另外用字符串匹配去除特殊的杂质


        此处去杂的目的是：
            * 如果最大簇中候选正文大于3，那么最优正文只进行了common_filter
            * 因为正文中杂质具有共性，尤其是正文的前几段后后几段，所以一些杂质句用句子对齐时，频次并不满足整句杂质的条件。例如www、http、请使用访问本站
            * 对于一些特殊的杂质，可以用字符串完全匹配等强规则，去除。尤其对于一些无法处理的bad case可以添加规则。
            * 注意：处理时要思考是否会影响之后段落对齐和句子对齐等。



        包括：
        1.过滤所有网址。将网址替换成空格，保证分句不会被影响，并且不会影响最终正文的显示。
        2.过滤公共串，通过总结杂质中通常的公共子句，通过字符串匹配进行过滤
        3.过滤一些特殊的杂质，处理特殊的case
        4,对段首段尾集中判断
        注意：
        1。要考虑杂质前后的标点符号。因为标点符号包括很多键盘上不存在的字符，太过于复杂，所以将公共串替换为站点的id
        :return:
        """
        return raw_content

        #将所有的字母和数字转化为半角
        raw_content = ''.join((is_number(char) or is_alphabet(char)) and Q2B(char) or char for char in raw_content)

        #过滤网址，不能过滤掉正确的正文，所以只能用规则保证过滤的正确性
        # 1，以www或http或wap开头，包含所有符号、数字、字母
        # 2，以net、com、me等结尾的，包含所有符号、数字、字母
        # 3，包含站点的名字的，尽可能考虑所有的情况
        # 注意：
        # 数字、字母和符号、空格 [\u0021-\u007e\uff01-\uff5e\s]
        before_punctuation = u'''！、＃＂％＄＇＆）（＋＊－，／．】【。—｜’‘；：＝＜？＞!＠#"%$'&)(+*-,/.“［·》;:=<?>@《～”｛×[]\_^`｀￥］…＼｝＿{＾}|~'''
        after_punctuation = u'''！、＃＂％＄＇＆）（＋＊－，／．】【。—｜’‘；：＝＜？＞!＠#"%$'&)(+*-,/.“［·》;:=<?>@《～”｛×[]\_^`｀￥］…＼｝＿{＾}|~'''
        url_pattern = re.compile(r'(http|www|wap)[a-zA-Z0-9\s]*', re.U)
        fmt_content = raw_content

        return fmt_content

    def is_chapter_header(self, para, chapter_title):
        """
        检测某一段是否是章节标题

        全角转半角，保留中文、字母和数字，然后，将连续的数字用0代替，便于比较
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
        将章节的段落列表转化为句子列表
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
        将连续的汉字、字母、数字作为一个句子，句子的数据结构见basic.NovelStructure.NovelSentence

        其中raw_content保存句子的除其后标点符号之外的原文，
        fmt_content只保留句子中的汉字、字母和数字，
        after_punctuation是句子后所有的标点符号

        句子切分的策略是，
        1，将键盘上所有的符号以及空格都作为句子切分的标准，以减少杂质和章节内容被分到一个句子的情况

        注意：
        1，对于字符先全角转半角，便于对齐时的比较和判断是否为字母、数字和中文。
        :param before_word_sum:当前章节之前的汉字、数字、字母的累积总数
        :return: 返回句子列表，以及本段之前包括本段所有汉字、数字、字母的累积总数
        """
        sentences = []

        start = 0  # 标识句子的起始
        cur_index = 0  # 指向下一个未检测的字符索引
        before_word_sum = before_word_sum
        fmt_content = u''  # 只保留汉字、字母和数字
        while True:
            if cur_index >= len(chapter_content):
                break

            char = chapter_content[cur_index]
            if is_number(char):  # 数字全角转半角
                char = Q2B(char)
                fmt_content += char
                cur_index += 1
            elif is_alphabet(char):  # 字母全角转半角，并且全转换为小写
                char = Q2B(char)
                char = char.lower()
                fmt_content += char
                cur_index += 1
            elif is_chinese(char):
                fmt_content += char
                cur_index += 1
            else:  # 汉字、字母和数字以外的字符作为句子的分隔符
                temp_sentence = NovelSentence(raw_content=chapter_content[start:cur_index], fmt_content=fmt_content,
                                              para_index=para_index, before_word_sum=before_word_sum)

                #查找句子后所有的标点符号
                temp_sentence.after_punctuation += char
                for i in xrange(cur_index + 1, len(chapter_content)):
                    if chapter_content[i].isspace():  # 忽略标点符号之后的空格
                        cur_index += 1
                        continue
                    elif not is_legal(chapter_content[i]):
                        temp_sentence.after_punctuation += chapter_content[i]
                        continue
                    else:
                        break
                cur_index += len(temp_sentence.after_punctuation)  # 指向标点之后下一个字符

                # 整段都没有字母、数字、汉字或者一段的开头有标点符号的情况，为了便于句子对齐，将句子内容设置为标点的内容
                if len(fmt_content) == 0:
                    temp_sentence.fmt_content = string_Q2B(temp_sentence.after_punctuation)
                    temp_sentence.raw_content = temp_sentence.after_punctuation
                    temp_sentence.after_punctuation = u''

                sentences.append(temp_sentence)
                before_word_sum += len(fmt_content)
                start = cur_index
                fmt_content = u''

        #当最后句子末尾没有符号作为句子结束时
        if start != cur_index:
            temp_sentence = NovelSentence(raw_content=chapter_content[start:cur_index], fmt_content=fmt_content,
                                          para_index=para_index, before_word_sum=before_word_sum)

            sentences.append(temp_sentence)
            before_word_sum += len(fmt_content)

        return sentences, before_word_sum

    def exact_align_paras(self, selected_chapter_index, candidate_chapter_list):
        """
        【可能有bug 思路同句子对齐，请参照修改更新】
        对齐最优正文和最大簇其它正文，主要返回对齐的句子dict

        对齐的句子dict是以chapter_index为key的，list为value。list是最优正文中每章在候选正文中对应句子的sentence_index，
        如果为找到匹配，对应的值为None

        同时最优正文句子的freq被更新，表明有几个匹配
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

        #检测在最优正文中是否有段落重复出现
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

        #统计最优候选中各段落在最大簇其它候选中对应的段落索引，在候选正文的全文中查找，并且判断是否重复出现
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

        #那些出现在3个候选中，且不存在重复的段落可以认为是完全匹配的
        exact_match_list = []
        for selected_para_index, selected_para in enumerate(selected_chapter.paragraph_list):
            if selected_para.freq >= 3 and not selected_para.there_dup:
                exact_match_list.append(selected_para_index)
        self.logger.info('exact match paragraph index:{0}'.format(exact_match_list))

        #初始化各章节的查找起始位置
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

        #对于没有完全匹配的段落，在其前后两个完全匹配的段落的范围内查找是否存在匹配
        for selected_para_index, selected_para in enumerate(selected_chapter.paragraph_list):
            #对于完全匹配的，更新对应章节候选的起始index
            if selected_para_index in exact_match_list:
                before_match_index = exact_match_list.index(selected_para_index)
                for chapter_index in para_align_dict:
                    #将对齐字典的值从list转换为单个值
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

            #对于未完全匹配的，如果存在匹配，检测有哪些在start和end范围内
            for chapter_index in para_align_dict:
                #未在最优候选正文中或者其它任何候选正文中重复，所以其不需要再次查找
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
        对齐最优正文和最大簇其它正文，主要返回对齐的段落dict

        对齐的段落dict是以chapter_index为key的，list为value。list是最优正文中每段在候选正文中对应段落的para_index，
        如果未找到匹配，对应的值为None

        同时最优正文的freq被更新，表明有几个匹配
        :param selected_chapter_index:
        :param candidate_chapter_list:
        :return: 段落对齐的词典
        """
        selected_chapter = candidate_chapter_list[selected_chapter_index]

        para_align_dict = {}  # {chapter_index: list of para_index, ...}
        align_cur_para_index = {}  # 标记最大簇中其它候选正文当前匹配到的段落索引
        for chapter_index in xrange(0, len(candidate_chapter_list)):
            if chapter_index == selected_chapter_index:
                continue

            para_align_dict.setdefault(chapter_index, [])
            align_cur_para_index.setdefault(chapter_index, 0)

        #统计最优正文中每一段在其它候选正文正出现的频次
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
        判断段落列表中是否有和该段落匹配的段落，返回匹配的para_index，无匹配返回-1
        从cur_para_index开始查找，paragraph_list中是否有和selected_para内容完全相同的段落，但是要保证段落在附近。

        重复段落出现的概率很小，同时cur_para_index之前的已经匹配了，所以重复段落，并且其中一段恰好缺失的概率很小。
        同时，为了以防出现这种小概率事件，并且避免每次都需要对所有段落进行比较，如果段落para_index超过6，即它们之前相差了6段则跳出。
        :param selected_para:
        :param paragraph_list:
        :param cur_para_index:
        :return:
        """
        align_index = -1
        for index in xrange(cur_para_index, len(paragraph_list)):
            cur_para = paragraph_list[index]

            if cur_para.need_remove:  #忽略basic_chapter_filter中被过滤掉的段落，段落对齐不考虑它们
                continue

            # 用来避免每次都需要对所有段落进行比较，同时从一定程度上避免重复段的情况
            if abs(cur_para.para_index - selected_para.para_index) > 6:
                break

            if cur_para.fmt_content == selected_para.fmt_content:
                align_index = index

        return align_index

    def check_para(self, selected_para_index, selected_chapter_index, para_align_dict, candidate_chapter_list):
        """
        检查段落是整段都是杂质，还是一部分为杂质，如果一部分为杂质，返回可能需要进行对齐去杂的句子

        寻找上下最近的频次超过总候选1/2的段落A和B。
        如果其它候选中A和B对应段落之间不存在其它段落，认为A和B之间所有的段落都是整段杂质。
        否则，A和B之间的段落可能包含杂质，将它们切分成句子，做句子的对齐。
        :param selected_para_index:
        :param selected_chapter_index:
        :param para_align_dict:
        :param candidate_chapter_list:
        :return: 可能需要进行对齐去杂的句子和起始段落的索引
        """
        selected_chapter = candidate_chapter_list[selected_chapter_index]

        #找出当前段前后出现在超过一半候选中的段落，获取它们匹配的段落index。另外，there_remove为True表示某个段落已被处理
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

        #对于所有前后都能匹配的候选章节，如果它们都相邻，表示整段都是杂质，否则，取它们之间的内容，进行分句比较
        need_align_sentences = {}
        match_count = 0
        remove_count = 0
        for chapter_index, chapter in enumerate(candidate_chapter_list):
            if chapter_index == selected_chapter_index:
                continue

            if before_index == -1:  # 在当前段落之前未找到freq大于总候选1/2的段落
                temp_before = -1
            else:
                temp_before = para_align_dict[chapter_index][before_index]

                if temp_before is None:  # 表明在第chapter_index中没有完全匹配的章节
                    continue

            if after_index == len(selected_chapter.paragraph_list):  # 在当前段落之后未找到freq大于总候选1/2的段落
                temp_after = len(chapter.paragraph_list)
            else:
                temp_after = para_align_dict[chapter_index][after_index]

                if temp_after is None:  # 表明在第chapter_index中没有完全匹配的章节
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
        if match_count == 0:  # 如果在其它候选未找到前后匹配的，那么只能对所有的句子做对齐了
            self.logger.info('paragraph no match has been found')
            before_index = -1
            after_index = len(selected_chapter.paragraph_list)
            for chapter_index, chapter in enumerate(candidate_chapter_list):
                need_align_sentences[chapter_index] = self.get_sentences(chapter.paragraph_list)
        elif remove_count >= 2:  # 因为段落缺失的情况很少见，所以如果有两个候选中该段不存在，那么其很有可能是杂质。最后通过分类器再次判断。
            need_align_sentences = {}
        else:  # 需要对段落进行句子对齐，将最优章对应的句子添加到need_align_sentences中
            need_align_sentences[selected_chapter_index] = self.get_sentences(
                selected_chapter.paragraph_list[before_index + 1:after_index])

        return need_align_sentences, before_index + 1, after_index

    def align_sentences(self, selected_chapter_index, need_align_sentences):
        """
        对齐最优正文和最大簇其它正文，主要返回对齐的句子dict

        对齐的句子dict是以chapter_index为key的，list为value。list是最优正文中每章在候选正文中对应句子的sentence_index，
        如果为找到匹配，对应的值为None

        同时最优正文句子的freq被更新，表明有几个匹配
        :param need_align_sentences:
        :param selected_chapter_index:
        :return:
        """
        selected_sentence_list = need_align_sentences[selected_chapter_index]

        # 初始化句子对齐字典，每个chapter_index对应一个列表，初始化包含最优正文需要对齐句子总数个None
        sentence_align_dict = {}
        init_list = [None for i in xrange(0, len(selected_sentence_list))]
        for chapter_index in need_align_sentences:
            if chapter_index == selected_chapter_index:
                continue

            sentence_align_dict[chapter_index] = init_list

        #检测在最优正文中是否有句子重复出现
        for selected_sentence_index, selected_sentence in enumerate(selected_sentence_list):
            selected_sentence.there_dup = False

            # 此段逻辑以移入分句部分 self.cut_into_sentences
            # if selected_sentence.fmt_content == '':  # 整段都没有字母、数字、汉字或者一段的开头有标点符号的情况，不能作为下文中的完全匹配
            #     selected_sentence.fmt_content = selected_sentence.after_punctuation
            #     selected_sentence.raw_content = selected_sentence.after_punctuation
            #     selected_sentence.after_punctuation = u''

            for other_index, other_sentence in enumerate(selected_sentence_list):
                if other_index == selected_sentence_index:
                    continue
                if other_sentence.fmt_content == selected_sentence.fmt_content:
                    selected_sentence.there_dup = True
                    break

        #对于最大簇中每个句子检测其是否在某个候选正文中出现多次，如果有，其频次为1；如果没有，统计其出现的频次
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

        #那些出现在所有候选中，且不存在重复的句子可以认为是完全匹配的
        exact_match_list = []
        for selected_sentence_index, selected_sentence in enumerate(selected_sentence_list):
            if selected_sentence.freq == len(need_align_sentences) and not selected_sentence.there_dup:
                exact_match_list.append(selected_sentence_index)
        self.logger.info('exact match sentence index:{0}'.format(exact_match_list))

        #初始化各章节的查找起始位置
        align_start_sentence_index = {}
        align_end_sentence_index = {}
        for chapter_index in sentence_align_dict:
            align_start_sentence_index[chapter_index] = 0
            if len(exact_match_list) == 0:
                align_end_sentence_index[chapter_index] = len(need_align_sentences[chapter_index])
            else:
                align_end_sentence_index[chapter_index] = sentence_align_dict[chapter_index][exact_match_list[0]]

        #对于没有完全匹配的句子，在其前后两个完全匹配的句子的范围内查找是否存在匹配
        for selected_sentence_index, selected_sentence in enumerate(selected_sentence_list):
            #对于完全匹配的，更新查找下一个句子的起止范围
            if selected_sentence_index in exact_match_list:
                before_match_index = exact_match_list.index(selected_sentence_index)
                for chapter_index in sentence_align_dict:
                    align_start_sentence_index[chapter_index] = sentence_align_dict[chapter_index][selected_sentence_index] + 1
                    if before_match_index == len(exact_match_list) - 1:
                        align_end_sentence_index[chapter_index] = len(need_align_sentences[chapter_index])
                    else:
                        align_end_sentence_index[chapter_index] = sentence_align_dict[chapter_index][exact_match_list[before_match_index + 1]]

                continue

            #对于未完全匹配的，如果存在匹配，检测有是否在完全匹配对应的索引范围内
            for chapter_index in sentence_align_dict:
                #句子未重复，且在当前章节中有匹配，只需要检测当前的索引是否在完全匹配对应的索引范围内即可
                if not selected_sentence.there_dup:
                    if sentence_align_dict[chapter_index][selected_sentence_index] is not None:
                        # 如果在范围内，修改开始范围为对应索引+1.否则，将句子的频次减1，并且将其对应的索引赋值为None
                        if align_start_sentence_index[chapter_index] <= sentence_align_dict[chapter_index][selected_sentence_index] < align_end_sentence_index[chapter_index]:
                            align_start_sentence_index[chapter_index] = sentence_align_dict[chapter_index][selected_sentence_index] + 1
                        else:
                            sentence_align_dict[chapter_index][selected_sentence_index] = None
                            selected_sentence.freq -= 1
                else:
                    sentence_align_dict[chapter_index][selected_sentence_index] = None
                    # 在起始范围内查找该句子，如果不存在重复，认为找到匹配。如果存在重复，认为没有匹配。
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
        检查句子是整句都是杂质，还是一部分为杂质，如果一部分为杂质，返回可能需要进一步去杂的句子

        通过对齐该句子前后的句子，获得一个范围，
        如果该句子的前后句子是相邻的，那么该句子整体可能都是杂质，通过分类器进一步分类，可以去除。
        否则，需要将句子返回，进一步对句子进行去杂。

        :param selected_sentence_index:
        :param selected_chapter_index:
        :param sentence_align_dict: 句子对齐的结果，每个候选章节对应一个list，存储selected对应句子对应的索引
        :param need_align_sentences: 保存各个候选章节中用来对齐的句子
        :param sentence_freq_threshold: freq小于sentence_freq_threshold的句子需要检测是否为杂质
        :return:
        """
        selected_sentence_list = need_align_sentences[selected_chapter_index]

        #找出当前句前后最邻近的freq大于等于sentence_freq_threshold的句子，获取它们匹配的sentence_index
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
        elif remove_count * 2 > match_count:  # 如果认为是整句杂质，例如完全匹配的章节的标点替换，这样可以不用做标点的检测
            if before_index != -1:
                #前一个句子如果只包含标点符号，标点符号的内容在fmt_content中
                if len(need_align_sentences[match_chapter_index][match_before_index].after_punctuation) == 0:
                    selected_sentence_list[before_index].fmt_content = need_align_sentences[match_chapter_index][match_before_index].fmt_content
                    selected_sentence_list[before_index].raw_content = need_align_sentences[match_chapter_index][match_before_index].raw_content
                else:
                    selected_sentence_list[before_index].after_punctuation = need_align_sentences[match_chapter_index][match_before_index].after_punctuation

            need_check_sentences = {}
        else:  # 句子的一部分是杂质
            need_check_sentences[selected_chapter_index] = selected_sentence_list[before_index + 1:after_index]

        return need_check_sentences, before_index + 1, after_index

    def remove_part_impurity(self, selected_chapter_index, need_check_sentences):
        """
        策略暂时未测试

        need_replace标识，如果为True，表明最后输出时，句子输出的内容为fmt_content。否则，输出raw_content+after_punctuation
        所以，处理完之后的句子要将need_replace设为True，并将处理后的内容写入fmt_content
        :param need_check_sentences:
        :return:
        """
        selected_sentence_list = need_check_sentences[selected_chapter_index]

        for sentence in selected_sentence_list:
            sentence.need_replace = False

        # 统计句子的个数、字符数、标点符号数、以及正文（包括标点），然后将所有句子的内容置为空。将第一个句子的内容设置为所有内容的连接
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

            selected_punc_count -= len(selected_sentence_list[-1].after_punctuation)  # 不用比较最后的标点符号

        selected_sentence_list[0].fmt_content = selected_text  # 所有there_remove为True的句子，其内容都直接读取fmt_content

        sen_num_dict = {}  # 句子的个数
        word_count_dict = {}  # 汉字、字母、数字的个数
        text_dict = {}
        clean_text_dict = {}  # 所有句子中的汉字、字母、数字

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

            temp_punc_count = 0  # 标点符号的个数

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

        # 1, 标点符号和空格，导致分句不同，此时正文内容相同，但是句子不能对齐。此时通常都是有标点的是正确的。
        # 2，有个别错别字时，正文的长度相同，无法判断那一个正文质量更好，所以也同样挑选标点符号最多的。
        if is_content_equal or is_word_count_equal:
            selected_sentence_list[0].fmt_content = text_dict[max_punc_chapter_index]
            return

        # 当正文字数不相等时，可能最长的正文中包含杂质，或者较短的正文缺少内容。
        # 因为我们rank时，尽量挑选中文字符多的，所以，通常情况下，候选的正文的句子是最长的.
        # 3，通过分类器判断最长正文是否是杂质，如果是，判断是否存在包含关系，如果存在选择较短的正文，如果不存在，认为其为整句杂质
        # 4, 如果最长的句子不是杂质，那么可能是较短的正文缺少内容，或者较长的正文包含拼音.
        text_set = set(text_dict.values())

        word_set_dict = {}  # 字的集合，或出现重复字符的情况，所以set的大小和word_count可能不相同
        for chapter_index, text in text_dict.items():
            word_set_dict[chapter_index] = set(string_filter(text))
        max_word_set = word_set_dict[max_word_chapter_index]

        if self.classifier.classify(clean_text_dict[max_word_chapter_index]) < 0.1:
            is_include = True
            for word_set in word_set_dict.values():
                if not len(max_word_set & word_set) * 2 > len(word_set):  # 超过一半的字符是相同的
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
            #检测是否包含字母，如果包含，将汉字转为拼音，检测是否相等，如果相等，选择不包含字母的。否则，直接选择字数最多的
            selected_sentence_list[0].fmt_content = text_dict[max_word_chapter_index]

    def is_impurity(self, case_content):
        '''
        通过分类器判断是否为杂质。由于分类器的性能不稳定，需要配合一些启发式规则判断。

        因为小说正文的内容比较复杂，没有合理的策略能够覆盖需要覆盖的正文。所以，分类器性能不稳定，某些正例或者句子一部分是杂质的情况，都可能造成误判，认为其是杂质。
        因此，分类器的目标定义为，作为句子对齐的辅助，阈值设为0.1，即概率小于0.1表示其为杂质，对于杂质的召回率达到100%，即不会将杂质判断为非杂质。
        策略：【以下策略是在句子未对齐的前提下实施的】

        * 对于短句，尤其是一个中文字通常认为是正例。将连续的几个可能包含杂质的句子作为一个整体用分类器判断。如果字数还是小于3，如果全都是数字或者字母，直接作为杂质
        * 对于字母和数字和标点符号等容易判断为正例，判断如果不包含中文字符，则直接当做杂质处理。
        * 有一些负例训练集中没有，通过整句杂质补充训练集。
        * 对于文章的章节标题等，需要更多的训练集，可以人工构造，所有第章和第节，作为负例的训练集
        :return:
        '''
        return False

    def sentence_to_paragraph(self, paragraph_list, para_start_index, para_end_index, sentence_list):
        """

        暂时未处理标点符号
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
                if cur_sen.need_remove:  # 句子是整句杂质
                    # cur_para.fmt_content += u'<span style="display:none" class="is_impurity whole_sentence_remove">' + \
                    #                         cur_sen.raw_content + cur_sen.after_punctuation + u'</span>'
                    cur_para.fmt_content += u'<span class="whole_sentence_remove">【整句杂质 ' + \
                                            cur_sen.raw_content + cur_sen.after_punctuation + u'】</span>'

                elif not cur_sen.there_remove:  # 句子的freq大于等于sentence_freq_threshold，但是其在未对齐的段落中
                    # cur_para.fmt_content += cur_sen.raw_content + cur_sen.after_punctuation
                    cur_para.fmt_content += u'【' + str(cur_sen.freq) + u'】' + \
                                            cur_sen.raw_content + cur_sen.after_punctuation
                else:  # 句子的一部分是杂质
                    if cur_sen.need_replace:
                        # cur_para.fmt_content += cur_sen.fmt_content
                        cur_para.fmt_content += u'<span class="part_sentence_remove"> ' + \
                                                u'【new ' + cur_sen.fmt_content + u' old ' \
                                                + cur_sen.raw_content + cur_sen.after_punctuation + u'】</span>'
                    else:
                        # cur_para.fmt_content += cur_sen.raw_content + cur_sen.after_punctuation
                        cur_para.fmt_content += u'<span class="not_handle_impurity">【未处理杂质 ' + \
                                                cur_sen.raw_content + cur_sen.after_punctuation + u'】</span>'

    def back_to_html(self, paragraph_list, site_id):
        """
        将paras还原为html的形式，para中para_index为-1，表示应该被删除的段落。sentence中need_remove为true的，表示应该被删除的句子
        :param paras:
        :return:
        """
        pure_chapter_content = u''
        p_tag = u'<p style="text-indent:2em;">'
        back_p_tag = u'</p>'

        for paragraph in paragraph_list:
            if paragraph.need_remove:
                if paragraph.there_remove:  # 表示该段落经过段落对齐确认为整段杂质，通过分类器进一步验证
                    if not self.is_impurity(string_filter(paragraph.fmt_content)):
                        self.logger.info('para_index:{0} is saved by the classifier'.format(paragraph.para_index))
                        pure_chapter_content += p_tag + paragraph.fmt_content + back_p_tag
                        continue

                # pure_chapter_content += u'<p style="text-indent:2em;" style="display:none" class="is_impurity whole_paragraph_impurity">' \
                #                        + paragraph.raw_content + u'</p>'
                pure_chapter_content += p_tag + u'【段落杂质 ' + paragraph.raw_content + u'】' + back_p_tag

                if len(paragraph.fmt_content) != 0:
                    with codecs.open('data/whole_para.csv', 'a', encoding='gbk', errors='ignore') as whole_impurity_file:
                        prob = self.classifier.classify(paragraph.fmt_content)
                        whole_impurity_file.write(
                            paragraph.fmt_content + ',' + str(site_id) + ',' + str(prob > 0.5 and 1 or 0) + ',' + str(prob) + '\n')
            else:
                pure_chapter_content += p_tag + paragraph.fmt_content + back_p_tag

        return pure_chapter_content
