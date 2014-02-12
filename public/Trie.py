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
    def __init__(self, char = '', count = 0, length = 0):
        """
        """
        self.char = char
        self.count = count
        self.length = length
        self.child = defaultdict(object)


    def insert_child(self, char = ''):
        """
        """
        self.child[char] = TrieNode(char, 0, self.length + 1)



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




if __name__ == '__main__':
    here()    







