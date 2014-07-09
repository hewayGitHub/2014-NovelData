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

# 初始化标点符号
punctuation_list = u'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
# punctuation_list = u'.,?<>;:\'"[]{}-~!()'
for p in punctuation_list:
    punctuation_list += unichr(ord(p) + 0xfee0)
punctuation_list += u'·～！＠＃￥％……＆×（）——＋－＝【】＼｛｝｜；：’‘“”，。、《》？'
# punctuation_list += u'，。？《》；：”“’‘{}【】、——（）……%！'
punctuation_set = set(punctuation_list)


def read_from_file_11111111111():
    """
    读取外包标注的杂质正负例
    :return:
    """
    sample_dir = r'D:\正文优化\外包样本\负例\\'

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

    sample_dir = r'D:\正文优化\外包样本\正例\\'

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
    同ChapterContentFilter.cut_into_sentences

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
            raw_content=chapter_content[start:cur_index]

            # 查找句子后所有的标点符号
            after_punctuation = char
            for i in xrange(cur_index + 1, len(chapter_content)):
                if chapter_content[i].isspace():  # 忽略标点符号之后的空格
                    cur_index += 1
                    continue
                elif not is_legal(chapter_content[i]):
                    after_punctuation += chapter_content[i]
                    continue
                else:
                    break
            cur_index += len(after_punctuation)  # 指向标点之后下一个字符

            # 整段都没有字母、数字、汉字或者一段的开头有标点符号的情况，为了便于句子对齐，将句子内容设置为标点的内容
            if len(fmt_content) == 0:
                fmt_content = string_Q2B(after_punctuation)
                raw_content = after_punctuation
                after_punctuation = u''

            sentences.append((raw_content, fmt_content, after_punctuation))
            start = cur_index
            fmt_content = u''

    # 当最后句子末尾没有符号作为句子结束时
    if start != cur_index:
        raw_content=chapter_content[start:cur_index]

        sentences.append(sentences.append((raw_content, fmt_content, u'')))

    return sentences


def clean_impurity(impurity):
    """
    整理外包提供的正负例
    1，全角转半角
    3，去掉[分段]
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

    impurity = impurity.replace(u'[分段]', '')
    impurity = string_filter(impurity)

    impurity = impurity.lower()
    return impurity


def clean_data():
    """
    整理外包提供的正例和负例

    负例样本中包括段首还是段尾和作者添加的杂质

    作者添加的话暂时不考虑作为杂质

    对于字符先全角转半角，便于对齐时的比较和判断是否为字母、数字和中文。
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
    分隔数据，训练集和测试集
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
    读取negative和positive来训练模型

    use_all_data选择使用所有数据还是仅仅是训练集
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
    neutral表示作者的话
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
    测试列表中每个句子的
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
    按照idf从小到大排序负例中的词
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

    # cases.append(u'我不知道今后自己的命运会怎么样，但是至少现在保好自己这条小命。')
    # cases.append(u'听说她还是江南的才女，多彩多艺，所以封她为全贵人，全，取之全才的意思。')
    # cases.append(u'我一定会支持你的')
    # cases.append(u'我一定会')
    # cases.append(u'支持你的')
    #cases.append(u'太祖当选为炎黄红党中央zhengzhiju主席')
    cases.append(u'也就是1943年3月21日')
    cases.append(u'一道赤色火龙')
    cases.append(u'【第两百九十六章】白蓉蓉来电')
    cases.append(u'''这个时候易才哲也说话了，“山伯啊，你就答应夕筠吧，我就这么一个宝贝女儿，如果你做了我的女婿，那就算是与马家开战>
        ，我也会全力支持你，若是马家背后的门派动手，我也会请动齐天门的人出手相助。”''')
    cases.append(u'(未完待续。如果您喜欢这部作品，欢迎您来起点投推荐票、月票，您的支持>，就是我最大的动力。手机用户请到阅读。)')
    cases.append(u'我彻夜未眠')
    #cases.append(u'如果一旦有人中了‘梦靥无涯’技能')
    # cases.append(u'不用麻烦了')
    # cases.append(u'这应该是她第一次自己动手穿衣服')
    # cases.append(u'你给本王站住。')
    # cases.append(u'见此情形')
    # cases.append(u'更新稍晚了些，没有达到预定的一个小时之后，嘻嘻，云小姐爱乃们。')
    # cases.append(u'她就什么都不是了')
    # cases.append(u'第四十章不忍')
    # cases.append(u'书记，道，我们应gai做个hao人')
    # cases.extend(u'''
    # 举报错误和落后的章节是对来书最大的帮助
    # 强烈建议您
    # 强烈建议您
    # 强烈建议您
    # 强烈建议您
    # 强烈建议您
    # 强烈建议您
    # 强烈建议您
    # 强烈建议您
    # 强烈建议您
    # 强烈建议您
    # fqxswcomfqxswcom
    # 章节错误点此举报
    # 如有错误
    # cmsbook3083003722html
    # 69zw
    # 告诉您的朋友
    # 告诉您的朋友
    # '''.split('\n'))
    classify(cases)
    print 'done'