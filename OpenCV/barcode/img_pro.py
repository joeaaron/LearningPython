# -*- coding: utf-8 -*-

import os
from bar_code import detect

#ÇĞ»»µ½²âÊÔÍ¼Æ¬ÎÄ¼ş¼Ğ
os.chdir('imgs')

image_names = os.listdir()

if _name_=='_main_':
    for image_name in image_names:
        detect(image_name)