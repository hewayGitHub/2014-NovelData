#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-12 22:34'

from collections import defaultdict


def here():
    print('PrimeMusic')


class TrieNode(object):
    """
        Trie���ϵ�һ���ڵ�
    """
    def __init__(self, char = '', count = 0):
        """
        """
        self.char = char
        self.count = count

        self.child = defaultdict(object)


    def insert_child(self, char = ''):
        """
        """
        self.child[char] = TrieNode(char)



class Trie(object):
    """
        Trie��
    """
    def __init__(self):
        """
            ��ʼ�����ڵ�
        """
        self.root = TrieNode('')


    def insert_string(self, string = ''):
        """
            ��Trie��������һ���ַ���
        """
        node = self.root
        for char in string:
            if node.child.has_key(char):
                node = node.child[char]
            else:
                node.insert_child(char)
                node = node.child[char]
            node.count += 1


    def find_common_prefix(self, node, count = 2, prefix = ''):
        """
            ��Trie�����ҵ����ִ������ڵ���count�������ǰ׺
        """
        prefix += node.char
        current_prefix = prefix
        for (char, child_node) in node.child.items():
            if child_node.count >= count:
                string = self.find_common_prefix(child_node, count, current_prefix)
                if len(string) > len(prefix):
                    prefix = string
        return prefix


if __name__ == '__main__':

    trie = Trie()
    trie.insert_string(u'��һ�� ������Ƭ')
    trie.insert_string(u'һ�� ����Ժ')
    trie.insert_string(u'��һ��-1-������Ƭ')
    trie.insert_string(u'��һ�� ��ѧ֮��')
    trie.insert_string(u'��һ��-1- �����Ǹ���')
    trie.insert_string(u'��һ��-1- ����Ժ')

    print(trie.find_common_prefix(trie.root, 2, '').encode('utf8', 'ignore'))

    here()    







