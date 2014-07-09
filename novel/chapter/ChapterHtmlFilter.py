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
    ͳ���ַ����к��֡���ĸ�����ֵĸ���
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
    ͳ���ַ����к��ֵĸ���
    """
    cn_count = 0
    for char in unicode_str:
        if is_chinese(char):
            cn_count += 1

    return cn_count

class ChapterHtmlFilter(object):
    """
    ����chapter_page�����˲��������е�html��ǩ�󣬷��ش�����chapter_page

    ���ص�chapter_page�е�NOVELCONTENT����ʽ��������������
    1��ֻ����<p>��</p>
    2��ҳ����������tagȱʧ����<p>Ƕ�׵����
    """
    __metaclass__ = Singleton

    def __init__(self):
        """
        ��ʼ��html���������������ʽ
        """
        self.logger = logging.getLogger('novel.chapter.html')
        self.err = logging.getLogger('err.chapter.html')

        #����htmlת���ַ�
        self.html_parser = HTMLParser.HTMLParser()

        # ����������ʽ����ʶ�����ж�Ӧtag����ʽ
        self.left_space_pattern = re.compile(r'^(\s|&nbsp;)+', re.U)
        self.right_space_pattern = re.compile(r'(\s|&nbsp;)+$', re.U)
        self.tag_pattern = re.compile(r'<(/?[a-zA-Z!]+)([^>]*)>', re.U)

        self.hidden_pattern = re.compile(r'display\s*:\s*none', re.U | re.I)
        self.invisible_pattern = re.compile(r'visibility\s*:\s*hidden', re.U | re.I)
        self.alt_pattern = re.compile(r'\salt=(.)(.*?)\1', re.U | re.I)

        self.empty_p_pattern = re.compile(r'<p style="text-indent:2em;"></p>', re.U)

    def chapter_html_filter(self, raw_chapter_content):
        """
        ���˲������½������е�HTML�������ش������½����ġ�
        �����������½����Ķ���unicode���롣����ȥ���κ���ǰ�˿ɼ��ַ������ұ�֤����htmlҳ��ֻ����<p></p>���Ҹ�ʽ�淶��
        ���ң����ж��ס���β�Ŀո񶼱�ȥ���ˡ�

        ����Ҫ�����£�
        0��������β�հ��ַ�ȥ��
        1��������½�����ֻ��<p>��</p>�����Ҳ�����Ƕ�ס�
        2��Ϊ<p>�������<p style="text-indent:2em;">���������������ַ�
        3������<script>��ǩ������֮����ı�
        4�����˰����������Եı�ǩ������֮����ı���
        5��ĳЩվ������ͼƬ�滻���֣�<img data-width="8" data-height="16" src="" alt="��"/>
        6��ɾ���հ׶�

        ע�⣻
        1��HTML��ǩ����ʼ�ַ�Ϊ[a-zA-Z!]�����Ա�֤����ƥ��<1><���>֮�������
        2�����ڱ�ǩp��/p��div��Ҫȷ����ȫƥ�䣬��Ϊ���ǿ�����������ǩ��ǰ׺��ͨ����ȡ��ǩ��ƥ��
        3��ͨ��ʹ��unicode��\s����ƥ����չ�������ģ�ISO 8859-1���еĲ���Ͽո�\xa0��"&nbsp;"�����Ŀո�\u3000�ȿհ��ַ�
        4�����пɼ������Ķ��������������п�����С˵���ġ�����<a>��ǩ��ʱ��������ֻ��ȥ����ǩ���ں�������ȥ�Ӵ���
        5���ȴ���htmlת���ַ����Ա�html��ǩ��⣬��������ȥ��&amp;�Ͳ��ᱻ��Ϊ����
        """
        #����htmlת���ַ����Ա�html��ǩ��⣬��������ȥ��&amp;�Ͳ��ᱻ��Ϊ����
        raw_chapter_content = self.html_parser.unescape(raw_chapter_content)

        format_chapter_content = u''

        # ��ɸ�ʽ������0-9
        pre_end = 0  # ��־��һ��tag��βindex + 1���ʳ�ʼ��Ϊ0
        p_level = 0  # ����<p>��1������</p>��1
        is_p_head = True  # ��ǵ�ǰ�����Ƿ��Ƕ��ף�����ȥ�����׵Ŀո�.��ʼֵΪTrue���Է���һ��tagǰ������
        need_remove = False  # ������<script>������Ҫ���صı�ǩʱ��ΪTrue��ȥ����β��ǩ�Լ�����֮�������
        remove_tag_level = 0  # �����ж���Ҫȥ���ı�ǩ��β��ǩ���磬<div style='display:none'> <div> </div> </div>
        remove_tag_name = ''  # ��Ҫȥ���ı�ǩ������
        for tag_match in self.tag_pattern.finditer(raw_chapter_content):
            tag = tag_match.group()
            tag_name = tag_match.group(1).lower()  # html��ǩ�����ִ�Сд��ͳһת��ΪСд
            first = tag_match.start()
            end = tag_match.end()

            # ������<script>������Ҫ���صı�ǩʱ������need_removeΪTrue
            # �����ǰneed_removeΪTrue��������ǰtag��ǰһ��tag֮������Ĳ���Ҫ�����
            # ͬʱ��Ҫ����Ƿ��뿪need_remove��ǩ�ڲ�
            if not need_remove:
                if tag_name == u'script' or self.hidden_pattern.search(tag) is not None \
                        or self.invisible_pattern.search(tag) is not None:
                    need_remove = True
                    remove_tag_name = tag_name
                    remove_tag_level = 1

                    #��Ҫ�����Ҫneed_remove��html��ǩ֮ǰ������
                    tag_name = u'meet_need_remove'
            else:
                if tag_name == remove_tag_name:
                    remove_tag_level += 1
                elif tag_name[1:] == remove_tag_name:
                    remove_tag_level -= 1

                if remove_tag_level == 0:
                    need_remove = False

                #����pre_end
                pre_end = end
                continue

            #is_p_head�����ڶ��ף�ֱ�������ǿյ����ģ������൱��һֱ�Ƕ���
            if is_p_head:  # ����
                if pre_end == first:
                    between_content = u''
                else:
                    between_content = self.left_space_pattern.sub('', raw_chapter_content[pre_end:first])

                if len(between_content) != 0:
                    is_p_head = False
            else:
                between_content = raw_chapter_content[pre_end:first]

            #����pre_end
            pre_end = end

            if tag_name == 'p' or tag_name == 'div' or tag_name == 'br':
                #����div��p��br����ʾ�¶���Ŀ�ʼ
                #���p_level���ڵ���1����ʾ�����<p>��Ƕ�ף��ڵ�ǰ<p>ǰ���</p>����ֹǶ�׳���
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
                #p_level����1��ȥ����β�Ŀո�Ϊ���Է�ԭ�ĸ�ʽ��������else���Դ���
                if p_level == 1:
                    between_content = self.right_space_pattern.sub('', between_content)
                    format_chapter_content += between_content + u'</p>'
                else:
                    if len(between_content) != 0:
                        between_content = self.left_space_pattern.sub('', between_content)
                        between_content = self.right_space_pattern.sub('', between_content)
                        format_chapter_content += u'<p style="text-indent:2em;">' + between_content + u'</p>'
                    else:  # �����</p>
                        pass

                p_level = 0
                is_p_head = False
            elif tag_name == 'meet_need_remove':
                #��Ҫ�����Ҫneed_remove��html��ǩ֮ǰ������
                #����len(between_content) != 0 and not between_content.isspace()�Ƿ�ֹ֮��Ķ��׿ո����δ��ȥ��
                if p_level == 0 and len(between_content) != 0 and not between_content.isspace():
                    between_content = self.left_space_pattern.sub('', between_content)
                    format_chapter_content += u'<p style="text-indent:2em;">' + between_content

                    p_level = 1
                else:
                    format_chapter_content += between_content
            elif tag_name == 'img':
                #<img data-width="8" data-height="16" src="" alt="��"/>
                #��ȡalt����ֵ
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

        # ������һ����ǩ��ĩβ���ı���ͨ������Ҫ
        if pre_end != len(raw_chapter_content):
            between_content = raw_chapter_content[pre_end:]
            between_content = self.right_space_pattern.sub('', between_content)  # һ���Ƕ�β
            if len(between_content) != 0:
                if p_level == 0:
                    between_content = self.left_space_pattern.sub('', between_content)
                    format_chapter_content += u'<p style="text-indent:2em;">' + between_content + u'</p>'
                else:
                    format_chapter_content += between_content + u'</p>'
                    p_level == 0

        #���html���淶����δ�պϵ�<p>�����½�ĩβ��ӣ���ʱ���ܶ�β�Ŀո�û�б�ȥ����
        if p_level != 0:
            format_chapter_content += u'</p>'

        #ȥ��<p></p>
        format_chapter_content = self.empty_p_pattern.sub('', format_chapter_content)

        return format_chapter_content

    def run(self, chapter_page, cid=0):
        """
        ����chapter_page�����˲��������е�html��ǩ�󣬷��ش�����chapter_page

        ���ص�chapter_page�е�NOVELCONTENT��������������
        1��ֻ����<p>��</p>
        2��ҳ����������tagȱʧ����<p>Ƕ�׵����
        """
        for block in chapter_page['blocks']:
            if 'type' in block and block['type'] == 'NOVELCONTENT':
                raw_chapter_content = block['data_value']
                fmt_chapter_content = self.chapter_html_filter(raw_chapter_content)

                # ���ǵ�ĳЩվ�������ĳЩ���ģ����¸�ʽ��ǰ�������ַ�������ֵ��Ϊ������1/2
                raw_zh_count = count_chinese(raw_chapter_content)
                fmt_zh_count = count_chinese(fmt_chapter_content)
                if raw_zh_count != fmt_zh_count:
                    self.logger.info('cid: {0}, raw_count: {1}, fmt_count: {2}'.format(cid, raw_zh_count, fmt_zh_count))

                # ��������ַ���ʧ����һ�룬����δ��ʽ��������
                # zh_threshold = raw_zh_count / 2
                # if raw_zh_count - fmt_zh_count > zh_threshold:
                #     self.err.warning('cid: {0}, lost of chinese char exceeds the threshold: {1}'.format(
                #         cid, raw_zh_count - fmt_zh_count))
                #     return chapter_page

                #��ʽ���½����ݺ�д��chapter_page
                block['data_value'] = fmt_chapter_content
                break

        return chapter_page
