#!/usr/bin/env python
# -*- coding: UTF-8 -*-
############################################################
#  Created on: 2017-12-26
#  Author: Joe Aaron
#  Email:  pant333@163.com
#  Description:  九九乘法表
############################################################
for i in range(1, 10):
    print
    for j in range(1, i+1):
        print "%d*%d=%d" % (i, j, i*j)