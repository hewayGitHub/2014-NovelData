#/bin/env python
#-*- coding:gbk -*-

__author__ = 'hewei13'
__date__ = '2014/6/24 17:23'

import os
import codecs
import random
from snownlp import SnowNLP, sentiment
from util.BasicStringMethod import *
cur_linesep = os.linesep
lt_pattern = re.compile(r'(&lt;|&#60;)', re.U)
gt_pattern = re.compile(r'(&gt;|&#62;)', re.U)

# ��ʼ��������
punctuation_list = u'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
# punctuation_list = u'.,?<>;:\'"[]{}-~!()'
for p in punctuation_list:
    punctuation_list += unichr(ord(p) + 0xfee0)
punctuation_list += u'�����������������������������������������ܣ�����������������������������'
# punctuation_list += u'����������������������{}������������������%��'
punctuation_set = set(punctuation_list)


def read_from_file_11111111111():
    """
    ��ȡ�����ע������������
    :return:
    """
    sample_dir = r'D:\�����Ż�\�������\����\\'

    negative_file = codecs.open('../data/negative.txt', 'w', encoding='utf-8', errors='ignore')
    neutral_file = codecs.open('../data/neutral.txt', 'w', encoding='utf-8', errors='ignore')

    for filename in os.listdir(sample_dir):
        with codecs.open(sample_dir + filename, encoding='gbk') as sample_file:
            for line in sample_file:
                items = line.strip().split(",")
                if len(items) < 5:
                    print 'filename:', filename, 'line:', line
                    continue
                elif len(items) < 6:
                    continue

                if items[5] != '':
                    if len(items) < 7:
                        continue

                    impurity = items[6].strip()
                    if len(impurity) == 0:
                        continue

                    if len(items) >= 9 and items[8] == '1':
                        neutral_file.write(impurity + cur_linesep)
                    else:
                        negative_file.write(impurity + cur_linesep)
                else:
                    if len(items) < 8:
                        continue

                    impurity = items[7].strip()
                    if len(impurity) == 0:
                        continue

                    if len(items) >= 10 and items[9] == '1':
                        neutral_file.write(impurity + cur_linesep)
                    else:
                        negative_file.write(impurity + cur_linesep)

    negative_file.close()
    neutral_file.close()

    sample_dir = r'D:\�����Ż�\�������\����\\'

    positive_file = codecs.open('../data/positive.txt', 'w', encoding='utf-8', errors='ignore')
    for filename in os.listdir(sample_dir):
        with codecs.open(sample_dir + filename, encoding='gbk') as sample_file:
            for line in sample_file:
                items = line.strip().split(",")
                if len(items) < 6:
                    print 'filename:', filename, 'line:', line
                    continue

                if items[5] == '':
                    if len(items) < 7:
                        continue

                    impurity = items[6].strip()
                    if len(impurity) == 0:
                        continue

                    positive_file.write(impurity + cur_linesep)
                else:
                    if len(items) < 6:
                        continue

                    impurity = items[5].strip()
                    if len(impurity) == 0:
                        continue

                    positive_file.write(impurity + cur_linesep)
    positive_file.close()


def cut_into_sentences(chapter_content):
    """
    ͬChapterContentFilter.cut_into_sentences

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
            raw_content=chapter_content[start:cur_index]

            # ���Ҿ��Ӻ����еı�����
            after_punctuation = char
            for i in xrange(cur_index + 1, len(chapter_content)):
                if chapter_content[i].isspace():  # ���Ա�����֮��Ŀո�
                    cur_index += 1
                    continue
                elif not is_legal(chapter_content[i]):
                    after_punctuation += chapter_content[i]
                    continue
                else:
                    break
            cur_index += len(after_punctuation)  # ָ����֮����һ���ַ�

            # ���ζ�û����ĸ�����֡����ֻ���һ�εĿ�ͷ�б����ŵ������Ϊ�˱��ھ��Ӷ��룬��������������Ϊ��������
            if len(fmt_content) == 0:
                fmt_content = string_Q2B(after_punctuation)
                raw_content = after_punctuation
                after_punctuation = u''

            sentences.append((raw_content, fmt_content, after_punctuation))
            start = cur_index
            fmt_content = u''

    # ��������ĩβû�з�����Ϊ���ӽ���ʱ
    if start != cur_index:
        raw_content=chapter_content[start:cur_index]

        sentences.append(sentences.append((raw_content, fmt_content, u'')))

    return sentences


def clean_impurity(impurity):
    """
    ��������ṩ��������
    1��ȫ��ת���
    3��ȥ��[�ֶ�]
    :param impurity:
    :return:
    """
    impurity = string_Q2B(impurity)

    lt_pattern = re.compile(r'(&lt;|&#60;)', re.U)
    gt_pattern = re.compile(r'(&gt;|&#62;)', re.U)
    quto_pattern = re.compile(r'(&quot;|&#34;)', re.U)
    impurity = lt_pattern.sub('<', impurity)
    impurity = gt_pattern.sub('>', impurity)
    impurity = quto_pattern.sub('"', impurity)

    impurity = impurity.replace(u'[�ֶ�]', '')
    impurity = string_filter(impurity)

    impurity = impurity.lower()
    return impurity


def clean_data():
    """
    ��������ṩ�������͸���

    ���������а������׻��Ƕ�β��������ӵ�����

    ������ӵĻ���ʱ��������Ϊ����

    �����ַ���ȫ��ת��ǣ����ڶ���ʱ�ıȽϺ��ж��Ƿ�Ϊ��ĸ�����ֺ����ġ�
    :return:
    """
    print 'clean data'

    negative_clean_file = codecs.open('../data/clean_negative.txt', 'w', encoding='utf-8', errors='ignore')
    neutral_clean_file = codecs.open('../data/clean_neutral.txt', 'w', encoding='utf-8', errors='ignore')
    positive_clean_file = codecs.open('../data/clean_positive.txt', 'w', encoding='utf-8', errors='ignore')

    with codecs.open('../data/negative.txt', encoding='utf-8', errors='ignore') as negative_file:
        for line in negative_file:
            line = line.strip()
            if line == '':
                continue

            impurity = clean_impurity(line)
            if impurity != '':
                negative_clean_file.write(impurity + cur_linesep)

    with codecs.open('../data/neutral.txt', encoding='utf-8', errors='ignore') as neutral_file:
        for line in neutral_file:
            line = line.strip()
            if line == '':
                continue

            impurity = clean_impurity(line)
            if impurity != '':
                neutral_clean_file.write(impurity + cur_linesep)

    with codecs.open('../data/positive.txt', encoding='utf-8', errors='ignore') as positive_file:
        for line in positive_file:
            line = line.strip()
            if line == '':
                continue

            impurity = clean_impurity(line)
            if impurity != '':
                positive_clean_file.write(impurity + cur_linesep)

    negative_clean_file.close()
    neutral_clean_file.close()
    positive_clean_file.close()


def split_data():
    """
    �ָ����ݣ�ѵ�����Ͳ��Լ�
    :return:
    """
    print 'split data'

    negative_case = []
    with codecs.open('../data/clean_negative.txt', encoding='utf-8') as negative_file:
        for line in negative_file:
            line = line.strip()
            if line != '':
                negative_case.append(line)
    test_negative = random.sample(negative_case, len(negative_case) / 5)

    train_negative_file = codecs.open('../data/train_negative.txt', 'w', encoding='utf-8', errors='ignore')
    test_negative_file = codecs.open('../data/test_negative.txt', 'w', encoding='utf-8', errors='ignore')
    for nc in negative_case:
        if nc in test_negative:
            test_negative_file.write(nc + cur_linesep)
        else:
            train_negative_file.write(nc + cur_linesep)
    train_negative_file.close()
    train_negative_file.close()

    positive_case = []
    with codecs.open('../data/clean_positive.txt', encoding='utf-8') as positive_file:
        for line in positive_file:
            line = line.strip()
            if line != '':
                positive_case.append(line)

    test_positive = random.sample(positive_case, len(positive_case) / 5)

    train_positive_file = codecs.open('../data/train_positive.txt', 'w', encoding='utf-8', errors='ignore')
    test_positive_file = codecs.open('../data/test_positive.txt', 'w', encoding='utf-8', errors='ignore')
    for pc in positive_case:
        if pc in test_positive:
            test_positive_file.write(nc + cur_linesep)
        else:
            train_positive_file.write(nc + cur_linesep)
    train_positive_file.close()
    test_positive_file.close()


def train_sentiment(use_all_data=True):
    """
    ��ȡnegative��positive��ѵ��ģ��

    use_all_dataѡ��ʹ���������ݻ��ǽ�����ѵ����
    :return:
    """
    print 'train model'

    if not use_all_data:
        sentiment.train('../data/train_negative.txt', '../data/train_positive.txt')
        sentiment.save('../data/train_impurity_classifier')
    else:
        sentiment.train('../data/clean_negative.txt', '../data/clean_positive.txt')
        sentiment.save('../data/impurity_classifier')


def test_sentiment():
    print 'test model'

    sentiment.load('../data/train_impurity_classifier')

    print 'test_negative'
    # with codecs.open('../data/test_negative.txt', encoding='utf-8') as negative_file:
    #     for line in negative_file:
    #         if sentiment.classify(line) > 0.1:
    #             print line,

    raw_input('press enter to continue')
    print 'test_positive'
    with codecs.open('../data/test_positive.txt', encoding='utf-8') as positive_file:
        for line in positive_file:
            if sentiment.classify(line) < 0.5:
                print line,


def test_neutral(to_stdout=True):
    """
    neutral��ʾ���ߵĻ�
    :param to_stdout:
    :return:
    """
    print 'test neutral'

    sentiment.load('../data/impurity_classifier')
    result_file = None
    if not to_stdout:
        result_file = codecs.open('../data/result.csv', 'w', encoding='gbk', errors='ignore')

    with codecs.open('../data/clean_neutral.txt', encoding='utf-8') as neutral_file:
        for line in neutral_file:
            line = line.strip()
            prob = sentiment.classify(line)
            if 0.8 > prob > 0.2:
                if to_stdout:
                    print (line + ',' + str(prob > 0.5 and 1 or 0) + ',' + str(prob) + cur_linesep).encode('gbk')
                    raw_input('press enter to continue')
                else:
                    result_file.write(line + ',' + str(prob > 0.5 and 1 or 0) + ',' + str(prob) + cur_linesep)

    if not to_stdout:
        result_file.close()


def classify(cases):
    """
    �����б���ÿ�����ӵ�
    :param cases:
    :return:
    """
    for case in cases:
        case = clean_impurity(case)
        sentiment.load('../data/impurity_classifier')
        prob = sentiment.classify(case)
        print (case + ',' + str(prob > 0.5 and 1 or 0) + ',' + str(prob) + cur_linesep).encode('gbk')


def sum_word():
    """
    ����idf��С�����������еĴ�
    :return:
    """
    print 'sum_word'

    words_list = []
    with codecs.open('../data/clean_negative.txt', encoding='utf-8') as negative_file:
        for line in negative_file:
            line = line.strip()
            if line == '':
                continue

            words_list.append(SnowNLP(line).words)

    sp = SnowNLP(words_list)
    idf = sorted(sp.idf.items(), key=lambda tuple:tuple[1])
    with codecs.open('../data/item_freq.txt', 'w', encoding='gbk', errors='ignore') as item_file:
        for word, freq in idf:
            if len(word) < 2:
                continue
            item_file.write(word + u'\t' + str(freq) + cur_linesep)

if __name__ == '__main__':
    #sum_word()

    # clean_data()
    # split_data()

    # train_sentiment(use_all_data=False)
    #test_sentiment()

    # train_sentiment(use_all_data=True)
    # test_neutral(to_stdout=True)

    cases = list()
    #
    # with codecs.open('../data/clean_negative.txt', encoding='utf-8') as negative_file:
    #     count = 0
    #     for line in negative_file:
    #         line = line.strip()
    #         if line != '':
    #             cases.append(line[:len(line)/2])
    #             cases.append(line[len(line)/2:])
    #
    #         count += 1
    #         if count > 20:
    #             break

    # cases.append(u'�Ҳ�֪������Լ������˻���ô���������������ڱ����Լ�����С����')
    # cases.append(u'��˵�����ǽ��ϵĲ�Ů����ʶ��գ����Է���Ϊȫ���ˣ�ȫ��ȡ֮ȫ�ŵ���˼��')
    # cases.append(u'��һ����֧�����')
    # cases.append(u'��һ����')
    # cases.append(u'֧�����')
    #cases.append(u'̫�浱ѡΪ�׻ƺ쵳����zhengzhiju��ϯ')
    cases.append(u'Ҳ����1943��3��21��')
    cases.append(u'һ����ɫ����')
    cases.append(u'�������پ�ʮ���¡�����������')
    cases.append(u'''���ʱ���ײ���Ҳ˵���ˣ���ɽ��������ʹ�ӦϦ�ްɣ��Ҿ���ôһ������Ů��������������ҵ�Ů�����Ǿ���������ҿ�ս>
        ����Ҳ��ȫ��֧���㣬������ұ�������ɶ��֣���Ҳ���붯�����ŵ��˳�����������''')
    cases.append(u'(δ������������ϲ���ⲿ��Ʒ����ӭ�������Ͷ�Ƽ�Ʊ����Ʊ������֧��>�����������Ķ������ֻ��û��뵽�Ķ���)')
    cases.append(u'�ҳ�ҹδ��')
    #cases.append(u'���һ���������ˡ��������ġ�����')
    # cases.append(u'�����鷳��')
    # cases.append(u'��Ӧ��������һ���Լ����ִ��·�')
    # cases.append(u'�������վס��')
    # cases.append(u'��������')
    # cases.append(u'����������Щ��û�дﵽԤ����һ��Сʱ֮����������С�㰮���ǡ�')
    # cases.append(u'����ʲô��������')
    # cases.append(u'����ʮ�²���')
    # cases.append(u'��ǣ���������Ӧgai����hao��')
    # cases.extend(u'''
    # �ٱ�����������½��Ƕ��������İ���
    # ǿ�ҽ�����
    # ǿ�ҽ�����
    # ǿ�ҽ�����
    # ǿ�ҽ�����
    # ǿ�ҽ�����
    # ǿ�ҽ�����
    # ǿ�ҽ�����
    # ǿ�ҽ�����
    # ǿ�ҽ�����
    # ǿ�ҽ�����
    # fqxswcomfqxswcom
    # �½ڴ����˾ٱ�
    # ���д���
    # cmsbook3083003722html
    # 69zw
    # ������������
    # ������������
    # '''.split('\n'))
    classify(cases)
    print 'done'