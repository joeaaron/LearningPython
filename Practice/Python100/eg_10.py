#!/usr/bin/env python
# -*- coding: UTF-8 -*-
############################################################
#  Created on: 2017-12-26
#  Author: Joe Aaron
#  Email:  pant333@163.com
#  Description:  暂停一秒输出，并格式化当前时间。
############################################################
import time

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# 暂停一秒
time.sleep(1)

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


