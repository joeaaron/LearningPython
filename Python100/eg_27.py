#!/usr/bin/env python
# -*- coding: UTF-8 -*-
############################################################
#  Created on: 2017-12-26
#  Author: Joe Aaron
#  Email:  pant333@163.com
#  Description:  利用递归函数调用方式，将所输入的5个字符，以相反顺序打印出来。
############################################################
def output(s, l):
    if 0 == l:
        return
    print(s[l - 1])
    output(s, l-1)

s = raw_input("input a string:")
l = len(s)
output(s, l)
