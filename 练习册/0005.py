#!/usr/bin/env python
# -*- coding: UTF-8 -*-
############################################################
#  Created on: 2018-04-27
#  Author: Joe Aaron
#  Email:  pant333@163.com
#  Description:  你有一个目录，装了很多照片，把它们的尺寸变成都不大于 iPhone5 分辨率的大小。
from __future__ import division
from PIL import Image
import os

path = 'images/0005/pics'
resultPath = 'images/0005/result'
if not os.path.isdir(resultPath):
    os.mkdir(resultPath)
for picName in os.listdir(path):
    picPath = os.path.join(path, picName)
    print(picPath)
    with Image.open(picPath) as im:
        w, h = im.size
        n = w / 1366 if (w / 1366) >= (h / 640) else h / 640
        try:
            im.thumbnail((w / n, h / n))       #生成缩略图
        except ZeroDivisionError:
            print "division by zero!"
        
        im.save(resultPath+'/finish_' + picName.split('.')[0] + '.jpg', 'jpeg')