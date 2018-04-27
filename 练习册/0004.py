#!/usr/bin/env python
# -*- coding: UTF-8 -*-
############################################################
#  Created on: 2018-04-27
#  Author: Joe Aaron
#  Email:  pant333@163.com
#  Description:  任一个英文的纯文本文件，统计其中的单词出现的个数。
import re

fin = open('source/0004-text.txt', 'r')
str = fin.read()

reObj = re.compile('\b?(\w+)\b?')
words = reObj.findall(str)

#dict() 函数用于创建一个字典
wordDict = dict()

for word in words:
    if word.lower() in wordDict:
        wordDict[word.lower()] += 1
    else:
        wordDict[word] = 1
        
for key, value in wordDict.items():
    print('%s: %s' % (key, value))