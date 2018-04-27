#!/usr/bin/env python
# -*- coding: UTF-8 -*-
############################################################
#  Created on: 2018-04-26
#  Author: Joe Aaron
#  Email:  pant333@163.com
#  Description: 将 0001 题生成的 200 个激活码（或者优惠券）保存到 MySQL 关系型数据库中。
import mysql.connector

import random
import string

forSelect = string.ascii_letters + string.digits

def generate_code(count, length):
    for x in range(count):
        Re = ""
        for y in range(length):
            Re += random.choice(forSelect)
        yield Re
 
def save_code():
    conn = mysql.connector.connect(user='root', password='1', database='test')
    cursor = conn.cursor()
    codes = generate_code(200, 20)
    for code in codes:
        cursor.execute("INSERT INTO `code`(`code`) VALUES(%s)", params=[code])
    conn.commit()
    cursor.close()
    
if __name__ == '__main__':
    save_code()