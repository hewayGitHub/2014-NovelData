#!/usr/bin/env python
# -*- coding:GBK

__author__ = 'sunhaowen'
__date__ = '2014-03-08 20:20'

from basic.NovelStructure import Singleton
from collections import defaultdict

def here():
    print('PrimeMusic')

class Node(object):
    """
        Trie树上的一个节点
    """
    def __init__(self, char):
        """
        """
        self.char = char

        self.count = 0
        self.probability = 0.0
        self.inner_cohesion_degree = 0.0
        self.pre_info_entropy = 0.0
        self.suf_info_entropy = 0.0

        self.child_dict = defaultdict(object)
        self.pre_char_dict = defaultdict(int)
        self.suf_char_dict = defaultdict(int)


    def get_child(self, char = ''):
        """
        """
        if not self.child_dict.has_key(char):
            self.child_dict[char] = Node(char)
        return self.child_dict[char]


    def add_word(self, pre_char, suf_char):
        """
        """
        self.count += 1
        if pre_char != '*':
            self.pre_char_dict[pre_char] += 1
        if suf_char != '*':
            self.suf_char_dict[suf_char] += 1



class Trie(object):
    """
    """
    __metaclass__ = Singleton

    def __init__(self):
        """
        """
        self.root = Node('')


    def set_total_count(self, total_count):
        """
        """
        self.total_count = total_count


    def get_node(self, word):
        """
        """
        node = self.root
        for char in word:
            node = node.get_child(char)

        return node


    def insert_word_tuple(self, word, pre_char, suf_char):
        """
        """
        node = self.get_node(word)
        node.add_word(pre_char, suf_char)


    def word_probability_calculation(self, node):
        """
        """
        for (char, child) in node.child_dict.items():
            self.word_probability_calculation(child)

        if node.count > 0:
            node.probability = 1.0 * node.count / self.total_count


    def word_cohesion_calculation(self, node, word):
        """
        """
        for (char, child) in node.child_dict.items():
            self.word_cohesion_calculation(child, word + char)

        if node.count == 0:
            return

        if len(word) == 1:
            node.inner_cohesion_degree = 1.0
            return






if __name__ == '__main__':
    here()    







