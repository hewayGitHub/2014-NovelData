#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'hewei13'
__date__ = '2014-06-06 17:18'

from basic.NovelStructure import Singleton
from public.BasicStringMethod import is_chinese, is_alphabet, is_number
import logging
import re
import HTMLParser


def count_word(unicode_str):
    """
    统计字符串中汉字、字母和数字的个数
    """
    cn_count = 0
    valid_count = 0
    for char in unicode_str:
        if is_chinese(char):
            cn_count += 1
            valid_count += 1
        elif is_alphabet(char) or is_number(char):
            valid_count += 1

    return valid_count, cn_count


def count_chinese(unicode_str):
    """
    统计字符串中汉字的个数
    """
    cn_count = 0
    for char in unicode_str:
        if is_chinese(char):
            cn_count += 1

    return cn_count

class ChapterHtmlFilter(object):
    """
    输入chapter_page，过滤并处理其中的html标签后，返回处理后的chapter_page

    返回的chapter_page中的NOVELCONTENT的样式满足如下条件：
    1，只包含<p>和</p>
    2，页面完整，无tag缺失或者<p>嵌套的情况
    """
    __metaclass__ = Singleton

    def __init__(self):
        """
        初始化html过滤所需的正则表达式
        """
        self.logger = logging.getLogger('novel.chapter.html')
        self.err = logging.getLogger('err.chapter.html')

        #处理html转义字符
        self.html_parser = HTMLParser.HTMLParser()

        # 下列正则表达式用于识别所有对应tag的形式
        self.left_space_pattern = re.compile(r'^(\s|&nbsp;)+', re.U)
        self.right_space_pattern = re.compile(r'(\s|&nbsp;)+$', re.U)
        self.tag_pattern = re.compile(r'<(/?[a-zA-Z!]+)([^>]*)>', re.U)

        self.hidden_pattern = re.compile(r'display\s*:\s*none', re.U | re.I)
        self.invisible_pattern = re.compile(r'visibility\s*:\s*hidden', re.U | re.I)
        self.alt_pattern = re.compile(r'\salt=(.)(.*?)\1', re.U | re.I)

        self.empty_p_pattern = re.compile(r'<p style="text-indent:2em;"></p>', re.U)

    def chapter_html_filter(self, raw_chapter_content):
        """
        过滤并处理章节正文中的HTML，并返回处理后的章节正文。
        输入和输出的章节正文都是unicode编码。不会去除任何在前端可见字符，并且保证最后的html页面只包含<p></p>，且格式规范。
        并且，所有段首、段尾的空格都被去除了。

        具体要求如下：
        0，将段首尾空白字符去掉
        1，输出的章节正文只有<p>和</p>，而且不会有嵌套。
        2，为<p>添加属性<p style="text-indent:2em;">，段首缩进两个字符
        3，过滤<script>标签和它们之间的文本
        4，过滤包含隐藏属性的标签和它们之间的文本。
        5，某些站点利用图片替换文字，<img data-width="8" data-height="16" src="" alt="男"/>
        6，删除空白段

        注意；
        1，HTML标签的起始字符为[a-zA-Z!]，可以保证不会匹配<1><你好>之类的内容
        2，对于标签p、/p、div等要确保完全匹配，因为它们可能是其它标签的前缀。通过提取标签名匹配
        3，通过使用unicode，\s可以匹配扩展的拉丁文（ISO 8859-1）中的不间断空格\xa0、"&nbsp;"和中文空格\u3000等空白字符
        4，所有可见的正文都不能做处理，都有可能是小说正文。例如<a>标签暂时不做处理，只是去除标签，在后期正文去杂处理
        5，先处理html转义字符，以便html标签检测，后期正文去杂&amp;就不会被作为杂质
        """
        #处理html转义字符，以便html标签检测，后期正文去杂&amp;就不会被作为杂质
        raw_chapter_content = self.html_parser.unescape(raw_chapter_content)

        format_chapter_content = u''

        # 完成格式化步骤0-9
        pre_end = 0  # 标志上一个tag的尾index + 1，故初始化为0
        p_level = 0  # 遇到<p>加1，遇到</p>减1
        is_p_head = True  # 标记当前正文是否是段首，用于去除段首的空格.初始值为True，以防第一个tag前有内容
        need_remove = False  # 当遇到<script>或者需要隐藏的标签时，为True，去除首尾标签以及它们之间的正文
        remove_tag_level = 0  # 用于判断需要去除的标签的尾标签，如，<div style='display:none'> <div> </div> </div>
        remove_tag_name = ''  # 需要去除的标签的名称
        for tag_match in self.tag_pattern.finditer(raw_chapter_content):
            tag = tag_match.group()
            tag_name = tag_match.group(1).lower()  # html标签不区分大小写，统一转换为小写
            first = tag_match.start()
            end = tag_match.end()

            # 当遇到<script>或者需要隐藏的标签时，设置need_remove为True
            # 如果当前need_remove为True，表明当前tag和前一个tag之间的正文不需要输出。
            # 同时，要检测是否离开need_remove标签内部
            if not need_remove:
                if tag_name == u'script' or self.hidden_pattern.search(tag) is not None \
                        or self.invisible_pattern.search(tag) is not None:
                    need_remove = True
                    remove_tag_name = tag_name
                    remove_tag_level = 1

                    #需要输出需要need_remove的html标签之前的内容
                    tag_name = u'meet_need_remove'
            else:
                if tag_name == remove_tag_name:
                    remove_tag_level += 1
                elif tag_name[1:] == remove_tag_name:
                    remove_tag_level -= 1

                if remove_tag_level == 0:
                    need_remove = False

                #更新pre_end
                pre_end = end
                continue

            #is_p_head表明在段首，直到遇到非空的正文，否则相当于一直是段首
            if is_p_head:  # 段首
                if pre_end == first:
                    between_content = u''
                else:
                    between_content = self.left_space_pattern.sub('', raw_chapter_content[pre_end:first])

                if len(between_content) != 0:
                    is_p_head = False
            else:
                between_content = raw_chapter_content[pre_end:first]

            #更新pre_end
            pre_end = end

            if tag_name == 'p' or tag_name == 'div' or tag_name == 'br':
                #遇到div、p、br，表示新段落的开始
                #如果p_level大于等于1，表示会出现<p>的嵌套，在当前<p>前添加</p>，防止嵌套出现
                if p_level >= 1:
                    between_content = self.right_space_pattern.sub('', between_content)
                    format_chapter_content += between_content + u'</p><p style="text-indent:2em;">'
                else:
                    if len(between_content) != 0:
                        between_content = self.left_space_pattern.sub('', between_content)
                        between_content = self.right_space_pattern.sub('', between_content)
                        format_chapter_content += u'<p style="text-indent:2em;">' + between_content \
                                                  + u'</p><p style="text-indent:2em;">'
                    else:
                        format_chapter_content += u'<p style="text-indent:2em;">'

                p_level = 1
                is_p_head = True
            elif tag_name == '/p' or tag_name == '/div':
                #p_level等于1。去掉段尾的空格。为了以防原文格式不正常，else予以处理
                if p_level == 1:
                    between_content = self.right_space_pattern.sub('', between_content)
                    format_chapter_content += between_content + u'</p>'
                else:
                    if len(between_content) != 0:
                        between_content = self.left_space_pattern.sub('', between_content)
                        between_content = self.right_space_pattern.sub('', between_content)
                        format_chapter_content += u'<p style="text-indent:2em;">' + between_content + u'</p>'
                    else:  # 多余的</p>
                        pass

                p_level = 0
                is_p_head = False
            elif tag_name == 'meet_need_remove':
                #需要输出需要need_remove的html标签之前的内容
                #条件len(between_content) != 0 and not between_content.isspace()是防止之后的段首空格可能未被去除
                if p_level == 0 and len(between_content) != 0 and not between_content.isspace():
                    between_content = self.left_space_pattern.sub('', between_content)
                    format_chapter_content += u'<p style="text-indent:2em;">' + between_content

                    p_level = 1
                else:
                    format_chapter_content += between_content
            elif tag_name == 'img':
                #<img data-width="8" data-height="16" src="" alt="男"/>
                #抽取alt属性值
                alt_search = self.alt_pattern.search(tag)
                if alt_search is not None:
                    alt_content = alt_search.group(2)
                    between_content += alt_content

                if p_level == 0 and len(between_content) != 0 and not between_content.isspace():
                    between_content = self.left_space_pattern.sub('', between_content)
                    format_chapter_content += u'<p style="text-indent:2em;">' + between_content

                    p_level = 1
                else:
                    format_chapter_content += between_content
            else:
                if p_level == 0 and len(between_content) != 0 and not between_content.isspace():
                    between_content = self.left_space_pattern.sub('', between_content)
                    format_chapter_content += u'<p style="text-indent:2em;">' + between_content

                    p_level = 1
                else:
                    format_chapter_content += between_content

        # 处理上一个标签至末尾的文本，通常不需要
        if pre_end != len(raw_chapter_content):
            between_content = raw_chapter_content[pre_end:]
            between_content = self.right_space_pattern.sub('', between_content)  # 一定是段尾
            if len(between_content) != 0:
                if p_level == 0:
                    between_content = self.left_space_pattern.sub('', between_content)
                    format_chapter_content += u'<p style="text-indent:2em;">' + between_content + u'</p>'
                else:
                    format_chapter_content += between_content + u'</p>'
                    p_level == 0

        #如果html不规范，有未闭合的<p>，在章节末尾添加，此时可能段尾的空格没有被去除。
        if p_level != 0:
            format_chapter_content += u'</p>'

        #去除<p></p>
        format_chapter_content = self.empty_p_pattern.sub('', format_chapter_content)

        return format_chapter_content

    def run(self, chapter_page, cid=0):
        """
        输入chapter_page，过滤并处理其中的html标签后，返回处理后的chapter_page

        返回的chapter_page中的NOVELCONTENT满足如下条件：
        1，只包含<p>和</p>
        2，页面完整，无tag缺失或者<p>嵌套的情况
        """
        for block in chapter_page['blocks']:
            if 'type' in block and block['type'] == 'NOVELCONTENT':
                raw_chapter_content = block['data_value']
                fmt_chapter_content = self.chapter_html_filter(raw_chapter_content)

                # 考虑到某些站点会隐藏某些正文，导致格式化前后中文字符差距大，阈值设为总数的1/2
                raw_zh_count = count_chinese(raw_chapter_content)
                fmt_zh_count = count_chinese(fmt_chapter_content)
                if raw_zh_count != fmt_zh_count:
                    self.logger.info('cid: {0}, raw_count: {1}, fmt_count: {2}'.format(cid, raw_zh_count, fmt_zh_count))

                # 如果中文字符丢失超过一半，返回未格式化的正文
                # zh_threshold = raw_zh_count / 2
                # if raw_zh_count - fmt_zh_count > zh_threshold:
                #     self.err.warning('cid: {0}, lost of chinese char exceeds the threshold: {1}'.format(
                #         cid, raw_zh_count - fmt_zh_count))
                #     return chapter_page

                #格式化章节内容后，写回chapter_page
                block['data_value'] = fmt_chapter_content
                break

        return chapter_page
