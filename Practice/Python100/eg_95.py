#!/usr/bin/env python
# -*- coding: UTF-8 -*-
############################################################
#  Created on: 2017-12-26
#  Author: Joe Aaron
#  Email:  pant333@163.com
#  Description: 字符串日期转换为易读的日期格式。
############################################################
from dateutil import parser
dt = parser.parse("Aug 28 2015 12:00AM")
print dt