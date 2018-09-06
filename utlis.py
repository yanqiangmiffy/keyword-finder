# -*- coding: utf-8 -*-
# @Author  : quincyqiang
# @File    : utlis.py
# @Time    : 2018/9/6 10:29


def generate_name(word_tags):
    name_pos = ['ns', 'n', 'vn', 'nr', 'nt', 'eng', 'nrt']
    for word_tag in word_tags:
        if word_tag[0] == '·' or word_tag[0]=='！':
            index = word_tags.index(word_tag)
            if (index+1)<len(word_tags):
                prefix = word_tags[index - 1]
                suffix = word_tags[index + 1]
                if prefix[1] in name_pos and suffix[1] in name_pos:
                    name = prefix[0] + word_tags[index][0] + suffix[0]
                    word_tags = word_tags[index + 2:]
                    word_tags.insert(0, (name, 'nr'))
    return word_tags


def judge_not_one(key_1,key_2,true_key):
    """
    命中一个关键词的情况
    :param key_1:
    :param key_2:
    :param true_key:
    :return:
    """
    if key_1 not in true_key and key_2 in true_key:
        return True
    if key_1 in true_key and key_2 not in true_key:
        return True


def judge_not_two(key_1,key_2,true_key):
    if key_1 not in true_key and key_2 not in true_key:
        return True