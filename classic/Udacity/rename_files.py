#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# Author: JoeAaron
# Created Time : Sat 05 Jan 2019 10:09:35 PM CST
# File Name: rename_files.py
# Description:
"""
import os
def rename_files():
    #(1) get file names from a folder
    file_list = os.listdir(r"C:\OOP\prank")
    print(file_list)
    saved_path = os.getcwd()
    print("Current Working Directory is "+ saved_path)
    os.chdir(r"C:\OOP\prank")
    #(2) for each file, rename filename
    for file_name  in file_list:
        os.rename(file_name, file_name.translate(None, "0123456789"))
rename_files()

