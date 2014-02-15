#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-03 16:39'

import Levenshtein

def here():
    print('PrimeMusic')

def is_chinese(char):
    """
        �ж�char�Ƿ�Ϊ���ģ�charΪunicode
    """
    if char >= u'\u4e00' and char <= u'\u9f5a':
        return True
    else:
        return False

def is_number(char):
    """
        �ж�char�Ƿ�Ϊ���֣�charΪunicode
    """
    if char >= u'\u0030' and char <= u'\u0039':
        return True
    else:
        return False

def is_alphabet(char):
    """
        �ж�char�Ƿ�Ϊ��ĸ��charΪunicode
    """
    if char >= u'\u0041' and char <= u'\u005a':
        return True
    if char >= u'\u0061' and char <= u'\u007a':
        return True
    return False

def is_legal(char):
    """
        �ж�char�Ƿ�Ϊ�Ǻ��֣���ĸ������֮��������ַ���charΪunicode
    """
    if is_alphabet(char) or is_chinese(char) or is_number(char):
        return True
    else:
        return False

def B2Q(char):
    """
        ���תȫ�ǣ�charΪunicode
    """
    inside_code = ord(char)
    if inside_code < 0x0020 or inside_code > 0x7e:
        return char
    if inside_code == 0x0020:
        inside_code = 0x3000
    else:
        inside_code += 0xfee0
    return unichr(inside_code)

def Q2B(char):
    """
        ȫ��ת��ǣ�charΪunicode
    """
    inside_code = ord(char)
    if inside_code == 0x3000:
        inside_code = 0x0020
    else:
        inside_code -= 0xfee0
    if inside_code < 0x0020 or inside_code > 0x7e:
        return char
    return unichr(inside_code)

def string_Q2B(string):
    """
    """
    string = ''.join(Q2B(char) for char in string)
    return string

def string_filter(string):
    """
        ȫ��ת��ǣ����˸����������
    """
    string = ''.join(is_legal(char) and char or '' for char in string)
    return string

def string_format(string):
    """
    """
    string = string.replace(u'\u005c', u'')
    string = string.replace(u'\u0027', u'\u005c\u0027')
    string = string.encode("GBK", "ignore")
    return string

def string_similarity(string_x, string_y):
    """
    """
    return Levenshtein.ratio(string_x, string_y)


if __name__ == '__main__':
    string = '����abc**987&^%test����ȫ��'.decode('GBK', 'ignore')
    print(string.encode('utf8', 'ignore'))
    print(string_filter(string).encode('utf8', 'ignore'))
    here()    







