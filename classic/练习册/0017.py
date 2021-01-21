#!/usr/bin/env python
# -*- coding: UTF-8 -*-
############################################################
#  Created on: 2018-05-04
#  Author: Joe Aaron
#  Email:  pant333@163.com
#  Description:  将 第 0014 题中的 student.xls 文件中的内容写到 student.xml 文件中
############################################################
from collections import OrderedDict

import xlwt,json

with open('source/0014/student.txt', 'r') as f:
    L = []
    L.append(r"""
<?xml version="1.0" encoding="UTF-8"?>
<root>
<students>
<!--
	学生信息表
	"id" : [名字, 数学, 语文, 英文]
-->
    """)
    L.append(f.read())
    L.append(r"""
</students>
</root>
    """)
    with open('source/0014/student.xml', 'w') as s:
        s.write(''.join(L))
