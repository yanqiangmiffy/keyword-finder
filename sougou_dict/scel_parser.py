# -*- coding: utf-8 -*-
# @Author  : quincyqiang
# @File    : scel_parser.py
# @Time    : 2018/9/11 10:35


import struct
import os
import random
class ScelParser():
    def __init__(self):
        pass

    def parse(self, content):
        hz_offset = 0
        mask = struct.unpack('128B', content[:128])[4]
        if mask == 0x44:
            hz_offset = 0x2628
        elif mask == 0x45:
            hz_offset = 0x26c4
        index = hz_offset
        words = set([])
        while index < len(content):
            word_count = struct.unpack('<H', content[index:index + 2])[0]
            index += 2
            pinyin_count = int(struct.unpack('<H', content[index:index + 2])[0] / 2)
            index += 2
            index += pinyin_count * 2

            for i in range(word_count):
                word_len = struct.unpack('<H', content[index:index + 2])[0]
                index += 2
                word= content[index:index + word_len].decode('UTF-16LE')
                index += word_len
                index += 12
                words.add(word)

        return list(words)

    def parse_file(self, filepath):
        with open(filepath, 'rb') as f:
            words = self.parse(f.read())
        return words

if __name__ == '__main__':

    scel_parser = ScelParser()

    f = open('sogou_dict.txt', 'w',encoding='utf-8')
    for flag in os.listdir('scel_files/'):
        file_names = os.listdir('scel_files/' + flag)
        o = ['scel_files/' + flag + '/' + file_name for file_name in file_names]
        for scel_file in o:
            words=scel_parser.parse_file(scel_file)
            for word in words:
                f.write(word)
                f.write(' ' + str(random.randint(100,500)) + ' ')
                if flag == 'nr':
                    f.write('nr')
                elif flag == 'nz':
                    f.write('nz')
                elif flag == 'nt':
                    f.write('nt')
                else:
                    pass
                f.write('\n')

    f.close()