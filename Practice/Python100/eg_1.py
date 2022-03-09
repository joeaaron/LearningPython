#!/usr/bin/env python
# -*- coding: UTF-8 -*-
############################################################
#  Created on : 2017-12-26
#  Author : Joe Aaron
#  Email :  pant333@163.com
#  Description :  有四个数字：1、2、3、4，能组成多少个互不相同且无重复数字的三位数？各是多少？
#  Website : http://www.runoob.com/python/python-100-examples.html
############################################################
d = []
for i in range(1, 5):
    for j in range(1, 5):
        for k in range(1, 5):
            if (i != k) and (i != j) and (j != k):
                d.append([i, j, k])
print "total num :", len(d)
print d

