#!/usr/bin/env python
# -*- coding: UTF-8 -*-
############################################################
#  Created on: 2018-05-04
#  Author: Joe Aaron
#  Email:  pant333@163.com
#  Description:  将文本文件中的内容写到xls文件中。
############################################################
from collections import OrderedDict

import xlwt,json

with open('source/0014/student.txt', 'r') as f:
    data = json.load(f,object_pairs_hook = OrderedDict)
    workbook = xlwt.Workbook()
    sheet1 = workbook.add_sheet('student', cell_overwrite_ok=True)
    for index, (key, values) in enumerate(data.items()):
        sheet1.write(index, 0, key)
        for i, value in enumerate(values):
            sheet1.write(index, i+1, value)
    workbook.save('source/0014/student.xls')