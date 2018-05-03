#!/usr/bin/env python
# -*- coding: UTF-8 -*-
############################################################
#  Created on: 2018-05-03
#  Author: Joe Aaron
#  Email:  pant333@163.com
#  Description:  当用户输入敏感词语，则用 星号 * 替换，例如当用户输入「北京是个好城市」，则变成「**是个好城市」。
############################################################
import string

word_filter=set()

with open('source/0011/filtered_words.txt') as f:
    for w in f.readlines():
        word_filter.add(w.strip())
        
while True:
    s=input()
    if s == 'exit':
        break
    for w in word_filter:
        if w in s:
            s= s.replace(w,'*'*len(w))
    print(s)
    