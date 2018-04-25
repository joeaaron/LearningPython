#!/usr/bin/env python
# -*- coding: UTF-8 -*-
############################################################
#  Created on: 2018-04-25
#  Author: Joe Aaron
#  Email:  pant333@163.com
#  Description:  做为 Apple Store App 独立开发者，你要搞限时促销，为你的应用生成激活码（或者优惠券），使用 Python 如何生成 200 个激活码（或者优惠券）？
############################################################
from random import Random

def CodeGenerator(number, codeLength = 15):
    print '**** Code Generator ****'
    codeFile = open('code.txt', 'w')
    if number <= 0:
        return 'invalid number of codes'
    else:
        chars = 'abcdefghijklmnopgrstuvwxyzABCDEFGHIJKLMNOPGRSTUVWXYZ1234567890'
        random = Random()
        for j in range(1, number + 1):
            str = ''
            for i in range(1, codeLength + 1):
                index = random.randint(1, len(chars))
                str = str + chars[index - 1]
            codeFile.write(str + '\n')
            
print CodeGenerator(10)