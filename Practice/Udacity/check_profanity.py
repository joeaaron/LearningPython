#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# Author: JoeAaron
# Created Time : Tue 08 Jan 2019 08:31:37 PM CST
# File Name: check_profanity.py
# Description:
"""
import urllib

def read_text():
    quotes = open("movie_quotes.txt")
    contents_of_file = quotes.read()
    print(contents_of_file)
    quotes.close()
    check_profanity(contents_of_file)

def check_profanity(text_to_check):
    connection = urllib.urlopen("http://www.wdyl.com/profanity?q="+text_to_check)
    output = connection.read()
    print(output)
    connection.close()

read_text()
