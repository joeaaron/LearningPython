#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -*-encoding=utf-8
############################################################
#  Created on: 2018-04-28
#  Author: Joe Aaron
#  Email:  pant333@163.com
#  Description:  一个HTML文件，找出里面的链接。
import requests,re,os
from bs4 import BeautifulSoup

url = 'http://linyii.com'
data=requests.get(url)
# urls = re.findall(r'<a.*href=\"(.*?)\".*</a>',data.text)
# print(urls)

soup = BeautifulSoup(data.text,'html.parser')
urls = soup.findAll('a')
for u in urls:
    print(u['href'])