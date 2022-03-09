#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# Author: JoeAaron
# Created Time : Mon 07 Jan 2019 07:46:23 AM CST
# File Name: mindstorms.py
# Description:
"""
import turtle

def draw_square(some_turtle):
    for i in range(1,5):
        some_turtle.forward(100)
        some_turtle.right(90)

def draw_art():
    window = turtle.Screen()
    window.bgcolor("red")
    #Create the turtle Brad - Draws a square
    brad = turtle.Turtle()
    brad.shape("turtle")
    brad.color("yellow")
    brad.speed(2)
    draw_square(brad)
    #Create the turtle Angie - Draws a circle
    angie = turtle.Turtle()
    angie.shape("arrow")
    angie.color("blue")
    angie.circle(100)

    window.exitonclick()

draw_art()
