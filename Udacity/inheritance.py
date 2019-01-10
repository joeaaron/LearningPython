#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# Author: JoeAaron
# Created Time : Thu 10 Jan 2019 08:46:26 PM CST
# File Name: inheritance.py
# Description: inheritance and override
"""
class Parent():
    def __init__(self, last_name, eye_color):
        print("Parent Constructor Called")
        self.last_name = last_name
        self.eye_color = eye_color

    def show_info(self):
        print("Last Name -" +self.last_name)
        print("Eye Color -" +self.eye_color)

class Child(Parent):
    def __init__(self, last_name, eye_color, number_of_toys):
        print("Child Constructor Called")
        Parent.__init__(self, last_name, eye_color)
        self.number_of_toys = number_of_toys

    def show_info(self):
        print("Last Name -" +self.last_name)
        print("Eye Color -" +self.eye_color)
        print("Number of toys -" +self.number_of_toys)

billy_cycrus = Parent("Cyrus", "blue")
# int to str
miley_cyrus = Child("Cyrus", "blue",bytes(5))
miley_cyrus.show_info()
