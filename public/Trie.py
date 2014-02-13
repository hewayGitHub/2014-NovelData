#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-02-12 22:34'

from collections import defaultdict


def here():
    print('PrimeMusic')


class TrieNode(object):
    """
        Trie树上的一个节点
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
        Trie树
    """
    def __init__(self):
        """
            初始化根节点
        """
        self.root = TrieNode('')


    def insert_string(self, string = ''):
        """
            向Trie树中增加一个字符串
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
            在Trie树上找到出现次数大于等于count的最长公共前缀
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
    trie.insert_string(u'第一章 六安瓜片')
    trie.insert_string(u'一章 北灵院')
    trie.insert_string(u'第一章-1-六安瓜片')
    trie.insert_string(u'第一章 数学之美')
    trie.insert_string(u'第一章-1- 标题是浮云')
    trie.insert_string(u'第一章-1- 北灵院')

    print(trie.find_common_prefix(trie.root, 2, '').encode('utf8', 'ignore'))

    here()    







